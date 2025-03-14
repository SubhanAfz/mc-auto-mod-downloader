from downloader.fileloader import FileLoader
import pytest

def test_load_file():
    file_loader = FileLoader("test/test_mods.txt")
    assert file_loader.load_file() == ["hi"]