from aqt import mw
from anki.consts import MODEL_STD, MODEL_CLOZE 

def use_model(model):
    expected_fields = [field['name'] for field in model['fields']]

    models = mw.col.models
    m = models.by_name(model['name'])

    if not m:
        m = models.new(model['name'])
        
        if model['kind'] == 'normal':
            m["type"] = MODEL_STD
        elif model['kind'] == 'cloze':
            m["type"] = MODEL_CLOZE
        else:
            raise f"Unsupported model kind: {model['kind']}"

        m["sortf"] = 0
        for i in expected_fields:
            f = models.new_field(i)
            models.add_field(notetype=m, field=f)
        for i in model['templates']:
            t = models.new_template(i['name'])
            if 'qfmt' in i: t['qfmt'] = i['qfmt'].read_text()
            if 'afmt' in i: t['afmt'] = i['afmt'].read_text()
            models.add_template(m, t)
        models.add(m)

    style = model['style'] if 'style' in model else None
    if style:
        if style['css']: m["css"] = style['css'].read_text()
        latex = style['latex'] if 'latex' in style else None
        if latex:
            if 'prefix' in latex: m["latexPre"] = latex['prefix'].read_text()
            if 'postfix' in latex: m["latexPost"] = latex['postfix'].read_text()
            if 'svg' in latex: m["latexsvg"] = latex['svg']

    existing_fields = models.field_names(m)
    for i in existing_fields:
        if not i in expected_fields:
            f = models.new_field(i)
            models.remove_field(notetype=m, field=f)
    for i in expected_fields:
        if not i in existing_fields:
            f = models.new_field(i)
            models.add_field(notetype=m, field=f)

    for f in m['flds']:
        fld = next((x for x in model['fields'] if x['name'] == f['name']), None)
        if 'rtl' in fld: f['rtl'] = fld['rtl']
        if 'description' in fld: f['description'] = fld['description']
        
        font = fld['font'] if 'font' in fld else None
        if font:
            if font['name']: f['font'] = font['name']
            if font['size']: f['size'] = font['size']

    models.save(m)
    return m