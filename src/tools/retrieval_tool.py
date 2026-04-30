"""Information Retrieval Tool for searching and fetching data"""

import requests
from typing import Dict, Any, List, Optional
from urllib.parse import quote

from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RetrievalTool(BaseTool):
    """Tool for retrieving information from various sources"""

    def __init__(self):
        """Initialize retrieval tool"""
        super().__init__(
            name="RetrievalTool",
            description="Search and retrieve information from web sources and APIs",
        )

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute retrieval operation"""
        operation = kwargs.get("operation", "search")

        operations = {
            "search": self.web_search,
            "fetch_url": self.fetch_url_content,
            "search_github": self.search_github_topics,
            "fetch_documentation": self.fetch_documentation,
        }

        if operation not in operations:
            return {"success": False, "error": f"Unknown operation: {operation}"}

        return await operations[operation](**kwargs)

    async def validate_input(self, **kwargs) -> bool:
        """Validate input parameters"""
        operation = kwargs.get("operation", "")
        return operation != ""

    async def web_search(self, **kwargs) -> Dict[str, Any]:
        """Search the web for information"""
        query = kwargs.get("query", "")
        limit = kwargs.get("limit", 5)

        if not query:
            return {"success": False, "error": "Search query required"}

        try:
            logger.debug(f"Searching web for: {query}")

            # Using DuckDuckGo API as alternative
            url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_redirect=1"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            results = []
            if data.get("Results"):
                results = [
                    {
                        "title": r.get("Text", ""),
                        "url": r.get("FirstURL", ""),
                        "snippet": r.get("Result", ""),
                    }
                    for r in data["Results"][:limit]
                ]

            logger.debug(f"Found {len(results)} web results for: {query}")

            return {
                "success": True,
                "data": {
                    "query": query,
                    "results": results,
                    "count": len(results),
                },
            }

        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            return {"success": False, "error": str(e)}

    async def fetch_url_content(self, **kwargs) -> Dict[str, Any]:
        """Fetch content from URL"""
        url = kwargs.get("url", "")

        if not url:
            return {"success": False, "error": "URL required"}

        try:
            logger.debug(f"Fetching URL: {url}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            content = response.text

            logger.debug(f"Successfully fetched URL: {url}")

            return {
                "success": True,
                "data": {
                    "url": url,
                    "content": content[:5000],  # Limit content size
                    "status_code": response.status_code,
                },
            }

        except requests.Timeout:
            logger.error(f"Timeout fetching URL: {url}")
            return {"success": False, "error": "Request timeout"}

        except Exception as e:
            logger.error(f"Failed to fetch URL: {str(e)}")
            return {"success": False, "error": str(e)}

    async def search_github_topics(self, **kwargs) -> Dict[str, Any]:
        """Search GitHub topics"""
        topic = kwargs.get("topic", "")
        limit = kwargs.get("limit", 10)

        if not topic:
            return {"success": False, "error": "Topic required"}

        try:
            logger.debug(f"Searching GitHub topics: {topic}")

            url = "https://api.github.com/search/repositories"
            params = {
                "q": f"topic:{topic}",
                "sort": "stars",
                "per_page": limit,
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            repos = [
                {
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "url": repo["html_url"],
                    "description": repo["description"],
                    "stars": repo["stargazers_count"],
                    "language": repo["language"],
                }
                for repo in data.get("items", [])
            ]

            logger.debug(f"Found {len(repos)} repositories for topic: {topic}")

            return {
                "success": True,
                "data": {
                    "topic": topic,
                    "repositories": repos,
                    "count": len(repos),
                },
            }

        except Exception as e:
            logger.error(f"GitHub topic search failed: {str(e)}")
            return {"success": False, "error": str(e)}

    async def fetch_documentation(self, **kwargs) -> Dict[str, Any]:
        """Fetch documentation from common sources"""
        project = kwargs.get("project", "")
        section = kwargs.get("section", "")

        if not project:
            return {"success": False, "error": "Project name required"}

        try:
            logger.debug(f"Fetching documentation for: {project}")

            # Map projects to documentation URLs
            docs_mapping = {
                "python": "https://docs.python.org/3/",
                "django": "https://docs.djangoproject.com/",
                "fastapi": "https://fastapi.tiangolo.com/",
                "openai": "https://platform.openai.com/docs/",
            }

            if project not in docs_mapping:
                return {"success": False, "error": f"Documentation not available for: {project}"}

            url = docs_mapping[project]

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            logger.debug(f"Successfully fetched documentation for: {project}")

            return {
                "success": True,
                "data": {
                    "project": project,
                    "url": url,
                    "content": response.text[:2000],  # Limit content
                },
            }

        except Exception as e:
            logger.error(f"Documentation fetch failed: {str(e)}")
            return {"success": False, "error": str(e)}
