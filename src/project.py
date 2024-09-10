from pathlib import Path
from string import Template

from .vendor import load_yaml, SafeYamlLoader
from .deck import use_deck
from .model import use_model
from .note import import_notes

from aqt.utils import showInfo

def get_project(filename):
    project = None

    project_file = Path(filename)
    if not project_file.is_file():
        showInfo(f'Project does not exist: {project_file}')
        return None

    with open(filename, 'r') as f:
        try:
            project = load_yaml(f, Loader=SafeYamlLoader)
        except Exception as e:
            showInfo(f'Could not parse project file: {e}')
            return None
        
    basedir = project_file.parent

    project['model']['style']['css'] = basedir / project['model']['style']['css']
    project['model']['style']['latex']['prefix'] = basedir / project['model']['style']['latex']['prefix']
    project['model']['style']['latex']['postfix'] = basedir / project['model']['style']['latex']['postfix']

    for i in project['model']['templates']:
        i['qfmt'] = basedir / i['qfmt']
        i['afmt'] = basedir / i['afmt']

    for i in project['model']['fields']:
        i['template'] = basedir / i['template']

    for i in project['data']:
        i['filename'] = basedir / i['filename']

    return project

def load_data(filename):
    project = get_project(filename)
    deck_id = use_deck(project['deck']['name'])
    model = use_model(project['model'])

    field_type = {i['name']: i['format'] for i in project['model']['fields']}
    note_index = [i['name'] for i in project['model']['fields'] if 'index' in i and i['index']]
    merge_fields = [i['name'] for i in project['model']['fields'] if 'merge' in i and i['merge']]
    field_template = {i['name']: Template(i['template'].read_text()) for i in project['model']['fields']}

    if project:
        import_notes(
            deck = deck_id,
            model = model,
            data = project['data'],
            field_type = field_type,
            note_index = note_index,
            merge_fields = merge_fields,
            field_template = field_template)
        showInfo(f"Loaded deck: {project['deck']['name']}")