from .vendor.markdown import markdown

def format_text(text):
    return text

def format_markdown(text):
    if not text: return ''
    return markdown(text)
