import os
import random
import base64
from io import BytesIO
from dash import html

_PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

_CJK_FONT_PATHS = [
    # Bundled (downloaded on Render during build)
    os.path.join(_PROJECT_ROOT, "assets", "fonts", "NotoSansCJK.otf"),
    # macOS
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    # Linux
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]


def _find_cjk_font():
    for p in _CJK_FONT_PATHS:
        if os.path.exists(p):
            return p
    return None


def _nf_color_func(word, font_size, position, orientation, **kwargs):
    """Color function matching the dark theme — blues with occasional teal."""
    colors = [
        "#6b9fd4", "#5889bb", "#7db3e0",
        "#8abde6", "#4a7ab0", "#93c5eb",
        "#5fb8c2", "#78cdd6",
    ]
    return random.choice(colors)


def generate_wordcloud_image(articles: list) -> object:
    """Generate a word cloud PNG from article titles.

    Returns:
        A base64 data URI string, or None if no text.
    """
    try:
        from wordcloud import WordCloud
    except ImportError:
        return None

    titles = [a.get("title", "") for a in articles if a.get("title")]
    text = " ".join(titles)

    if not text.strip():
        return None

    font = _find_cjk_font()
    wc = WordCloud(
        width=900,
        height=240,
        background_color="#242426",
        color_func=_nf_color_func,
        font_path=font,
        max_words=40,
        margin=12,
        prefer_horizontal=0.75,
        relative_scaling=0.5,
        min_font_size=10,
    )
    wc.generate(text)

    img = wc.to_image()
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()


def build_wordcloud_component(articles: list):
    """Build a Dash component containing the word cloud image."""
    img_data = generate_wordcloud_image(articles)
    if not img_data:
        return None

    return html.Div(
        html.Img(
            src=img_data,
            style={
                "width": "100%",
                "borderRadius": "6px",
                "display": "block",
            },
        ),
        className="nf-wordcloud",
    )
