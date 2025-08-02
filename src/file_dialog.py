import dearpygui.dearpygui as dpg
from object_registry import object_registry
from decorator import add_to_registry

class FileDialog:
    @add_to_registry
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
        self.selected_file_path = app_data['file_path_name']
        for selection in app_data['selections']:
            self.file_type.append(selection.split('.')[-1])
        if object_registry['file'].path != self.selected_file_path:
            object_registry['file'].load(self.selected_file_path)
        print(f"File selected: {self.selected_file_path}")
        
    def add_extentions(self):
        dpg.add_file_extension(".*", color=(255, 255, 255), custom_text="[All Files]")
        dpg.add_file_extension(".pdf", color=(255, 140, 23), custom_text="[PDF]")
        dpg.add_file_extension(".py", color=(140, 255, 23), custom_text="[Python]")

    def add_to_registry(self):
        object_registry.register_object(self.name, self)
        

