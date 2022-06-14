"""Basic file dialog functions."""
import os
import json
import easygui


class FileChooser():
    """Functionality for open and save file options."""

    def open_multiple_file_dialog(self, start_directory='resources/shaders'):
        """
        Open multiple files at a time. This is currently only used for shaders.

        :return: Files to be opened
        :rtype: list
        """
        return easygui.fileopenbox("Please Choose Shader Files",
            default=os.path.join(os.getcwd(), start_directory), multiple=True)

    def open_file_dialog(self, start_directory="resources"):
        """
        Open a file and return the path.

        :param start_directory: defaults to resources
        :type start_directory: (str, optional)

        :return: Files to be opened
        :rtype: list
        """
        return easygui.fileopenbox("Please choose a file", default=os.path.join(os.getcwd(), start_directory))

    def save_file_dialog(self, save_dict):
        """
        Save a the current workspace as a json file.

        :param save_dict: Dictionary with save values.
        :type save_dict: dict
        """
        file_path = easygui.filesavebox("Please choose a file", default=os.path.join(os.getcwd(), 'resources/saves'))

        if file_path != '':
            try:
                with open(file_path, 'w') as f:
                    json.dump(save_dict, f, indent=4)
            except Exception:
                pass
