from aqt import mw
from aqt.utils import qconnect
from aqt.qt import QInputDialog, QAction

from .project import load_data

def import_project() -> None:
    # cardCount = mw.col.cardCount()
    # showInfo("Card count: %d" % cardCount)
    text, ok = QInputDialog.getText(mw, 'Import project', 'Project file:')
    if ok:
        load_data(str(text))

def setup():
    action = QAction("Import project...", mw)
    qconnect(action.triggered, import_project)
    mw.form.menuTools.addAction(action)