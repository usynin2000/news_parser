
def generate_text(title: str, text: str, link: str, source:str) -> str:
    return f"""
<b><a href='{link}'>{title}</a></b>

{text}

{source}
"""
