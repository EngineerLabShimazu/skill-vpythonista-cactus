class Cactus:
    def __init__(self, height=0):
        self.height = height

    def get_height(self, handler_input):
        attributes = handler_input.attributes_manager.persistent_attributes
        if isinstance(attributes, dict):
            self.height = attributes.get('height', 0)
        pass
