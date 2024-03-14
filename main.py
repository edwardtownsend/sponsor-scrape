import json
import requests

NOTION_TOKEN = "secret_6eeibF3IPeoL8j4NJpUj579walrfJYgkChxjQTRMGvd"
DATABASE_ID = "cae626f5d084404ca4c21ca174f9dc31"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res

description = "Test Description"
data = {
    "URL": {"title": [{"text": {"content": description}}]},
}

create_page(data)
