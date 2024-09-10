import csv
import hashlib

from aqt.utils import showInfo

from .vendor import load_yaml, SafeYamlLoader

from .format import format_text, format_markdown

def read_csv(filename):
    with filename.open() as f:
        data = list(csv.DictReader(f, delimiter='\t'))
    return data

def read_yaml(filename):
    with filename.open() as f:
        data = load_yaml(filename, Loader=SafeYamlLoader)
    return data

reader = {
    '.csv': read_csv,
    '.yml': read_yaml
}

format = {
    'text': format_text,
    'markdown': format_markdown
}

def read_data(data, field_type, field_template):
    for i in data:
        f = i['filename']
        t = i['tags']
        ext = f.suffix
        if not ext in reader:
            showInfo(f'File extension "{ext}" not supported: {f}')
            continue
        d = reader[ext](f)
        for r in d:
            for k in r:
                if not k in field_type:
                    showInfo(f'Unexpected field "{k}" in file: {f}')
                    continue
                ft = field_type[k]
                if not ft in format:
                    showInfo(f'Unsupported format "{ft}" for field "{k}" in file: {f}')
                    continue
                r[k] = format[ft](r[k])
                r[k] = field_template[k].substitute(r)
            yield r,t