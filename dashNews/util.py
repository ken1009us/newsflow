import pycountry


def get_countries():
    countries = [country.alpha_2.lower() for country in pycountry.countries]
    return {
        country.name: {"newsid": country.alpha_2.lower(), "name": country.name}
        for country in pycountry.countries
        if country.alpha_2.lower() in countries
    }
