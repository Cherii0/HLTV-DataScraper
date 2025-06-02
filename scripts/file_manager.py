from json import dump

class FileManager:

    @staticmethod
    def write_to_txt_file(*, file_path : str, data : list) -> None:
        with open(file = file_path, mode = "w", encoding="UTF-8") as file:
            for line in data:
                file.write(line + "\n")
        return None

    @staticmethod
    def write_to_json_file(*, file_path : str, data : dict) -> None:
        file_name, file_extension = file_path.split(".")
        if  file_extension != "json":
            file_path = file_name + ".json"
        with open(file = file_path, mode = "w", encoding="UTF-8") as file:
            for line in data:
                dump(data, file)
        return None
