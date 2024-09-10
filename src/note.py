

from aqt import mw
from aqt.utils import showInfo
from anki.errors import NotFoundError
from anki.notes import Note

from .reader import read_data

def import_notes(deck, model, data, field_type, note_index, merge_fields, field_template):
    col = mw.col
    note_name = model['name']
    for rec, tags in read_data(data, field_type, field_template):
        note = None

        query = f'deck:"{col.decks.name(deck)}" note:"{note_name}"'
        for k in note_index:
            query += f' {k}:'
            v = rec[k]
            if v:
                query += f'"{v}"'

        notes = col.find_notes(query)
        if len(notes):
            note = Note(col=col,id=notes[0])
            note.load()
        else:
            note = col.new_note(model)

        note.tags.extend(tags)
        for k in rec:
            if not k in merge_fields:
                note[k] = rec[k]
                continue

            v = [i.strip() for i in note[k].split(';') if i]
            for i in rec[k].split(';'):
                i = i.strip()
                if i and not i in v:
                    v.append(i)

            note[k] = '; '.join(v)

        if note.id:
            col.update_note(note)
        else:
            col.add_note(note, deck)