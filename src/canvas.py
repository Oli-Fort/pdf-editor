import tkinter as tk

import pymupdf
from PIL import ImageTk, Image
import customtkinter as ctk


class DynamicCanvas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_item = None
        self.parent = parent
        self.edit_mode = "normal"
        self.page_load_func = self.load_page
        self.pdf = None
        self.img = None
        self.tkimg = None
        self.scale = 1.0

        self.drag_data = {"x": self.parent.winfo_width(),
                          "y": self.parent.winfo_height(),
                          "points": []}

        self.pen_data = {
            "color": "black",
            "width": 1,
            "rgb_color": (0, 0, 0)
        }

        self.highlighter_data = {
            "color": "red",
            "width": 10,
            "rgb_color": (1, 0, 0)
        }
        super().configure(bg_color="gray10")
        self.canvas = ctk.CTkCanvas(self)
        self.canvas.configure(bg="gray10", borderwidth=0, highlightthickness=0)
        self.v_scrollbar = ctk.CTkScrollbar(master=self, orientation="vertical", command=self.canvas.yview)
        # self.scroll_frame = ctk.CTkFrame(self.canvas)
        # self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.canvas.pack(expand=True, fill="both", side="left")
        self.v_scrollbar.pack(side="right", fill="y")

    def on_resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_pdf(self, pdf=None):
        self.pdf = pdf

        if self.pdf is None:
            self.canvas.delete("all")
        else:
            self.page_load_func()

    def change_current_page(self, event):
        self.canvas.delete("all")

        if self.pdf.current_page is None:
            return

        self.pdf.change_page(event)
        self.load_page()
        self.canvas.update_idletasks()

    def load_page(self, center_x=None, center_y=None):
        page = self.pdf.current_page

        zoom = pymupdf.Matrix(self.scale, self.scale)
        pix = page.get_pixmap(matrix=zoom)

        self.img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        self.tkimg = ImageTk.PhotoImage(self.img)

        self.canvas.delete("all")
        self.image_item = self.canvas.create_image(int(self.parent.winfo_width()/2), int(self.parent.winfo_height()/2), anchor=tk.CENTER, image=self.tkimg)

        self.canvas.tag_bind(self.image_item, "<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.image_item, '<B1-Motion>', self.drag_handler)
        self.canvas.tag_bind(self.image_item, '<ButtonRelease-1>', self.stop_drag)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if center_x and center_y:
            self.canvas.xview_moveto(center_x/pix.width)
            self.canvas.yview_moveto(center_y/pix.height)

    def load_double_page(self):
        if self.pdf.document.page_count == 1:
            return

        left_page = self.pdf.document.load_page(self.pdf.current_page_index)
        left_pix = left_page.get_pixmap()
        left_img = Image.frombytes("RGB", (left_pix.width, left_pix.height), left_pix.samples)

        right_img = None
        if self.pdf.current_page_index + 1 < self.pdf.document.page_count:
            right_page = self.pdf.document.load_page(self.pdf.current_page_index+1)
            right_pix = right_page.get_pixmap()
            right_img = Image.frombytes("RGB", (right_pix.width, right_pix.height), right_pix.samples)

        total_width = left_img.width + (right_img.width if right_img else 0)
        max_height = max(left_img.height, right_img.height if right_img else 0)

        merged_img = Image.new("RGB", (total_width, max_height), "white")
        merged_img.paste(left_img, (0, 0))

        if right_img:
            merged_img.paste(right_img, (left_img.width, 0))

        self.tkimg = ImageTk.PhotoImage(merged_img)
        self.canvas.create_image(600, 400, anchor="center", image=self.tkimg)

    def load_continuous_scroll(self):
        if self.pdf.document.page_count == 1:
            return

        self.pdf.images.clear()

        for page in range(self.pdf.document.page_count):
            page = self.pdf.document.load_page(page)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            img_tk = ImageTk.PhotoImage(img)

            img_it = self.canvas.create_image(int(self.parent.winfo_width()/2), int(self.parent.winfo_height()/2), anchor=tk.CENTER, image=img_it)
            self.pdf.images.append(img_it)

    def zoom(self, event):
        old_scale = self.scale
        factor = 1.2 if event.delta > 0 else 0.8
        self.scale *= factor

        # mouse_x = self.canvas.canvasx(event.x)
        # mouse_y = self.canvas.canvasy(event.y)
        #
        # new_center_x = mouse_x * (self.scale/old_scale)
        # new_center_y = mouse_y * (self.scale/old_scale)

        # self.load_page(new_center_x, new_center_y)
        self.load_page()

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["points"].clear()

    def stop_drag(self, event):
        match self.edit_mode:
            case "draw":
                self.pdf.current_page.draw_polyline(
                    self.drag_data["points"],
                    color=self.pen_data["rgb_color"],
                    width=self.pen_data["width"])
                self.load_page()
            case "highlight":
                self.drag_data["points"].append(self.convert_canvas_to_pdf(event.x, event.y))
                self.pdf.current_page.draw_line(self.drag_data["points"][0],
                                                (self.drag_data["points"][-1][0], self.drag_data["points"][0][1]),
                                                color=self.highlighter_data["rgb_color"],
                                                width=self.highlighter_data["width"],
                                                stroke_opacity=0.5)
                self.load_page()
            case _:
                return

    def dragging(self, event):
        deltax = event.x - self.drag_data.get("x")
        deltay = event.y - self.drag_data.get("y")

        self.canvas.move(self.image_item, deltax, deltay)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drawing(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        self.drag_data["points"].append((self.convert_canvas_to_pdf(event.x, event.y)))

        if len(self.drag_data["points"]) != 1:
            self.canvas.create_line(self.drag_data["x"],
                                    self.drag_data["y"],
                                    x, y,
                                    fill=self.pen_data["color"],
                                    width=self.pen_data["width"])

        # self.drag_data["points"].append((self.convert_canvas_to_pdf(event.x, event.y)))
        self.drag_data["x"] = x
        self.drag_data["y"] = y

    def highlighting(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        #self.canvas.create_line(self.drag_data["x"], self.drag_data["y"], x, y, fill="red", width=10)

        self.drag_data["points"].append((self.convert_canvas_to_pdf(event.x, event.y)))
        self.drag_data["x"] = x
        self.drag_data["y"] = y

    def check_if_within_borders(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if 0 <= x <= self.canvas.winfo_width() and 0 <= y <= self.canvas.winfo_height():
            return True
        return False

    def drag_handler(self, event):
        match self.edit_mode:
            case "normal":
                self.dragging(event)
            case "draw":
                self.drawing(event)
            case "highlight":
                self.highlighting(event)
            case _:
                return

    def change_view_mode(self, mode):
        match mode:
            case "single":
                self.page_load_func = self.load_page
                self.draw_pdf()
            case "double":
                self.page_load_func = self.load_double_page
                self.draw_pdf()
            case "scroll":
                self.page_load_func = self.load_continuous_scroll
                self.draw_pdf()

    def convert_canvas_to_pdf(self, x, y):
        pdf_width, pdf_height = self.pdf.current_page.rect.width, self.pdf.current_page.rect.height

        canvas_x = self.canvas.canvasx(x)
        canvas_y = self.canvas.canvasy(y)

        top_left_x = int(self.parent.winfo_width()/2) - (self.tkimg.width()/2)
        top_left_y = int(self.parent.winfo_height()/2) - (self.tkimg.height()/2)

        x = canvas_x - top_left_x
        y = canvas_y - top_left_y

        x = x / self.scale
        y = y / self.scale

        return x, y






