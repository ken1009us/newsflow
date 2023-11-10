import pycountry
from typing import Dict


def get_countries() -> Dict[str, Dict[str, str]]:
    """
    Retrieves a dictionary of countries with their two-letter ISO 3166-1 alpha-2 codes
    and names, suitable for use with the News API.

    :return: A dictionary where each key is the full country name and the value is
             another dictionary with 'newsid' (the country's alpha-2 code) and 'name' (the country's name).
    """
    countries = [country.alpha_2.lower() for country in pycountry.countries]
    return {
        country.name: {"newsid": country.alpha_2.lower(), "name": country.name}
        for country in pycountry.countries
        if country.alpha_2.lower() in countries
    }
