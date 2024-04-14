import json


def import_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def export_to_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)


def import_from_txt(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def export_to_txt(filename, data):
    with open(filename, 'w') as f:
        f.writelines(data)
