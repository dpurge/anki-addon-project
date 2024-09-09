import csv
import hashlib

from aqt.utils import showInfo

from .format import format_text, format_markdown

def read_csv(filename):
    with filename.open() as f:
        data = list(csv.DictReader(f, delimiter='\t'))
    return data

reader = {
    '.csv': read_csv
}

format = {
    'text': format_text,
    'markdown': format_markdown
}

def read_data(data, field_type, note_index):
    for i in data:
        f = i['filename']
        t = i['tags']
        ext = f.suffix
        if not ext in reader:
            showInfo(f'File extension "{ext}" not supported: {f}')
            continue
        d = reader[ext](f)
        for r in d:
            # index = []
            for k in r:
                if not k in field_type:
                    showInfo(f'Unexpected field "{k}" in file: {f}')
                    continue
                ft = field_type[k]
                if not ft in format:
                    showInfo(f'Unsupported format "{ft}" for field "{k}" in file: {f}')
                    continue
                # if k in note_index:
                #     index.append(r[k])
                r[k] = format[ft](r[k])
            # id = int(hashlib.md5('\t'.join(index).encode('utf-8')).hexdigest(), 16)
            # id = int.from_bytes(hashlib.md5('\t'.join(index).encode('utf-8')).digest(), 'big')
            # showInfo(str(id))
            # yield id, r
            yield r,t