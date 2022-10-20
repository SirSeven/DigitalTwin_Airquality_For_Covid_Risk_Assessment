import json

def readJsonFromFile(file_path: str) -> object:
    file = open(file_path)
    file_content = file.read()
    file.close()
    data = json.loads(file_content)
    return data