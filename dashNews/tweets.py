import requests
import base64

access_token = 0

def get_bearer_token():
    consumer_key = 'XpNXWUpRZUrbsY7nZIW1r8LnW'
    consumer_secret_key = 'VmoOPlVCyn8CKjZWefXNxz8RnZxZjNDN844PzkH9CWVsbOMOgO'

    # Reformat the keys and encode them
    key_secret = '{}:{}'.format(consumer_key, consumer_secret_key).encode('ascii')
    # Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)
    # Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_resp.json()['access_token']

    return access_token


def get_trending_tweets(country_code):
    global access_token
    if access_token == 0:
        access_token = get_bearer_token()

    trend_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    trend_params = {
        'id': country_code,
    }

    tweets = requests.get(
        "https://api.twitter.com/1.1/trends/place.json", headers=trend_headers, params=trend_params).json()
    print(tweets)
    return tweets[0]['trends']


def get_countries():
    global access_token
    if access_token == 0:
        access_token = get_bearer_token()

    newsapi_countries = ["ae","ar","at","au","be","bg","br","ca","ch","cn","co","cu","cz","de","eg","fr","gb","gr","hk","hu","id","ie","il","in","it","jp","kr","lt","lv","ma","mx","my","ng","nl","no","nz","ph","pl","pt","ro","rs","ru","sa","se","sg","si","sk","th","tr","tw","ua","us","ve","za"]

    trend_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    locations = requests.get(
        "https://api.twitter.com/1.1/trends/available.json", headers=trend_headers).json()

    news_twitter_dict = {}
    for place in locations:
        countryCode = place["countryCode"]
        if countryCode is not None and countryCode.lower() in newsapi_countries:
            news_twitter_dict[place["country"]] = {}
            news_twitter_dict[place["country"]]["newsid"] = countryCode.lower()
            news_twitter_dict[place["country"]]["twitterid"] = place["woeid"]
    return news_twitter_dict
