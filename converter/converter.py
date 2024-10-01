class Converter:
    # Base converter class that manages all registered converters.
    _registry = {}

    @classmethod
    def register(cls, converter_cls):
        # Register a new converter class with the name as the key.
        cls._registry[converter_cls.__name__] = converter_cls

    @classmethod
    def get_converter(cls, name):
        # Retrieve a registered converter class by its name.
        converter_cls = cls._registry.get(name)
        if converter_cls is not None:
            return converter_cls
        else:
            raise ValueError(f"No converter found for name: {name}")
    
    @staticmethod
    def convert_to_switch(switch_fname, pc_folder_name):
        # Convert gamesave from PC to Switch format.
        raise NotImplementedError("Subclasses should implement this method")

    @staticmethod
    def convert_to_pc(switch_fname, pc_folder_name):
        # Convert gamesave from Switch to PC format.
        raise NotImplementedError("Subclasses should implement this method")