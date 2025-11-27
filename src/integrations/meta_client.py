# src/integrations/meta_client.py

import os
from typing import Dict, Any, List, Optional

import requests


META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_IG_BUSINESS_ID = os.getenv("META_IG_BUSINESS_ID")  # ID da conta IG Business
GRAPH_BASE_URL = "https://graph.facebook.com/v19.0"


class MetaClient:
    def __init__(
        self,
        access_token: Optional[str] = None,
        ig_business_id: Optional[str] = None,
    ):
        self.access_token = access_token or META_ACCESS_TOKEN
        self.ig_business_id = ig_business_id or META_IG_BUSINESS_ID

        if not self.access_token or not self.ig_business_id:
            raise ValueError(
                "META_ACCESS_TOKEN ou META_IG_BUSINESS_ID não configurados."
            )

    def _get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if params is None:
            params = {}

        params["access_token"] = self.access_token
        url = f"{GRAPH_BASE_URL}/{path.lstrip('/')}"
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_ig_account_insights(self) -> Dict[str, Any]:
        """
        Exemplo: puxa alguns insights da conta IG.
        Métricas possíveis: impressions, reach, profile_views, follower_count...
        """
        params = {
            "metric": "impressions,reach,profile_views,follower_count",
            "period": "day",
        }
        data = self._get(f"{self.ig_business_id}/insights", params)
        return data

    def get_recent_media_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Lista os posts recentes e pega métricas básicas (likes, comments, saves, reach).
        """
        media_data = self._get(
            f"{self.ig_business_id}/media",
            params={
                "fields": "id,caption,media_type,permalink,timestamp",
                "limit": limit,
            },
        )

        results: List[Dict[str, Any]] = []
        for item in media_data.get("data", []):
            media_id = item["id"]
            caption = item.get("caption")
            media_type = item.get("media_type")
            permalink = item.get("permalink")
            timestamp = item.get("timestamp")

            try:
                insights = self._get(
                    f"{media_id}/insights",
                    params={"metric": "impressions,reach,engagement,saved"},
                )
                metrics = {
                    m["name"]: m["values"][0]["value"] for m in insights.get("data", [])
                }
            except Exception:
                metrics = {}

            results.append(
                {
                    "id": media_id,
                    "caption": caption,
                    "media_type": media_type,
                    "permalink": permalink,
                    "timestamp": timestamp,
                    "metrics": metrics,
                }
            )

        return results
