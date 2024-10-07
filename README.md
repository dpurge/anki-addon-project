# Project importer for Anki

Anki extension that I use to import my custom project files from [Anki flashcards](https://github.com/dpurge/anki-flashcards).

Install for development:

```cmd
cd %APPDATA%\Anki2\addons21
mklink /D project C:\jdp\src\github.com\dpurge\anki-addon-project\src
```

## Examples

Since project file loads the models (fields, stylesheets, scripts etc.) various kinds of flashcards can be imported from CSV or YAML files.

| Flashcard type  | Question card                               | Answer card                               |
| ---             | ---                                         | ---                                       |
| Question/Answer | ![QA front](./doc/img/qa-front.png)         | ![QA back](./doc/img/qa-back.png)         |
| Cloze           | ![Cloze front](./doc/img/cloze-front.png)   | ![Cloze back](./doc/img/cloze-back.png)   |
| Multiple choice | ![Choice front](./doc/img/choice-front.png) | ![Choice back](./doc/img/choice-back.png) |
