

from aqt import mw
from aqt.utils import showInfo
# from anki.errors import NotFoundError

from .reader import read_data

def import_notes(deck, model, data, field_type, note_index):
    col = mw.col
    for rec, tags in read_data(data, field_type, note_index):
        # note = None
        # try:
        #     note = col.get_note(id)
        # except NotFoundError:
        #     note = col.new_note()
        note = col.new_note(model)
        note.tags.extend(tags)
        for k in rec:
            note[k] = rec[k]
        col.add_note(note, deck)
        # showInfo(str(note))