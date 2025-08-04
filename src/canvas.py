import dearpygui.dearpygui as dpg
from object_registry import object_registry
from decorator import add_to_registry_decorator
from utils import is_text_file, is_image_file, is_pdf_file, clear_previous_state
from files import PDFFile, TextFile, ImageFile
from toolbar import ToolBar

class CanvasWindow():
    @add_to_registry_decorator
    def __init__(self, name):
        self.name = name
        self.width = dpg.get_viewport_width()
        self.height = dpg.get_viewport_height()
        self.file = None
        self.file_name = ""

        self.create_canvas_window()

    def create_canvas_window(self):
        with dpg.window(label="Canvas",
                        tag="canvas_window",
                        width=self.width,
                        height=self.height,
                        no_close=True,
                        no_collapse=True) as self.canvas_window:
            pass

    def load_file(self, path, file_name):
        if self.file and self.file.path == path:
            self.file = None
        dpg.set_item_label(self.name, file_name)
        dpg.delete_item(self.name, children_only=True)
        clear_previous_state()
        if is_pdf_file(path):
            self.file = PDFFile("pdf_file")
            self.file.load_document(path)
        elif is_text_file(path):
            self.file = TextFile("text_file")
            self.file.load(path)
        elif is_image_file(path):
            self.file = ImageFile("image_file")
            self.file.load(path)
        else:
            raise ValueError("Unsupported file type")

    def save_canvas(self):
        # Placeholder for save functionality
        pass

    def add_to_registry(self):
        object_registry.register_object(self.name, self)

