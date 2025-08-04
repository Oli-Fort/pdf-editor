import dearpygui.dearpygui as dpg


def on_resize(sender, app_data):
    width, height = dpg.get_viewport_width(), dpg.get_viewport_height()
    plot_width = max(width - 30, 400)
    plot_height = max(height - 50, 300)
    dpg.configure_item("canvas_window", width=width, height=height)
    dpg.configure_item("pdf_plot", width=plot_width, height=plot_height)

