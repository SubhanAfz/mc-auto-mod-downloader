"""
This module is responsible for loading/parsing the links from the text file.
"""
class FileLoader:
    """
    FileLoader class for loading links from a text file.

    Args:
        mod_txt (str): Path to the text file containing the links.
    """
    def __init__(self, mod_txt = "mods.txt"):
        self.mod_txt = mod_txt
        self.ensure_file_exists()

    """
    Ensure the file exists.
    """
    def ensure_file_exists(self):
        try:
            with open(self.mod_txt, "r") as f:
                pass
        except FileNotFoundError:
            open(self.mod_txt, "w").close()

    """
    Load the file and return a list of lines.
    """
    def load_file(self):
        lines = []
        with open(self.mod_txt, "r") as f:
            for line in f.readlines():
                # ignore comments
                if line.startswith("#"):
                    continue
                lines.append(line.strip())
        return lines