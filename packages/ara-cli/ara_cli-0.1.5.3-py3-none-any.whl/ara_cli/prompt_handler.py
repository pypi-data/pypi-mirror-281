import base64
from langchain_openai import ChatOpenAI
from ara_cli.classifier import Classifier
from ara_cli.template_manager import TemplatePathManager
from ara_cli.ara_config import ConfigManager
from ara_cli.file_lister import generate_markdown_listing
from os.path import exists, join, splitext, isfile
import os
from os import makedirs, listdir, environ
from sys import exit
from subprocess import run
from re import findall
import re
import shutil
import glob

class ChatOpenAISingleton:
    _instance = None

    def __init__(self):
        ChatOpenAISingleton._instance = ChatOpenAI(openai_api_key=environ.get("OPENAI_API_KEY"), model_name='gpt-4o')

    @staticmethod
    def get_instance():
        if ChatOpenAISingleton._instance is None:
            ChatOpenAISingleton()
        return ChatOpenAISingleton._instance    

def write_string_to_file(filename, string, mode):
    with open(filename, mode) as file:
            file.write(f"\n{string}\n")
    return file

def read_string_from_file(path):
    with open(path, 'r') as file:
            text = file.read()
    return text

def send_prompt_message_list(message_list):
    chat = ChatOpenAISingleton.get_instance()
    chat_result = chat.invoke(message_list)
    return chat_result.content

def send_prompt(prompt):
    chat = ChatOpenAISingleton.get_instance()
    chat_result = chat.invoke(prompt)
    return chat_result.content

def append_headings(classifier, param, heading_name):
    sub_directory = Classifier.get_sub_directory(classifier)

    artefact_data_path = f"ara/{sub_directory}/{param}.data/{classifier}.exploration.md"
    content = read_string_from_file(artefact_data_path)
    pattern = r'## {}_(\d+)'.format(heading_name)
    matches = findall(pattern, content)

    max_number = 1
    if matches:
        max_number = max(map(int, matches)) + 1
    heading = f"## {heading_name}_{max_number}"
            
    write_string_to_file(artefact_data_path, heading, 'a')

def write_prompt_result(classifier, param, text):
    sub_directory = Classifier.get_sub_directory(classifier)

    # TODO change absolute path to relative path with directory navigator
    artefact_data_path = f"ara/{sub_directory}/{param}.data/{classifier}.exploration.md"
    write_string_to_file(artefact_data_path, text, 'a')

def prompt_data_directory_creation(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = f"ara/{sub_directory}/{parameter}.data/prompt.data"
    if not exists(prompt_data_path):
        makedirs(prompt_data_path)
    return prompt_data_path

def get_file_content(path):
    with open(path, 'r') as file:
        return file.read()


def initialize_prompt_templates(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = prompt_data_directory_creation(classifier, parameter)
    
    generate_config_prompt_template_file(prompt_data_path, "config.prompt_templates.md")
    
    # Mark the relevant artefact in the givens list
    generate_config_prompt_givens_file(prompt_data_path, "config.prompt_givens.md", artefact_to_mark=f"{parameter}.{classifier}")

def write_template_files_to_config(template_type, config_file, base_template_path):
    template_path = os.path.join(base_template_path, template_type)
    for root, _, files in os.walk(template_path):
        for file in sorted(files):
            config_file.write(f"  - [] {template_type}/{file}\n")

def load_selected_prompt_templates(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = f"ara/{sub_directory}/{parameter}.data/prompt.data"
    config_file_path = os.path.join(prompt_data_path, "config.prompt_templates.md")

    if not os.path.exists(config_file_path):
        print("WARNING: config.prompt_templates.md does not exist.")
        return

    with open(config_file_path, 'r') as config_file:
        content = config_file.read()

    global_base_template_path = TemplatePathManager.get_template_base_path_prompt_modules()
    local_base_template_path = ConfigManager.get_config().local_prompt_templates_dir

    markdown_items = extract_and_load_markdown_files(config_file_path)

    # Ensure the prompt archive directory exists
    prompt_archive_path = os.path.join(prompt_data_path, "prompt.archive")
    if not os.path.exists(prompt_archive_path):
        os.makedirs(prompt_archive_path)
        print(f"Created archive directory: {prompt_archive_path}")

    for item in markdown_items:
        if item.startswith("custom-prompt-modules"):
            source_path = os.path.join(local_base_template_path, item)
            target_path = os.path.join(prompt_data_path, os.path.basename(item))
        elif item.startswith("prompt-modules"):
            source_path = os.path.join(global_base_template_path, item)
            target_path = os.path.join(prompt_data_path, os.path.basename(item))
        else:
            print(f"WARNING: Unrecognized template type for item {item}.")
            continue

        move_and_copy_files(source_path, prompt_data_path, prompt_archive_path)

def find_files_with_endings(directory, endings):
    """
    this function finds only files in the given directory it does not iterate recursively over sub directories
    """

    # Create an empty dictionary to store files according to their endings
    files_by_ending = {ending: [] for ending in endings}

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # Walk through the files list
    for file in files:
        # Check each file to see if it ends with one of the specified endings
        for ending in endings:
            if file.endswith(ending):
                # If it does, append the file to the corresponding list
                files_by_ending[ending].append(file)
                break  # Move to the next file after finding a matching ending

    # Collect and sort files by the order of their endings, flatten the dictionary values into a list
    sorted_files = []
    for ending in endings:
        sorted_files.extend(files_by_ending[ending])

    return sorted_files

def move_and_copy_files(source_path, prompt_data_path, prompt_archive_path):
    """
    method detects existing prompt templates in the prompt.data directory and move them to the prompt.archive directory before new prompt templates are loaded in the prompt.data directory. So it is guaranteed, that only one .rules.md, .commands.md and .intention.md exists in the prompt.data directory
    """
    if os.path.exists(source_path):
        file_name = os.path.basename(source_path)
        
        # Check the name ending and extension of source path
        endings = [".commands.md", ".rules.md", ".intention.md"]
        if any(file_name.endswith(ext) for ext in endings):
            for ext in endings:
                if file_name.endswith(ext):
                    # Define glob pattern to match all files with the same ending in the prompt_data_path
                    glob_pattern = os.path.join(prompt_data_path, f"*{ext}")
                    
                    # Move all existing files with the same ending to the prompt_archive_path
                    for existing_file in glob.glob(glob_pattern):
                        archived_file_path = os.path.join(prompt_archive_path, os.path.basename(existing_file))
                        shutil.move(existing_file, archived_file_path)
                        print(f"Moved existing prompt-module: {os.path.basename(existing_file)} to prompt.archive")
                    
                    # Copy the source_path file to the prompt_data_path directory
                    target_path = os.path.join(prompt_data_path, file_name)
                    shutil.copy(source_path, target_path)
                    print(f"Lodaded new prompt-module: {os.path.basename(target_path)}")

        else:
            print(f"File name {file_name} does not end with one of the specified patterns, skipping move and copy.")
    else:
        print(f"WARNING: template {source_path} does not exist.")

def extract_and_load_markdown_files(md_prompt_file_path):
    """
    Extracts markdown files paths based on checked items and constructs proper paths respecting markdown header hierarchy.
    """
    header_stack = []
    path_accumulator = []
    with open(md_prompt_file_path, 'r') as file:
        for line in file:
            if line.strip().startswith('#'):
                level = line.count('#')
                header = line.strip().strip('#').strip()
                # Adjust the stack based on the current header level
                current_depth = len(header_stack)
                if level <= current_depth:
                    header_stack = header_stack[:level-1]
                header_stack.append(header)
            elif '[x]' in line:
                relative_path = line.split(']')[-1].strip()
                full_path = os.path.join('/'.join(header_stack), relative_path)
                path_accumulator.append(full_path)
    return path_accumulator

def create_and_send_custom_prompt(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = f"ara/{sub_directory}/{parameter}.data/prompt.data"
    prompt_file_path_markdown = join(prompt_data_path, f"{classifier}.prompt.md")
    combined_content_markdown = ""
    image_data_list = []

    endings = [".rules.md", ".prompt_givens.md", ".intention.md", ".commands.md"]
    prompt_order = find_files_with_endings(prompt_data_path, endings)

    for file_name in prompt_order:
        md_prompt_file_path = join(prompt_data_path, file_name)
        if file_name.endswith(".prompt_givens.md"):
            combined_content_markdown += "### GIVENS\n\n"
            markdown_items = extract_and_load_markdown_files(md_prompt_file_path)
            for item in markdown_items:
                if item.lower().endswith(('.png', '.jpeg', '.jpg')):
                    with open(item, "rb") as image_file:
                        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                    image_data_list.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})
                    combined_content_markdown += item + "\n"
                    combined_content_markdown += f'![{item}](data:image/png;base64,{base64_image})' + "\n"
                else:
                    combined_content_markdown += item + "\n" + "```\n"
                    combined_content_markdown += get_file_content(item) + "\n"
                    combined_content_markdown += "```\n\n"
                
        else:
            combined_content_markdown += get_file_content(md_prompt_file_path) + "\n\n"

    with open(prompt_file_path_markdown, 'w') as file:
        file.write(combined_content_markdown)

    prompt = read_string_from_file(prompt_file_path_markdown)
    append_headings(classifier, parameter, "prompt")
    write_prompt_result(classifier, parameter, prompt)

    # Create a message list from text and image data
    message_list = [
        {"role": "system", "content": "You are a helpful assistant that can process both text and images."},
        {"role": "user", "content": [
            {"type": "text", "text": combined_content_markdown},
        ] + image_data_list}
    ]

    response = send_prompt_message_list(message_list)

    append_headings(classifier, parameter, "result")
    write_prompt_result(classifier, parameter, response)

def generate_config_prompt_template_file(prompt_data_path, config_prompt_templates_name):
    config_prompt_templates_path = os.path.join(prompt_data_path, config_prompt_templates_name)
    config = ConfigManager.get_config()
    global_prompt_template_path = TemplatePathManager.get_template_base_path_prompt_modules()
    dir_list = ["ara/.araconfig/custom-prompt-modules"] + [f"{os.path.join(global_prompt_template_path,'prompt-modules')}"]
    file_list = ['*.rules.md','*.intention.md', '*.commands.md']

    print(f"used {dir_list} for prompt templates file listing")
    generate_markdown_listing(dir_list, file_list, config_prompt_templates_path)

def generate_config_prompt_givens_file(prompt_data_path, config_prompt_givens_name, artefact_to_mark=None):
    config_prompt_givens_path = os.path.join(prompt_data_path, config_prompt_givens_name)
    config = ConfigManager.get_config()
    dir_list = ["ara"] + [item for ext in config.ext_code_dirs for key, item in ext.items()] + [config.doc_dir] + [config.glossary_dir]

    print(f"used {dir_list} for prompt givens file listing")
    generate_markdown_listing(dir_list, config.ara_prompt_given_list_includes, config_prompt_givens_path)
    
    # If an artefact is specified, mark it with [x]
    if artefact_to_mark:
        print(f"artefact {artefact_to_mark} marked in related config.prompt_givens.md per default")

        # Read the generated file content
        with open(config_prompt_givens_path, 'r') as file:
            markdown_listing = file.readlines()

        updated_listing = []
        for line in markdown_listing:
            # Use a regular expression to match the exact string
            if re.search(r'\b' + re.escape(artefact_to_mark) + r'\b', line):
                line = line.replace("[]", "[x]")
            updated_listing.append(line)

        # Write the updated listing back to the file
        with open(config_prompt_givens_path, 'w') as file:
            file.write("".join(updated_listing))