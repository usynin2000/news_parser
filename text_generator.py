def generate_text(title: str, text: str | None, link: str, source: str) -> str:
    sources_with_bad_summary = [
        "www.bloomberg.com",
        "www.forbes.com",
        "www.artforum.com",
    ]
    if source in sources_with_bad_summary or text == "":
        return f"""
    <b><a href='{link}'>{title}</a></b>
    
    {source}
    """
    else:
        return f"""
    <b><a href='{link}'>{title}</a></b>
    
    {text}
    
    {source}
    """
