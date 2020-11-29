

class GidfileBaseError(Exception):
    pass


# class GidUnclearPathSepError(GidfileBaseError):
#     def __init__(self, path):
#         self.path = path
#         self.message = f"Unable to determine the path seperator for path '{self.path}'"
#         super().__init__(self.message)
