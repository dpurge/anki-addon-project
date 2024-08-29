from aqt import mw

def use_deck(name):
    id = mw.col.decks.id(name)
    mw.col.decks.save()
    mw.col.decks.currentId = id
    return id