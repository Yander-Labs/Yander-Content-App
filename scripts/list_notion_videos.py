#!/usr/bin/env python3
"""
Script to list all video entries in Notion database.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from notion_client import Client

def main():
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not database_id:
        print("ERROR: NOTION_DATABASE_ID not set")
        return

    print("Querying Notion database for videos...\n")

    # Query for all entries
    try:
        results = notion.databases.query(database_id=database_id)
    except AttributeError:
        # Try alternative method
        import requests
        headers = {
            "Authorization": f"Bearer {os.getenv('NOTION_API_KEY')}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        response = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            headers=headers,
            json={}
        )
        results = response.json()

    print(f"Found {len(results['results'])} videos in Notion:\n")

    for page in results['results']:
        title = page['properties'].get('Name', {}).get('title', [])
        title_text = title[0]['text']['content'] if title else 'Untitled'

        status = page['properties'].get('Status', {}).get('select', {})
        status_name = status.get('name', 'Unknown') if status else 'Unknown'

        page_id = page['id']

        print(f"- {title_text[:60]}...")
        print(f"  Status: {status_name}")
        print(f"  Page ID: {page_id}")
        print()


if __name__ == "__main__":
    main()
