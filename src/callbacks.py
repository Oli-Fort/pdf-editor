import dearpygui.dearpygui as dpg


def on_resize(sender, app_data):
    width, height = dpg.get_viewport_width(), dpg.get_viewport_height()
    plot_width = max(width - 30, 400)
    plot_height = max(height - 50, 300)
    if dpg.does_item_exist("canvas_window"):
        dpg.configure_item("canvas_window", width=width, height=height)
    if dpg.does_item_exist("pdf_plot"):
        dpg.configure_item("pdf_plot", width=plot_width, height=plot_height)

