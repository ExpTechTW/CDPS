import os


class Plugin():
    def __init__(self) -> None:
        pass

    def get_all_plugins(self, directory_path):
        all_contents = []
        print(os.listdir(directory_path))
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path):
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    all_contents.append(content)
            else:
                print(full_path)
        return all_contents  