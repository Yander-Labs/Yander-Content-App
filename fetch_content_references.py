#!/usr/bin/env python3
"""
Fetch and analyze content from successful creators database
This script accesses the reference database and extracts content patterns
"""

import os
import json
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

load_dotenv('/Users/jordanhayes/content-creation-agents/.env')

client = Client(auth=os.getenv('NOTION_API_KEY'))

# Reference database ID from the URL
# https://www.notion.so/1f7e3474427a4e73891106d20747f5bc?v=1e52c3cd0c8f410f87aa27bc8b47dc18
REFERENCE_DB_ID = "1f7e3474427a4e73891106d20747f5bc"

def fetch_reference_content():
    """Fetch content from the reference database"""
    try:
        print("🔍 Fetching reference content database...\n")

        # Get database info first
        db = client.databases.retrieve(database_id=REFERENCE_DB_ID)
        print(f"✅ Database: {db.get('title', [{}])[0].get('plain_text', 'Untitled')}\n")

        # Try to use search to find pages in this database
        # Note: Notion API version compatibility - using available methods
        print("⚠️  Note: Direct database query not available in current API version")
        print("Please share the database with the integration and provide sample content manually\n")

        return None

        # Alternative: Query the database (if API version supports it)
        # response = client.databases.query(database_id=REFERENCE_DB_ID)

        profiles = []

        for page in response.get('results', []):
            profile_data = {
                'id': page['id'],
                'url': page.get('url', ''),
                'properties': {}
            }

            # Extract properties
            props = page.get('properties', {})
            for prop_name, prop_data in props.items():
                prop_type = prop_data.get('type')

                if prop_type == 'title':
                    title_array = prop_data.get('title', [])
                    if title_array:
                        profile_data['properties']['name'] = title_array[0].get('plain_text', '')

                elif prop_type == 'url':
                    url_value = prop_data.get('url')
                    if url_value:
                        profile_data['properties'][prop_name.lower()] = url_value

                elif prop_type == 'rich_text':
                    text_array = prop_data.get('rich_text', [])
                    if text_array:
                        profile_data['properties'][prop_name.lower()] = text_array[0].get('plain_text', '')

                elif prop_type == 'select':
                    select_data = prop_data.get('select')
                    if select_data:
                        profile_data['properties'][prop_name.lower()] = select_data.get('name', '')

            profiles.append(profile_data)

        print(f"✅ Found {len(profiles)} reference profiles\n")

        for i, profile in enumerate(profiles, 1):
            print(f"{i}. {profile['properties'].get('name', 'Unnamed')}")
            for key, value in profile['properties'].items():
                if key != 'name' and value:
                    print(f"   {key}: {value}")
            print()

        # Save to file for research agent to use
        output_file = 'data/content_references.json'
        with open(output_file, 'w') as f:
            json.dump({
                'fetched_at': datetime.now().isoformat(),
                'profiles': profiles
            }, f, indent=2)

        print(f"💾 Saved to {output_file}")
        return profiles

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    fetch_reference_content()
