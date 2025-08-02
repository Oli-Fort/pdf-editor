import dearpygui.dearpygui as dpg
from decorator import add_to_registry
from utils import is_text_file, is_image_file

class File:
    @add_to_registry
    def __init__(self, path):
        self.path = path
        self.file_type = path.split('.')[-1] if '.' in path else None
    
    def load(self, path):
        self.path = path
        if is_text_file(path):
            self.load_text_file(path)
        elif is_image_file(path):
            self.load_image_file(path)
        else:
            print(f"Unsupported file type: {self.file_type}")

    def load_text_file(self, path):
        pass

    def load_image_file(self, path):
        pass
    
    def save(self):
        pass
    

    