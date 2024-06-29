import os
from functools import lru_cache
from ara_cli.classifier import Classifier
from ara_cli.file_classifier import FileClassifier
from ara_cli.template_manager import DirectoryNavigator
from pathlib import Path
from shutil import rmtree, copyfile

class ArtefactCreator:

    def __init__(self, file_system=None):
        self.file_system = file_system or os

    @lru_cache(maxsize=None)
    def read_template_content(self, template_file_path):
        with open(template_file_path, "r") as template_file:
            return template_file.read()

    def create_artefact(self, dir_path, template_path, classifier):
        if not template_path:
            raise ValueError("template_path must not be None or empty!")

        if not classifier:
            raise ValueError("classifier must not be None or empty!")

        # Standard exploration artefact
        self._copy_template_file(dir_path, template_path, f"template.{classifier}.exploration.md", f"{classifier}.exploration.md")

        # Additional exploration artefact for 'feature' classifier
        if classifier == 'feature':
            self._copy_template_file(dir_path, template_path, "template.steps.exploration.md", "steps.exploration.md")

    def _copy_template_file(self, dir_path, template_path, source_name, dest_name):
        source = Path(template_path) / source_name
        destination = Path(dir_path) / dest_name

        if not source.exists():
            print("[ERROR] Source file does not exist!")
            raise FileNotFoundError(f"Source file {source} not found!")

        if not destination.parent.exists():
            print("[ERROR] Destination directory does not exist!")
            raise NotADirectoryError(f"Destination directory {destination.parent} does not exist!")

        copyfile(source, destination)

    def create_file(self, file_path, template_path=None, classifier=None, filename=None):
        if template_path and classifier:
            template_file_path = self.file_system.path.join(template_path, f"template.{classifier}")
            if self.file_system.path.exists(template_file_path):
                template_content = self.read_template_content(template_file_path)
                formatted_filename = filename.replace("-", " ").replace("_", " ")
                template_content = template_content.replace("<descriptive title>", formatted_filename)

                with open(file_path, "w") as file:
                    file.write(template_content)
            else:
                with open(file_path, "w") as file:
                    pass
        else:
            with open(file_path, "w") as file:
                pass

    def create_directory(self, dir_path):
        self.file_system.makedirs(dir_path, exist_ok=True)

    def template_exists(self, template_path, template_name):
        if not template_path:
            return False

        full_path = self.file_system.path.join(template_path, template_name)

        if not self.file_system.path.isfile(full_path):
            print(f"Template file '{template_name}' not found at: {full_path}")
            return False

        return True

    def run(self, filename, classifier, template_path=None):
        # make sure this function is always called from the ara top level directory
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()

        if not Classifier.is_valid_classifier(classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            return

        sub_directory = Classifier.get_sub_directory(classifier)
        file_path = self.file_system.path.join(sub_directory, f"{filename}.{classifier}")
        dir_path = self.file_system.path.join(sub_directory, f"{filename}.data")

        # Check for existing files and directories once at the beginning
        file_exists = self.file_system.path.exists(file_path)
        dir_exists = self.file_system.path.exists(dir_path)

        if file_exists or dir_exists:
            user_choice = input("File or directory already exists. Do you want to overwrite the existing file and directory? (Y/N): ")
            if user_choice.lower() != "y":
                print("No changes were made to the existing file and directory.")
                return

        template_name = f"template.{classifier}"
        if template_path and not self.template_exists(template_path, template_name):
            print(f"Template file '{template_name}' not found in the specified template path.")
            return

        # Create file and directory if they do not exist
        self.create_file(file_path, template_path, classifier, filename)
        if not dir_exists:
            self.create_directory(dir_path)
        self.create_artefact(dir_path, template_path, classifier)

        print(f"Created file: {file_path}")
        print(f"Created directory: {dir_path}")
        print(f"Created artefact exploration: {dir_path}/{classifier}.exploration.md")