
def generate_text(title: str, text: str | None, link: str, source: str) -> str:
    return f"""
{title}

{text}

{link}

{source}
"""
