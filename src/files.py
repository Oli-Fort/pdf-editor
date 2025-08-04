import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import time
import fitz

from dataclasses import dataclass

from object_registry import object_registry
from decorator import add_to_registry_decorator
from utils import is_python_file, is_python_keyword, is_c_file, is_c_keyword, get_image_array
from toolbar import ToolBar

class File(ABC):
    @add_to_registry_decorator
    def __init__(self, name):
        self.name = name
        self.path = None
        self.file = None
    

    @abstractmethod 
    def save(self):
        pass

    @abstractmethod
    def create_display(self):
        pass

    def add_to_registry(self):
        object_registry.register_object(self.name, self)


class PDFFile(File):
    def __init__(self, name):
        super().__init__(name)
        self.content = None
        self.width = None
        self.height = None
        self.drawing_enabled = False
        
        self.page_mode = PDFFile.PageMode.SINGLE
        self.document = None
        self.current_page = None
        self.current_page_index = 0
        self.last_page_index = 0
        self.num_pages = 0
        
        self.pages = []
        self.draw_thickness = 2
        self.draw_data = []

        self.create_display()
    
    class PageMode:
        SINGLE = "single"
        CONTINUOUS = "continuous"

        @staticmethod
        def switch_mode(current_mode):
            if current_mode == PDFFile.PageMode.SINGLE:
                return PDFFile.PageMode.CONTINUOUS
            else:
                return PDFFile.PageMode.SINGLE
            
    class Page:
        def __init__(self, index, page):
            self.index = index
            self.page = page
            self.pixmap = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), colorspace=fitz.csRGB, alpha=False)
            self.height = self.pixmap.height
            self.width = self.pixmap.width
            self.draw_data = []
            
    def load_document(self, path):
        if self.document:
            self.document.close()
            self.pages.clear()

        self.path = path
        self.document = fitz.open(self.path)
        self.num_pages = self.document.page_count
        self.last_page_index = self.num_pages - 1
        
        zoom = 2.0, 2.0
        mat = fitz.Matrix(*zoom)

        for i, page in enumerate(self.document.pages()):
            self.pages.append(self.Page(i, self.document.load_page(i)))
        
        self.current_page = self.pages[self.current_page_index]
        
        self.load_page()

    def load_page(self):
        self.content = get_image_array(self.current_page.pixmap)
    
        if dpg.does_item_exist("pdf_image_series"):
            dpg.delete_item("pdf_image_series")
        if dpg.does_item_exist("pdf_texture"):
            dpg.delete_item("pdf_texture")
            
        dpg.add_static_texture(
            width=self.current_page.width,
            height=self.current_page.height,
            default_value=self.content,
            tag="pdf_texture",
            parent="texture_registry")

        dpg.add_image_series(
            "pdf_texture",
            [0, 0],
            [self.current_page.width, self.current_page.height],
            parent="y_axis",
            tag="pdf_image_series")

    def save(self):
        try:
            self.document.save(self.path, incremental=True)
        except Exception as e:
            new_path = self.path.replace(".pdf", "_edited.pdf")
            self.document.save(new_path)
    

    def create_display(self):
        window_width = dpg.get_viewport_width()
        window_height = dpg.get_viewport_height()
        
        toolbar_height = 60 
        margin = 20
        plot_width = max(window_width - margin, 400)
        plot_height = max(window_height - toolbar_height - margin, 300)
    
        with dpg.texture_registry(tag="texture_registry"):
            pass
                
        if not dpg.does_item_exist("pdf_plot"):
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
                    no_label=True,
                    tag="x_axis")
                
                y_axis = dpg.add_plot_axis(
                    dpg.mvYAxis, 
                    label="Y",
                    no_tick_labels=True,
                    no_tick_marks=True,
                    no_gridlines=True,
                    no_label=True,
                    tag="y_axis")

        plot_pos = dpg.get_item_pos("pdf_plot")
            
        if not dpg.does_item_exist("tool_bar"):
            with dpg.group(tag="tool_bar", parent="canvas_window"):
                # dpg.add_button(label="Text", pos=(plot_pos[0] + 10, plot_pos[1] + 60), width=50, height=50, callback=add_textbox_handler)
                dpg.add_button(label="Draw", pos=(plot_pos[0] + 10, plot_pos[1] + 120), width=50, height=50, callback=self.draw_handler)
                # dpg.add_button(label="Single Page", pos=(plot_pos[0] + 10, plot_pos[1] + 180), width=50, height=50, callback=self.toggle_page_mode_handler)
                # dpg.add_button(label="Continuous Scroll", pos=(plot_pos[0] + 10, plot_pos[1] + 240), width=100, height=50, callback=self.toggle_page_mode_handler)
        
        if not dpg.does_item_exist("change_page_handler"):
            with dpg.handler_registry(tag="change_page_handler"):
                dpg.add_key_press_handler(
                    dpg.mvKey_Right, 
                    callback=lambda s, a: self.change_page(1))
                dpg.add_key_press_handler(
                    dpg.mvKey_Left, 
                    callback=lambda s, a: self.change_page(-1))
            

    def draw_handler(self, sender, app_data):
        if not self.drawing_enabled:
            self.enable_drawing(sender, app_data)
        else:
            self.disable_drawing(sender, app_data)
    
    def enable_drawing(self, sender, app_data):
        if not self.drawing_enabled:
            self.drawing_enabled = True
            dpg.configure_item("pdf_plot", pan_button=2)
            if not dpg.does_item_exist("draw_event_handler"):
                with dpg.handler_registry(tag="draw_event_handler") as handler:
                    dpg.add_mouse_drag_handler(callback=self.draw)
                    dpg.add_mouse_release_handler(callback=self.clear_draw_data)
                    dpg.add_mouse_down_handler(callback=self.enable_drawing)
        elif app_data[0] == 0:
            mouse_pos = dpg.get_plot_mouse_pos() 
            self.draw_data.append([mouse_pos[0], mouse_pos[1]])
            dpg.draw_polyline(self.draw_data, color=(255, 0, 0), thickness=2, parent="pdf_plot")
            
                    
    def disable_drawing(self, sender, app_data):
        self.drawing_enabled = False
        self.initial_pos = None
        self.draw_data.clear()
        dpg.configure_item("pdf_plot", pan_button=dpg.mvMouseButton_Left)
        if dpg.does_item_exist("draw_event_handler"):
            dpg.delete_item("draw_event_handler")
    
    def draw(self, sender, app_data):
        if dpg.is_item_hovered("pdf_plot") and self.drawing_enabled and app_data[0] == 0:
            image_width = self.current_page.width
            image_height = self.current_page.height

            x_min, x_max = dpg.get_axis_limits("x_axis")
            y_min, y_max = dpg.get_axis_limits("y_axis")
            visible_width = x_max - x_min
            visible_height = y_max - y_min
            zoom_x = image_width / visible_width
            zoom_y = image_height / visible_height
            zoom_level = (zoom_x + zoom_y) / 2
                        
            mouse_pos = dpg.get_plot_mouse_pos() 
            self.draw_data.append([mouse_pos[0], mouse_pos[1]])
            print(f"Exists before: ", dpg.does_item_exist("draw_polyline"))
            polyline_id = dpg.get_item_configuration("draw_polyline") if dpg.does_item_exist("draw_polyline") else None
            print("Polyline ID before delete:", polyline_id)
            dpg.draw_polyline(self.draw_data, color=(255, 0, 0), thickness=zoom_level*self.draw_thickness, parent="pdf_plot", tag="draw_polyline")
             
    def clear_draw_data(self, sender, app_data):
        if self.drawing_enabled:
            self.save_polyline() 
            self.draw_data.clear()
            
    def save_polyline(self):
        if self.draw_data:
            annot = self.current_page.page.add_polyline_annot(self.draw_data)
            annot.set_colors((1, 0, 0, 1))
            annot.set_border(width=self.draw_thickness)
            annot.update()

            self.draw_data.clear()
            if dpg.does_item_exist("draw_polyline"):
                dpg.delete_item("draw_polyline")
            
    def toggle_page_mode(self, sender, app_data):
        pass

    def change_page(self, direction):
        if direction == 1 and self.current_page_index < self.last_page_index:
            self.current_page_index += 1
            self.current_page = self.pages[self.current_page_index]
            self.load_page()
        elif direction == -1 and self.current_page_index > 0:
            self.current_page_index -= 1
            self.current_page = self.pages[self.current_page_index]
            self.load_page()

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

    def create_display(self):
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

    def create_display(self):
        if (dpg.does_item_exist("image_texture")):
            dpg.delete_item("image_texture")

        with dpg.texture_registry():
            dpg.add_static_texture(width=self.width, height=self.height, default_value=self.data, tag="image_texture")

        dpg.add_image("image_texture", width=dpg.get_viewport_width(), height=dpg.get_viewport_height(), parent="canvas_window")

    