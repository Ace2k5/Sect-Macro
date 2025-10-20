from backend import clicks
'''
important:
self.template_matching only requires the template_filename.
'''


class summerEvent():
    def __init__(self, game_config, prefilled_temp_match, handle_location):
        self.game_config = game_config
        self.template_matching = prefilled_temp_match
        self.handle_location = handle_location
        self.location = None

    def initialGameClick(self):
        print("Test")
    def gameModeClick(self):
        print("test")
    
class infinite():
    def __init__(self, game_config, prefilled_temp_match, handle_location):
        self.game_config = game_config
        self.template_matching = prefilled_temp_match
        self.handle_location = handle_location
        self.location = None

    def initialGameClick(self):
        print("Test")
    
    def gameModeClick(self):
        print("test")