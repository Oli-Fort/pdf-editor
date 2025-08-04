import dearpygui.dearpygui as dpg
from object_registry import object_registry
from decorator import add_to_registry_decorator


class MenuBar():
    @add_to_registry_decorator
    def __init__(self, name):
        self.name = name

        self.create_menu_bar()
    
    def create_menu_bar(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open", callback=lambda: dpg.show_item("file_dialog_id"))
                dpg.add_menu_item(label="Save", callback=lambda: object_registry.get_object("pdf_file").save())
                dpg.add_menu_item(label="Save As", callback=lambda: dpg.show_item("file_dialog_id"))
                dpg.add_menu_item(label="Close")

    def add_to_registry(self):
        object_registry.register_object(self.name, self)