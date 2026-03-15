from datetime import datetime, timezone
from dash import html


def _format_time(iso_str: str) -> str:
    """Format ISO timestamp to relative or short absolute time."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = now - dt

        secs = diff.total_seconds()
        if secs < 0:
            return dt.strftime("%H:%M")
        elif secs < 3600:
            mins = max(1, int(secs / 60))
            return f"{mins}m ago"
        elif secs < 86400:
            hours = int(secs / 3600)
            return f"{hours}h ago"
        else:
            return dt.strftime("%b %d, %H:%M")
    except Exception:
        return iso_str[:10] if iso_str else ""


def build_timeline(articles: list, lang_data: dict = None) -> html.Div:
    """Build a vertical timeline with expandable article details.

    Each item is a <details> element: clicking expands to show
    article image, full description, source badge, and read-more link.
    """
    if lang_data is None:
        lang_data = {}

    sorted_articles = sorted(
        articles,
        key=lambda a: a.get("publishedAt") or "",
        reverse=True,
    )

    items = []
    for article in sorted_articles:
        title = article.get("title") or lang_data.get("no_description", "No title")
        source = (article.get("source") or {}).get("name", "Unknown")
        url = article.get("url") or "#"
        published = article.get("publishedAt") or ""
        description = article.get("description") or ""
        image_url = article.get("urlToImage")

        time_str = _format_time(published)

        # --- Summary (always visible) ---
        summary_children = [
            html.Div(time_str, className="nf-tl-time"),
            html.Span(title, className="nf-tl-title-text"),
            html.Span(source, className="nf-tl-source"),
        ]

        # --- Detail body (shown when expanded) ---
        # Left: thumbnail image, Right: description + read more
        right_children = []
        if description:
            if len(description) > 200:
                description = description[:200] + "..."
            right_children.append(
                html.P(description, className="nf-tl-desc")
            )

        right_children.append(
            html.A(
                lang_data.get("read_more", "Read More"),
                href=url,
                target="_blank",
                className="nf-tl-readmore",
            )
        )

        detail_inner = []
        if image_url:
            detail_inner.append(
                html.Img(src=image_url, className="nf-tl-thumb")
            )
        detail_inner.append(
            html.Div(right_children, className="nf-tl-detail-body")
        )

        item = html.Details(
            [
                html.Summary(summary_children),
                html.Div(detail_inner, className="nf-tl-detail"),
            ],
            className="nf-tl-item",
        )
        items.append(item)

    return html.Div(items, className="nf-timeline")
