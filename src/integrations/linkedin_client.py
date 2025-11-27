import os
from typing import Dict, Any, List, Optional
import requests

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_ORG_ID = os.getenv("LINKEDIN_ORG_ID")
LINKEDIN_BASE_URL = "https://api.linkedin.com/v2"


class LinkedInClient:
    def __init__(
        self,
        access_token: Optional[str] = None,
        org_id: Optional[str] = None,
    ):
        self.access_token = access_token or LINKEDIN_ACCESS_TOKEN
        self.org_id = org_id or LINKEDIN_ORG_ID

        if not self.access_token:
            raise ValueError("LINKEDIN_ACCESS_TOKEN não configurado.")

    def _get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        url = f"{LINKEDIN_BASE_URL}/{path.lstrip('/')}"
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_organization_posts(self, limit: int = 10) -> Dict[str, Any]:
        """
        Exemplo básico de busca de posts de uma organization.
        """
        if not self.org_id:
            raise ValueError("LINKEDIN_ORG_ID não configurado.")

        params = {
            "q": "organization",
            "organization": f"urn:li:organization:{self.org_id}",
            "count": limit,
        }
        data = self._get("ugcPosts", params=params)
        return data
