def add_to_registry(init):
    def wrapper(self, *args, **kwargs):
        init(self, *args, **kwargs)
        self.add_to_registry()
    return wrapper
