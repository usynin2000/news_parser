def generate_text(title: str, text: str | None, link: str, source: str) -> str:
    sources_with_bad_summary = [
        "www.bloomberg.com",
        "www.forbes.com",
        "www.artforum.com",
        "www.reddit.com",
        "www.ycombinator.com",
        "www.theguardian.com",
        "www.arstechnica.com",
        "www.ft.com",
        "www.informationisbeautiful.com",
        "www.visualistan.com",
        "www.infographicsarchive.com",
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
