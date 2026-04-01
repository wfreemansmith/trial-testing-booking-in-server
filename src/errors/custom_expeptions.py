class FileProcessingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class UnprocessableEntity(Exception):
    def __init__(self, message: str, data: dict):
        super().__init__(message)
        self.message = message
        self.data = data

class StagedFileNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message