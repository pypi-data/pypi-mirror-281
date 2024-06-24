import os
from ara_cli.classifier import Classifier
from ara_cli.artefact_link_updater import ArtefactLinkUpdater
from ara_cli.template_manager import DirectoryNavigator
from pathlib import Path
import re

class ArtefactRenamer:
    def __init__(self, file_system=None):
        self.file_system = file_system or os
        self.link_updater = ArtefactLinkUpdater()

    def rename(self, old_name, new_name, classifier):
        # Navigate to the target directory using DirectoryNavigator
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()

        if not new_name:
            raise ValueError("New name must be provided for renaming.")

        if not Classifier.is_valid_classifier(classifier):
            raise ValueError("Invalid classifier provided. Please provide a valid classifier.")

        sub_directory = Classifier.get_sub_directory(classifier)
        old_file_path = self.file_system.path.join(sub_directory, f"{old_name}.{classifier}")
        new_file_path = self.file_system.path.join(sub_directory, f"{new_name}.{classifier}")

        old_dir_path = self.file_system.path.join(sub_directory, f"{old_name}.data")
        new_dir_path = self.file_system.path.join(sub_directory, f"{new_name}.data")

        old_dir_exists = self.file_system.path.exists(old_dir_path)

        # Check if the original file exists
        if not self.file_system.path.exists(old_file_path):
            raise FileNotFoundError(f"The file {old_file_path} does not exist.")

        # Check if the new file name and directory already exist
        if self.file_system.path.exists(new_file_path):
            raise FileExistsError(f"The new file name {new_file_path} already exists.")
        if self.file_system.path.exists(new_dir_path):
            raise FileExistsError(f"The new directory name {new_dir_path} already exists.")

        # Perform the renaming of the file and directory
        self.file_system.rename(old_file_path, new_file_path)
        if old_dir_exists:
            self.file_system.rename(old_dir_path, new_dir_path)
        # TODO: we should be able to remove this next line once ara delete ignores non-existent data folders
        os.makedirs(new_dir_path, exist_ok=True)

        print(f"Renamed file: {old_file_path} to {new_file_path}.")
        print(f"Renamed directory: {old_dir_path} to {new_dir_path}.")


        # Update the title within the artefact file
        self._update_title_in_artefact(new_file_path, new_name, classifier)

        # Update links in related artefact files
        self.link_updater.update_links_in_related_artefacts(old_name, new_name)


  
    def _update_title_in_artefact(self, artefact_path, new_title, classifier):
    # Format the new title: replace underscores with spaces
        formatted_new_title = new_title.replace('_', ' ')

        # Get the artefact title prefix using the classifier
        title_prefix = Classifier.get_artefact_title(classifier.lower())

        if not title_prefix:
            raise ValueError(f"Invalid classifier: {classifier}")

        # Read the file content
        with open(artefact_path, 'r') as file:
            content = file.read()

        # Find the old title line
        old_title_line = next((line for line in content.split('\n') if re.match(f"^{title_prefix}", line)), None)
        if old_title_line is None:
            raise ValueError(f"The artefact file does not contain the title prefix '{title_prefix}'.")

        # Construct the new title line without adding an extra colon
        new_title_line = f"{title_prefix}: {formatted_new_title}"
        # Replace the old title line with the new title line in the content
        new_content = content.replace(old_title_line, new_title_line, 1)

        # Write the updated content back to the file
        with open(artefact_path, 'w') as file:
            file.write(new_content)