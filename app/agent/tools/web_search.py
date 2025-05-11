from langchain.tools import DuckDuckGoSearchResults
from langchain.tools import BaseTool
from bs4 import BeautifulSoup
import requests
from pydantic import Field


class DuckDuckGoWebReaderTool(BaseTool):
    name: str = "duckduckgo_web_reader"
    description: str = '''Поиск в интернете с использованием DuckDuckGo и извлечение текста 
                    с первой найденной страницы.'''
    search: DuckDuckGoSearchResults = Field(default_factory=DuckDuckGoSearchResults)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search = DuckDuckGoSearchResults()

    def _run(self, query: str) -> str:
        """
        Выполняет поиск через DuckDuckGo и возвращает содержимое первой страницы.

        Args:
            query (str): Поисковый запрос.

        Returns:
            str: Текст с первой страницы или ошибка.


        """
        try:
            results = self.search.run(query)
            if not results or "link" not in results[0]:
                return "Ничего не найдено."

            url = results[0]["link"]
            html = requests.get(url, timeout=10).text
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
            content = "\n".join(paragraphs[:10])

            return f"Источник: {url}\n\n{content.strip()}"
        except Exception as e:
            return f"Ошибка: {e}"
