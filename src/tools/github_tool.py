"""GitHub Integration Tool"""

from typing import Dict, Any, List, Optional

import requests
from github import Github, GithubException

from src.tools.base_tool import BaseTool
from src.config.settings import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GitHubTool(BaseTool):
    """Tool for interacting with GitHub API"""

    def __init__(self):
        """Initialize GitHub tool"""
        super().__init__(
            name="GitHubTool",
            description="Interact with GitHub repositories, issues, PRs, and code",
        )

        settings = get_settings()
        self.token = settings.github_token
        self.user = settings.github_user

        if not self.token:
            raise ValueError("GITHUB_TOKEN not set in environment")

        self.github = Github(self.token)

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute GitHub operation"""
        operation = kwargs.get("operation", "list_repos")

        operations = {
            "list_repos": self.list_repositories,
            "list_issues": self.list_issues,
            "create_issue": self.create_issue,
            "list_prs": self.list_pull_requests,
            "search_code": self.search_code,
            "get_file": self.get_file_content,
            "get_repo_info": self.get_repository_info,
        }

        if operation not in operations:
            return {"success": False, "error": f"Unknown operation: {operation}"}

        return await operations[operation](**kwargs)

    async def validate_input(self, **kwargs) -> bool:
        """Validate input parameters"""
        operation = kwargs.get("operation", "")
        return operation != ""

    async def list_repositories(self, **kwargs) -> Dict[str, Any]:
        """List user repositories"""
        try:
            user = self.github.get_user()
            repos = user.get_repos()

            repo_list = [
                {
                    "name": repo.name,
                    "url": repo.html_url,
                    "description": repo.description,
                    "stars": repo.stargazers_count,
                    "language": repo.language,
                }
                for repo in repos
            ]

            logger.debug(f"Listed {len(repo_list)} repositories")

            return {
                "success": True,
                "data": {"repositories": repo_list, "count": len(repo_list)},
            }

        except Exception as e:
            logger.error(f"Failed to list repositories: {str(e)}")
            return {"success": False, "error": str(e)}

    async def list_issues(self, **kwargs) -> Dict[str, Any]:
        """List repository issues"""
        repo_name = kwargs.get("repo", "")
        state = kwargs.get("state", "open")
        limit = kwargs.get("limit", 10)

        if not repo_name:
            return {"success": False, "error": "Repository name required"}

        try:
            repo = self.github.get_repo(repo_name)
            issues = repo.get_issues(state=state)

            issue_list = [
                {
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "url": issue.html_url,
                    "created_at": issue.created_at.isoformat(),
                    "labels": [label.name for label in issue.labels],
                }
                for issue in issues[:limit]
            ]

            logger.debug(f"Listed {len(issue_list)} issues from {repo_name}")

            return {
                "success": True,
                "data": {"issues": issue_list, "count": len(issue_list)},
            }

        except Exception as e:
            logger.error(f"Failed to list issues: {str(e)}")
            return {"success": False, "error": str(e)}

    async def create_issue(self, **kwargs) -> Dict[str, Any]:
        """Create new issue"""
        repo_name = kwargs.get("repo", "")
        title = kwargs.get("title", "")
        body = kwargs.get("body", "")

        if not all([repo_name, title]):
            return {"success": False, "error": "Repository name and title required"}

        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body)

            logger.debug(f"Issue created: {issue.number} in {repo_name}")

            return {
                "success": True,
                "data": {
                    "issue_number": issue.number,
                    "url": issue.html_url,
                    "title": issue.title,
                },
            }

        except Exception as e:
            logger.error(f"Failed to create issue: {str(e)}")
            return {"success": False, "error": str(e)}

    async def list_pull_requests(self, **kwargs) -> Dict[str, Any]:
        """List repository pull requests"""
        repo_name = kwargs.get("repo", "")
        state = kwargs.get("state", "open")
        limit = kwargs.get("limit", 10)

        if not repo_name:
            return {"success": False, "error": "Repository name required"}

        try:
            repo = self.github.get_repo(repo_name)
            prs = repo.get_pulls(state=state)

            pr_list = [
                {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "url": pr.html_url,
                    "author": pr.user.login,
                    "created_at": pr.created_at.isoformat(),
                }
                for pr in prs[:limit]
            ]

            logger.debug(f"Listed {len(pr_list)} PRs from {repo_name}")

            return {
                "success": True,
                "data": {"pull_requests": pr_list, "count": len(pr_list)},
            }

        except Exception as e:
            logger.error(f"Failed to list pull requests: {str(e)}")
            return {"success": False, "error": str(e)}

    async def search_code(self, **kwargs) -> Dict[str, Any]:
        """Search code in repositories"""
        query = kwargs.get("query", "")
        language = kwargs.get("language", "")
        limit = kwargs.get("limit", 5)

        if not query:
            return {"success": False, "error": "Search query required"}

        try:
            search_query = query
            if language:
                search_query += f" language:{language}"

            results = self.github.search_code(search_query)

            code_results = [
                {
                    "path": result.path,
                    "repository": result.repository.full_name,
                    "url": result.html_url,
                    "score": result.score,
                }
                for result in results[:limit]
            ]

            logger.debug(f"Found {len(code_results)} code results for: {query}")

            return {
                "success": True,
                "data": {"results": code_results, "count": len(code_results)},
            }

        except Exception as e:
            logger.error(f"Failed to search code: {str(e)}")
            return {"success": False, "error": str(e)}

    async def get_file_content(self, **kwargs) -> Dict[str, Any]:
        """Get file content from repository"""
        repo_name = kwargs.get("repo", "")
        file_path = kwargs.get("path", "")

        if not all([repo_name, file_path]):
            return {"success": False, "error": "Repository name and file path required"}

        try:
            repo = self.github.get_repo(repo_name)
            file = repo.get_contents(file_path)

            logger.debug(f"Retrieved file: {file_path} from {repo_name}")

            return {
                "success": True,
                "data": {
                    "content": file.decoded_content.decode("utf-8"),
                    "path": file.path,
                    "size": file.size,
                },
            }

        except Exception as e:
            logger.error(f"Failed to get file content: {str(e)}")
            return {"success": False, "error": str(e)}

    async def get_repository_info(self, **kwargs) -> Dict[str, Any]:
        """Get repository information"""
        repo_name = kwargs.get("repo", "")

        if not repo_name:
            return {"success": False, "error": "Repository name required"}

        try:
            repo = self.github.get_repo(repo_name)

            logger.debug(f"Retrieved info for repository: {repo_name}")

            return {
                "success": True,
                "data": {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "url": repo.html_url,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "language": repo.language,
                    "created_at": repo.created_at.isoformat(),
                    "updated_at": repo.updated_at.isoformat(),
                    "topics": repo.get_topics(),
                },
            }

        except Exception as e:
            logger.error(f"Failed to get repository info: {str(e)}")
            return {"success": False, "error": str(e)}
