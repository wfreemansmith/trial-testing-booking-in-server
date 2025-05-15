from config import FILES_DOT_COM_API_KEY
import files_sdk

class FileHandler():
    def __init__(self):
        files_sdk.set_api_key(FILES_DOT_COM_API_KEY)

    # helper functions
    ## REWRITE so this accepts a file not a local path
    def upload_file(self, local_path: str, destination: str) -> None:
        """Uploads a file to Files.com to given file path"""
        try:
            files_sdk.upload_file(local_path, destination)
        except Exception as e:
            print(f"Error uploading file: {e}")
            # handle an exception, raise here