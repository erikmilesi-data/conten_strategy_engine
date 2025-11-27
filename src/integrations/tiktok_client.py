import os
from typing import Dict, Any, List, Optional
import requests

TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")
TIKTOK_ADVERTISER_ID = os.getenv("TIKTOK_ADVERTISER_ID")
TIKTOK_BASE_URL = "https://business-api.tiktok.com/open_api/v1.3"


class TikTokClient:
    def __init__(
        self,
        access_token: Optional[str] = None,
        advertiser_id: Optional[str] = None,
    ):
        self.access_token = access_token or TIKTOK_ACCESS_TOKEN
        self.advertiser_id = advertiser_id or TIKTOK_ADVERTISER_ID

        if not self.access_token or not self.advertiser_id:
            raise ValueError(
                "TIKTOK_ACCESS_TOKEN ou TIKTOK_ADVERTISER_ID não configurados."
            )

    def _post(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json",
        }
        url = f"{TIKTOK_BASE_URL}/{path.lstrip('/')}"
        resp = requests.post(url, headers=headers, json=json, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_video_stats(self, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Exemplo de endpoint de estatísticas de vídeo (ajustar conforme doc oficial).
        """
        payload = {
            "advertiser_id": self.advertiser_id,
            "page_size": page_size,
        }
        data = self._post("video/list/", json=payload)
        return data.get("data", {}).get("list", [])
