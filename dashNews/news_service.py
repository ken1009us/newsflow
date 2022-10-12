from typing import Tuple, List, Dict, Any
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
        """Fetch top headlines with optional query and country filters.

        Args:
            query: Search keyword(s). None or empty string means no filter.
            country: ISO 3166-1 alpha-2 country code (lowercase). None means worldwide.

        Returns:
            A dict with 'articles' key containing a list of article dicts.
        """
        kwargs = {}
        if query and query.strip():
            kwargs["q"] = query.strip()
        if country:
            kwargs["country"] = country

        try:
            result = self.client.get_top_headlines(**kwargs)
        except Exception as e:
            print(f"NewsAPI error: {e}")
            return {"articles": []}

        return result

    def search_news(
        self,
        query: str = None,
        country: str = None,
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Search news and return a title string and articles list.

        Args:
            query: Search keyword(s).
            country: Country code.

        Returns:
            Tuple of (title_string, articles_list).
        """
        result = self.get_top_headlines(query=query, country=country)
        articles = result.get("articles", [])

        # Build title
        title = self._build_title(query, country, has_articles=bool(articles))

        return title, articles

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
