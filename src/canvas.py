import dearpygui.dearpygui as dpg
from object_registry import object_registry
from decorator import add_to_registry

class CanvasWindow():
    @add_to_registry
    def __init__(self, name):
        self.name = name
        self.width = dpg.get_viewport_width()
        self.height = dpg.get_viewport_height()

        self.create_canvas_window()
    
    def create_canvas_window(self):
        with dpg.window(label="PDF canvas",
                        width=self.width,
                        height=self.height,
                        no_close=True,
                        no_collapse=True) as self.canvas_window:
            dpg.add_text("PDF Canvas Area")
    
    def save_canvas(self):
        # Placeholder for save functionality
        pass

    def add_to_registry(self):
        object_registry.register_object(self.name, self)

