class Version:
    def __init__(self, version_str):
        self.version_tuple = tuple(map(int, version_str.split('.')))

    def __lt__(self, other):
        return self.version_tuple < other.version_tuple

    def __gt__(self, other):
        return self.version_tuple > other.version_tuple

    def __eq__(self, other):
        return self.version_tuple == other.version_tuple

    def __str__(self):
        return '.'.join(map(str, self.version_tuple))
