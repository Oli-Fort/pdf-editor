class ObjectRegistry:
    _services = {}

    @classmethod
    def register_object(cls, name, obj):
        cls._services[name] = obj

    @classmethod
    def get_object(cls, name):
        return cls._services.get(name)

object_registry = ObjectRegistry()