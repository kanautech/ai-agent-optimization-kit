#!/usr/bin/env python3
import os
import requests
import json

QIITA_API_TOKEN = os.getenv("QIITA_API_TOKEN")
ARTICLE_PATH = "QIITA_ARTICLE.md"

def publish_to_qiita():
    if not QIITA_API_TOKEN:
        print("Error: QIITA_API_TOKEN environment variable is not set.")
        return

    if not os.path.exists(ARTICLE_PATH):
        print(f"Error: {ARTICLE_PATH} not found.")
        return

    with open(ARTICLE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Qiita API endpoint
    url = "https://qiita.com/api/v2/items"
    
    headers = {
        "Authorization": f"Bearer {QIITA_API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Extract title and body (basic split or hardcoded)
    payload = {
        "title": "【Claude Code / Codex】AIエージェントの暴走とクォータ枯渇を防ぐ！TDD最適化キットの導入術",
        "body": content,
        "private": False,
        "tags": [
            {"name": "AI"},
            {"name": "ClaudeCode"},
            {"name": "TDD"},
            {"name": "生産性向上"},
            {"name": "ガードレール"}
        ],
        "tweet": True
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print("Successfully published to Qiita!")
        print("URL:", response.json().get("url"))
    else:
        print(f"Failed to publish to Qiita. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    publish_to_qiita()
