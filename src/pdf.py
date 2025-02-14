import pymupdf


class PDF:
    def __init__(self, path):
        self.path = path
        self.document = pymupdf.open(self.path, filetype="pdf")
        self.current_page_index = 0
        self.current_page = self.document.load_page(0)

    def change_page(self, event):


        if self.document.page_count == 1:
            return

        if event.keysym == "Up" and self.current_page_index != 0:
            self.current_page_index -= 1

        if event.keysym == "Down" and self.current_page_index < self.document.page_count - 1:
            self.current_page_index += 1

        self.current_page = self.document.load_page(self.current_page_index)



