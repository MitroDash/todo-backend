import json
import os


class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def __str__(self):
        return self.title

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': []
        }
        for entry in self.entries:
            res['entries'].append(entry.json())
        return res

    @classmethod
    def from_json(cls, value):
        entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            entry.add_entry(cls.from_json(sub_entry))
        return entry

    def save(self, path):
        path = os.path.join(path, f'{self.title}.json')
        with open(path, 'w') as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            file = json.load(f)
        return cls.from_json(file)


def print_with_indent(value, indent):
    print('\t' * indent + str(value))


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)
            with open(os.path.join(self.data_path, entry.title), 'w') as file:
                file.write(entry.title)

    def load(self):
        for name in os.listdir(self.data_path):
            if name.endswith('.json'):
                path = os.path.join(self.data_path, name)
                entry = Entry.load(path)
                self.entries.append(entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)
