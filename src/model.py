from aqt import mw
from anki.consts import MODEL_STD

def use_model(model):
    expected_fields = [field['name'] for field in model['fields']]

    models = mw.col.models
    m = models.by_name(model['name'])

    if not m:
        m = models.new(model['name'])
        m["type"] = MODEL_STD
        m["sortf"] = 0
        for i in expected_fields:
            f = models.new_field(i)
            models.add_field(notetype=m, field=f)
        for i in model['templates']:
            t = models.new_template(i['name'])
            t['qfmt'] = i['qfmt'].read_text()
            t['afmt'] = i['afmt'].read_text()
            models.add_template(m, t)
        models.add(m)

    existing_fields = models.field_names(m)
    for i in existing_fields:
        if not i in expected_fields:
            f = models.new_field(i)
            models.remove_field(notetype=m, field=f)
    for i in expected_fields:
        if not i in existing_fields:
            f = models.new_field(i)
            models.add_field(notetype=m, field=f)

    m["css"] = model['style']['css'].read_text()


    models.save(m)
    return m