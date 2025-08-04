import dearpygui.dearpygui as dpg
from object_registry import object_registry
from decorator import add_to_registry_decorator

class FileDialog:
    @add_to_registry_decorator
    def __init__(self, name):
        self.name = name
        self.selected_file_path = None
        self.file_type = []

        self.create_file_dialog()


    def create_file_dialog(self):
        
        with dpg.file_dialog(show=False,
                            tag="file_dialog_id",
                            width=500,
                            height=400,
                            callback=self.file_selected):
        
            self.add_extentions()

    def file_selected(self, sender, app_data):
        i = 0
        for k, v in app_data['selections'].items():
            if i == 1:
                break
            self.selected_file_path = v
            self.file_name = k
            i += 1
        object_registry.get_object("canvas_window").load_file(self.selected_file_path, self.file_name)
        
    def add_extentions(self):
        dpg.add_file_extension(".*", color=(255, 255, 255), custom_text="[All Files]")
        dpg.add_file_extension(".pdf", color=(255, 140, 23), custom_text="[PDF]")
        dpg.add_file_extension(".py", color=(140, 255, 23), custom_text="[Python]")

    def add_to_registry(self):
        object_registry.register_object(self.name, self)
        

