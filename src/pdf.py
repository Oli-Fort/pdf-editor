from pdf2image import convert_from_path


class PDF:
    def __init__(self, path):
        self.path = path
        self.data = None 
        self.current_page_index = 0
        self.current_page = self.document.load_page(0)
        self.images = []

    def load(self):
        self.data = convert_from_path(self.path)

    def change_page(self, event):

        if self.document.page_count == 1:
            return

        if event.keysym == "Up" and self.current_page_index != 0:
            self.current_page_index -= 1

        if event.keysym == "Down" and self.current_page_index < self.document.page_count - 1:
            self.current_page_index += 1

        self.current_page = self.document.load_page(self.current_page_index)

    def save(self, path=None):
        if not path:
            self.document.save(self.path)
        else:
            self.document.save(path)
