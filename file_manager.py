import json
import os
import logging

FILE_PATH = os.path.abspath('./games_data.json')
logging.basicConfig(level=logging.ERROR)


class FileManager:
    @staticmethod
    def save(data, file_path=None):
        """Save data to a json file."""
        file_path = file_path or FILE_PATH

        try:
            with open(file_path, 'w') as f:
                json_data = json.dumps(data, indent=4)
                f.write(json_data)
        except Exception as e:
            logging.error(
                f"Unexpected error in save_file: {type(e).__name__}: {e}"
            )

    @staticmethod
    def load(file_path=None):
        """Load data from a json file."""
        file_path = file_path or FILE_PATH
        try:
            with open(file_path, 'r') as f:
                return json.loads(f.read())
        except json.JSONDecodeError:
            logging.error("Wrong data file")
        except Exception as e:
            logging.error(
                f"Unexpected error in get_olds_games {type(e).__name__}"
            )

        return None

    @staticmethod
    def update_from_key(key, data, file_path=None):
        """Update a specific key in the json file with new data."""
        file_path = file_path or FILE_PATH
        try:
            file_data = FileManager.load(file_path=file_path)
            with open(file_path, 'w') as f:
                file_data[key] = data
                json_data = json.dumps(file_data, indent=4)
                f.write(json_data)
        except Exception as e:
            logging.error(
                f"Unexpected error in update: {type(e).__name__}: {e}"
            )


if __name__ == "__main__":
    data = {
        'test1': 'elemento 1',
        'test2': 'elemento 2'
    }

    FileManager.save(data, file_path="test.json")
    data = ["cambie le texto"]
    FileManager.update_from_key("test2", data, file_path="test.json")
