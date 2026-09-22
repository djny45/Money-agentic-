from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

def add_utm(url: str, *, source: str, medium: str, campaign: str,
            content: str | None = None) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({"utm_source": source, "utm_medium": medium, "utm_campaign": campaign})
    if content:
        query["utm_content"] = content
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
