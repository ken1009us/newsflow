from typing import Tuple, List, Dict, Any, Optional
from newsapi import NewsApiClient
from config import NEWS_API_KEY


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
    ) -> Dict[str, Any]:
        """Fetch top headlines with optional query and country filters."""
        kwargs = {}
        if query and query.strip():
            kwargs["q"] = query.strip()
        if country:
            kwargs["country"] = country

        try:
            result = self.client.get_top_headlines(**kwargs)
        except Exception as e:
            print(f"NewsAPI top_headlines error: {e}")
            return {"articles": []}

        return result

    def get_everything(
        self,
        query: str,
    ) -> Dict[str, Any]:
        """Search all articles using the everything endpoint."""
        try:
            result = self.client.get_everything(
                q=query,
                sort_by="relevancy",
                page_size=20,
            )
        except Exception as e:
            print(f"NewsAPI everything error: {e}")
            return {"articles": []}

        return result

    def search_news(
        self,
        query: str = None,
        country: str = None,
    ) -> Tuple[str, List[Dict[str, Any]], Optional[str], str]:
        """Search news with 3-tier fallback.

        Fallback chain:
        1. Top headlines for the specified country
        2. Everything endpoint with country name as keyword
        3. Worldwide top headlines (no country filter)

        Returns:
            Tuple of (title, articles, fallback_type, original_country_name).
            fallback_type is None (direct hit), "everything", or "worldwide".
        """
        from config import NEWSAPI_SUPPORTED_COUNTRIES

        original_country_name = NEWSAPI_SUPPORTED_COUNTRIES.get(country, "")
        fallback_type = None

        # Tier 1: top headlines for the specified country
        result = self.get_top_headlines(query=query, country=country)
        articles = result.get("articles", [])

        # Tier 2: if country was specified but no top headlines,
        # search "everything" using country name as keyword
        if not articles and country and original_country_name:
            fallback_type = "everything"
            everything_query = original_country_name
            if query and query.strip():
                everything_query = f"{original_country_name} {query.strip()}"
            result = self.get_everything(query=everything_query)
            articles = result.get("articles", [])

        # Tier 3: worldwide top headlines as last resort
        if not articles and country:
            fallback_type = "worldwide"
            result = self.get_top_headlines(query=query, country=None)
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
