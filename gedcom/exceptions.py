class FileAlreadyExistsError(Exception):
    def __init__(self, filename):
        message = f"File '{filename}' already exists"

        super().__init__(message)
