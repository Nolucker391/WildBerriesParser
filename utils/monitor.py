import httpx
import datetime
from typing import Dict, List, Any


async def get_product_info(article: str) -> Dict[str, Any]:
    url = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-1257786&nm={article}"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        products = data.get("data", {}).get("products", [])
        if not products:
            raise ValueError("❌ Товар не найден")
        product = products[0]
        return {
            "name": product["name"],
            "id": product["id"],
            "root": product["root"],
        }

async def get_reviews(root_id: int) -> List[Dict[str, Any]]:
    domains = ["feedbacks1.wb.ru", "feedbacks2.wb.ru"]
    now = datetime.datetime.utcnow()
    three_days_ago = now - datetime.timedelta(days=3)
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        for dom in domains:
            url = f"https://{dom}/feedbacks/v1/{root_id}?limit=100&page=1"
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                continue
            feedbacks = resp.json().get("feedbacks", [])
            if not feedbacks:
                continue

            return [
                {
                    "id": f.get("id"),
                    "rating": f.get("productValuation", 5),
                    "text": f.get("text", "").strip(),
                    "advantages": f.get("pros", "").strip(),
                    "disadvantages": f.get("cons", "").strip(),
                    "author": f.get("wbUserDetails", {}).get("name") or "Покупатель",
                    "datetime": datetime.datetime.strptime(f["createdDate"], "%Y-%m-%dT%H:%M:%SZ")
                }
                for f in feedbacks
                if f.get("productValuation", 5) <= 3 and datetime.datetime.strptime(f["createdDate"], "%Y-%m-%dT%H:%M:%SZ") >= three_days_ago
            ]
    return []
