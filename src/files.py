import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

from dataclasses import dataclass

from object_registry import object_registry
from decorator import add_to_registry_decorator
from utils import is_python_file, is_python_keyword, is_c_file, is_c_keyword
from toolbar import ToolBar

class File(ABC):
    @add_to_registry_decorator
    def __init__(self, name):
        self.name = name
        self.path = None
        self.file = None
    
    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod 
    def save(self):
        pass

    @abstractmethod
    def display(self):
        pass

    def add_to_registry(self):
        object_registry.register_object(self.name, self)


class PDFFile(File):
    def __init__(self, name):
        super().__init__(name)
        self.content = None
        self.width = None
        self.height = None
        self.tool_bar = ToolBar("tool_bar")
        self.drawing_enabled = False
        self.initial_pos = None

        self.page_mode = PDFFile.PageMode.SINGLE

        self.draw_data = []
    
    class PageMode:
        SINGLE = "single"
        CONTINUOUS = "continuous"

        @staticmethod
        def switch_mode(current_mode):
            if current_mode == PDFFile.PageMode.SINGLE:
                return PDFFile.PageMode.CONTINUOUS
            else:
                return PDFFile.PageMode.SINGLE


    def load(self, path):
        self.path = path
        images = convert_from_path(self.path)
        image = images[0]
        image = image.convert("RGBA")
        self.width, self.height = image.size
        image_data = np.asarray(image).astype(np.float32) / 255.0
        flat_image_data = image_data.flatten().tolist()

        self.content = flat_image_data
        self.display()

    def save(self):
        pass

    def display(self):
        if dpg.does_item_exist("pdf_plot"):
            dpg.delete_item("pdf_plot")
        if dpg.does_item_exist("pdf_texture"):
            dpg.delete_item("pdf_texture")
        
        window_width = dpg.get_viewport_width()
        window_height = dpg.get_viewport_height()
        
        toolbar_height = 60 
        margin = 20
        plot_width = max(window_width - margin, 400)
        plot_height = max(window_height - toolbar_height - margin, 300)
        
        pdf_aspect = self.width / self.height
        plot_aspect = plot_width / plot_height
        
        if pdf_aspect > plot_aspect:
            display_width = self.width
            display_height = self.width / plot_aspect
        else:
            display_height = self.height
            display_width = self.height * plot_aspect
        
        with dpg.texture_registry():
            dpg.add_static_texture(
                width=self.width, 
                height=self.height, 
                default_value=self.content, 
                tag="pdf_texture")
        
        with dpg.plot(
            height=plot_height,
            width=plot_width,
            parent="canvas_window",
            tag="pdf_plot",
            no_title=True,
            equal_aspects=True) as plot:
            
            x_axis = dpg.add_plot_axis(
                dpg.mvXAxis, 
                label="X",
                no_tick_labels=True,
                no_tick_marks=True,
                no_gridlines=True,
                no_label=True)
            
            y_axis = dpg.add_plot_axis(
                dpg.mvYAxis, 
                label="Y",
                no_tick_labels=True,
                no_tick_marks=True,
                no_gridlines=True,
                no_label=True)
            
            dpg.add_image_series(
                "pdf_texture", 
                [0, 0],                
                [self.width, self.height],
                parent=y_axis)
            
        plot_pos = dpg.get_item_pos("pdf_plot")
        with dpg.group(tag="tool_bar", parent="canvas_window"):
            # dpg.add_button(label="Text", pos=(plot_pos[0] + 10, plot_pos[1] + 60), width=50, height=50, callback=add_textbox_handler)
            dpg.add_button(label="Draw", pos=(plot_pos[0] + 10, plot_pos[1] + 120), width=50, height=50, callback=self.draw_handler)
            dpg.add_button(label="Single Page", pos=(plot_pos[0] + 10, plot_pos[1] + 180), width=50, height=50, callback=self.toggle_page_mode_handler)
            dpg.add_button(label="Continuous Scroll", pos=(plot_pos[0] + 10, plot_pos[1] + 240), width=100, height=50, callback=self.toggle_page_mode_handler)

    def draw_handler(self, sender, app_data):
        if not self.drawing_enabled:
            self.enable_drawing(sender, app_data)
        else:
            self.disable_drawing(sender, app_data)
    
    def enable_drawing(self, sender, app_data):
        self.drawing_enabled = True
        self.initial_pos = dpg.get_plot_mouse_pos()
        dpg.configure_item("pdf_plot", no_inputs=True)
        print(dpg.get_plot_mouse_pos())

        if not dpg.does_item_exist("draw_event_handler"):
            with dpg.handler_registry(tag="draw_event_handler") as handler:
                dpg.add_mouse_drag_handler(callback=self.draw)
                dpg.add_mouse_release_handler(callback=self.disable_drawing)

    
    def disable_drawing(self, sender, app_data):
        self.drawing_enabled = False
        self.initial_pos = None
        dpg.configure_item("pdf_plot", no_inputs=False)
        self.draw_data.clear()
        if dpg.does_item_exist("draw_event_handler"):
            dpg.delete_item("draw_event_handler")
    
    def draw(self, sender, app_data):
        
        self.draw_data.append([self.initial_pos[0]+app_data[1], self.initial_pos[1]+app_data[2]])
        dpg.draw_polyline(self.draw_data, color=(255, 0, 0), thickness=2, parent="pdf_plot")

    def toggle_page_mode(self, sender, app_data):
        


class TextFile(File):
    def __init__(self, name):
        super().__init__(name)
        self.content = None
        self.word_type_colors = self.WordTypeColor()

    @dataclass
    class WordTypeColor:
        text: tuple = (255, 255, 255)
        keyword: tuple = (255, 0, 0)
        comment: tuple = (0, 255, 0)
        name: tuple = (0, 0, 255)

    def load(self, path):
        self.path = path
        with open(self.path, 'r') as file:
            self.content = file.read()
        self.display()
    
    def save(self):
        pass

    def display(self):
        if (dpg.does_item_exist("file_content_box")):
            dpg.delete_item("file_content_box")

        dpg.add_input_text(
                tag="file_content_box",
                multiline=True,
                default_value=self.content,
                width=dpg.get_viewport_width(),
                height=dpg.get_viewport_height(),
                parent="canvas_window")

        # with dpg.child_window(tag="file_content_box",
        #                     width=dpg.get_viewport_width(),
        #                     height=dpg.get_viewport_height(),
        #                     auto_resize_x=True,
        #                     auto_resize_y=True,
        #                     horizontal_scrollbar=True,
        #                     parent="canvas_window"):
        #     for line in self.content:
        #         with dpg.group(horizontal=True):
        #             words = line.split(" ")
        #             words_map = self.text_coloring_handler(words)
        #             for i, word in enumerate(words):
        #                 if word.endswith('\n'):
        #                     word = word.rstrip('\n')
                        
        #                 color = words_map.get(word)
                    
        #                 dpg.add_text(word, color=color, wrap=False, bullet=False, indent=0) 
        #             dpg.add_text('\n')
    
    def text_coloring_handler(self, words):
        words_map = {} 
        if is_python_file(self.path):
            keyword_func = is_python_keyword
            function_token = "def"
            comment_token = "#"
        elif is_c_file(self.path):
            keyword_func = is_c_keyword
            comment_token = "//"

        for i, word in enumerate(words):
            global_color = None
            if word.endswith('\n'):
                word = word.rstrip('\n')

            if global_color:
                words_map[word] = global_color
                continue

            if keyword_func(word):
                words_map[word] = self.word_type_colors.keyword
            elif word.startswith(comment_token):
                words_map[word] = self.word_type_colors.comment
                global_color = self.word_type_colors.comment
            elif i > 1 and (words[i-1] == function_token or words[i-1] == "class"):
                words_map[word] = self.word_type_colors.name
            else:
                words_map[word] = self.word_type_colors.text

        return words_map
    


class ImageFile(File):
    def __init__(self, name):
        super().__init__(name)
        self.width = None
        self.height = None
        self.channels = None
        self.data = None
    
    def load(self, path):
        self.path = path
        self.width, self.height, self.channels, self.data = dpg.load_image(self.path)
        self.display()

    def save(self):
        pass

    def display(self):
        if (dpg.does_item_exist("image_texture")):
            dpg.delete_item("image_texture")

        with dpg.texture_registry():
            dpg.add_static_texture(width=self.width, height=self.height, default_value=self.data, tag="image_texture")

        dpg.add_image("image_texture", width=dpg.get_viewport_width(), height=dpg.get_viewport_height(), parent="canvas_window")

    