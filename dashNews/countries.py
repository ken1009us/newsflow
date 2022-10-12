from config import NEWSAPI_SUPPORTED_COUNTRIES


def get_country_options():
    """Return sorted dropdown options for NewsAPI-supported countries.

    Returns a list of dicts with 'label' (country name) and 'value' (country code)
    suitable for use with dcc.Dropdown.
    """
    options = [
        {"label": name, "value": code}
        for code, name in NEWSAPI_SUPPORTED_COUNTRIES.items()
    ]
    return sorted(options, key=lambda x: x["label"])
