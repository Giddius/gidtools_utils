

class InputError(Exception):

    type_dict = {
        'missing': 'Input does not contain the required ',
    }

    def __init__(self, in_message, in_type='missing'):
        self.message = str(in_message)
        self.type = str(self.get_type(in_type))
        self.complete_message = self.type + self.message
        super().__init__(self.complete_message)

    def get_type(self, in_type):
        try:
            _out = self.type_dict[in_type]
        except KeyError:
            _out = "Generic Input Error with "
        return _out
