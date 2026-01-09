import requests
from pymongo import MongoClient

MONGO_URL = "YOUR_MONGODB_URL"
DB_NAME = "YOUR_DB_NAME"
COLLECTION = "characters"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
col = db[COLLECTION]

query = """
query ($page: Int) {
  Page(page: $page, perPage: 20) {
    characters {
      name {
        full
      }
      image {
        large
      }
    }
  }
}
"""

url = "https://graphql.anilist.co"

page = 1
added = 0

while added < 100:   # change to 500 / 1000 if you want
    response = requests.post(
        url,
        json={"query": query, "variables": {"page": page}}
    ).json()

    chars = response["data"]["Page"]["characters"]

    for c in chars:
        if not c["image"]["large"]:
            continue

        col.insert_one({
            "name": c["name"]["full"],
            "img_url": c["image"]["large"]
        })
        added += 1
        if added >= 100:
            break

    page += 1

print(f"✅ Added {added} characters to database")
