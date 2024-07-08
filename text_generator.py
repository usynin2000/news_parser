def generate_text(title: str, text: str | None, link: str, source: str) -> str:
    sources_with_bad_summary = [
        "www.bloomberg.com",
        "www.forbes.com",
        "www.artforum.com",
        "www.reddit.com (Technology)",
        "www.reddit.com (Tech)",
        "www.reddit.com (StartUp)",
        "www.reddit.com (Programming)",
        "www.reddit.com (Webdev)",
        "www.reddit.com (AI)",
        "www.reddit.com (TechNews)",
        "www.reddit.com (Cyberpunk)",
        "www.reddit.com (Learn Programming)",
        "www.reddit.com (Software)",
        "www.ycombinator.com",
        "www.theguardian.com",
        "www.theguardian.com (Art)",
        "www.arstechnica.com",
        "www.ft.com",
        "www.informationisbeautiful.com",
        "www.visualistan.com",
        "www.infographicsarchive.com",
        "www.bbc.co.uk",
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
