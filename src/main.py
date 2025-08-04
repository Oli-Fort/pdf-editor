
import dearpygui.dearpygui as dpg
from canvas import CanvasWindow
from menubar import MenuBar
from file_dialog import FileDialog
from files import File
from callbacks import on_resize


def main():
    dpg.create_context()
    # with dpg.window(label="Tutorial", pos=(20, 50), width=275, height=225) as win1:
    #     t1 = dpg.add_input_text(default_value="some text")
    #     t2 = dpg.add_input_text(default_value="some text")
    #     with dpg.child_window(height=100):
    #         t3 = dpg.add_input_text(default_value="some text")
    #         dpg.add_input_int()
    #         dpg.add_input_text(default_value="some text")
    # with dpg.window(label="Tutorial", pos=(320, 50), width=275, height=225) as win2:
    #     dpg.add_input_text(default_value="some text")
    #     dpg.add_input_int()
    # with dpg.theme() as global_theme:
    #     with dpg.theme_component(dpg.mvAll):
    #         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core)
    #         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
    #     with dpg.theme_component(dpg.mvInputInt):
    #         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (140, 255, 23), category=dpg.mvThemeCat_Core)
    #         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
    
    # dpg.bind_theme(global_theme)
    # dpg.show_style_editor()
    
    file_dialog = FileDialog("file_dialog")
 
    dpg.create_viewport(title='PDF editor', width=900, height=600)
    dpg.set_viewport_resize_callback(on_resize)

    menu_bar = MenuBar("menu_bar")
    canvas_window = CanvasWindow("canvas_window")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
