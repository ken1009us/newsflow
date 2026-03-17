from typing import Tuple, List, Dict, Any, Optional
from newsapi import NewsApiClient
from config import NEWS_API_KEY


LANG_TO_NEWSAPI = {
    "en": "en",
    "zh_tw": "zh",
    "ja": None,  # NewsAPI doesn't support Japanese; use country=jp instead
}

# When no country is selected, auto-pick a default country for the language
LANG_DEFAULT_COUNTRY = {
    "ja": "jp",
    "zh_tw": "tw",
}


class NewsService:
    """Encapsulates NewsAPI calls. Lazy-initializes the client."""

    def __init__(self):
        self._client = None

    @property
    def client(self) -> NewsApiClient:
        if self._client is None:
            if not NEWS_API_KEY:
                raise RuntimeError(
                    "NEWS_API_KEY is not set. "
                    "Please set the NEWS_API_KEY environment variable."
                )
            self._client = NewsApiClient(api_key=NEWS_API_KEY)
        return self._client

    def get_top_headlines(
        self,
        query: str = None,
        country: str = None,
        language: str = None,
    ) -> Dict[str, Any]:
        """Fetch top headlines with optional query and country filters.

        Note: NewsAPI doesn't allow country + language together.
        Language is only used when country is not set.
        """
        kwargs = {}
        if query and query.strip():
            kwargs["q"] = query.strip()
        if country:
            kwargs["country"] = country
        elif language:
            kwargs["language"] = language

        try:
            result = self.client.get_top_headlines(**kwargs)
        except Exception as e:
            print(f"NewsAPI top_headlines error: {e}")
            return {"articles": []}

        return result

    def get_everything(
        self,
        query: str,
        language: str = None,
    ) -> Dict[str, Any]:
        """Search all articles using the everything endpoint."""
        kwargs = {
            "q": query,
            "sort_by": "relevancy",
            "page_size": 20,
        }
        if language:
            kwargs["language"] = language

        try:
            result = self.client.get_everything(**kwargs)
        except Exception as e:
            print(f"NewsAPI everything error: {e}")
            return {"articles": []}

        return result

    def search_news(
        self,
        query: str = None,
        country: str = None,
        lang: str = None,
    ) -> Tuple[str, List[Dict[str, Any]], Optional[str], str]:
        """Search news with 3-tier fallback and language filtering.

        Fallback chain:
        1. Top headlines for the specified country
        2. Everything endpoint with country name as keyword
        3. Worldwide top headlines (no country filter)

        Returns:
            Tuple of (title, articles, fallback_type, original_country_name).
            fallback_type is None (direct hit), "everything", or "worldwide".
        """
        from config import NEWSAPI_SUPPORTED_COUNTRIES

        # Map UI language to NewsAPI language code
        api_lang = LANG_TO_NEWSAPI.get(lang)

        # If no country selected, use default country for the language
        if not country and lang in LANG_DEFAULT_COUNTRY:
            country = LANG_DEFAULT_COUNTRY[lang]

        original_country_name = NEWSAPI_SUPPORTED_COUNTRIES.get(country, "")
        fallback_type = None

        # Tier 1: top headlines for the specified country
        result = self.get_top_headlines(
            query=query, country=country, language=api_lang,
        )
        articles = result.get("articles", [])

        # Tier 2: if country was specified but no top headlines,
        # search "everything" using country name as keyword
        if not articles and country and original_country_name:
            fallback_type = "everything"
            everything_query = original_country_name
            if query and query.strip():
                everything_query = f"{original_country_name} {query.strip()}"
            result = self.get_everything(
                query=everything_query, language=api_lang,
            )
            articles = result.get("articles", [])

        # Tier 3: worldwide top headlines as last resort
        if not articles and country:
            fallback_type = "worldwide"
            result = self.get_top_headlines(
                query=query, country=None, language=api_lang,
            )
            articles = result.get("articles", [])

        title = self._build_title(query, country, has_articles=bool(articles))

        return title, articles, fallback_type, original_country_name

    def _build_title(
        self, query: str, country: str, has_articles: bool
    ) -> str:
        from config import NEWSAPI_SUPPORTED_COUNTRIES

        if not has_articles:
            return "No articles found."

        country_name = NEWSAPI_SUPPORTED_COUNTRIES.get(country, "")

        if query and country_name:
            return f"Top News Articles with '{query}' from {country_name}"
        elif query:
            return f"Top News Articles with '{query}' Worldwide"
        elif country_name:
            return f"Top News Articles from {country_name}"
        else:
            return "Top News Articles Worldwide"
