#!/usr/bin/env python3
"""Update test card with proper status and properties"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv('/Users/jordanhayes/content-creation-agents/.env')

client = Client(auth=os.getenv('NOTION_API_KEY'))

# Test card page ID from creation
test_page_id = "2ebf5ce3-1c48-81ea-b912-c6bd0d84208a"

try:
    print('🔄 Updating test card with proper properties...\n')

    # Update the page properties
    updated_page = client.pages.update(
        page_id=test_page_id,
        properties={
            "Status": {
                "select": {
                    "name": "Ideation"
                }
            },
            "Where": {
                "multi_select": [
                    {"name": "YouTube"}
                ]
            },
            "Media": {
                "select": {
                    "name": "video"
                }
            }
        }
    )

    print('✅ Test card updated successfully!')
    print(f'   Status: Ideation')
    print(f'   Where: YouTube')
    print(f'   Media: video')
    print(f'\n🎯 Check your Notion - the card should now appear in the Ideation column!')

except Exception as e:
    print(f'❌ Error: {str(e)}')
    print('\nTrying to get available options...')

    # If update failed, query the database to see valid options
    try:
        db_id = os.getenv('NOTION_DATABASE_ID')
        db = client.databases.retrieve(database_id=db_id)

        print('\nAvailable property options:')
        for prop_name, prop_data in db.get('properties', {}).items():
            if prop_data.get('type') == 'select':
                options = prop_data.get('select', {}).get('options', [])
                if options:
                    print(f'  {prop_name}: {[o.get("name") for o in options]}')
            elif prop_data.get('type') == 'multi_select':
                options = prop_data.get('multi_select', {}).get('options', [])
                if options:
                    print(f'  {prop_name}: {[o.get("name") for o in options]}')
    except:
        pass

    import traceback
    traceback.print_exc()
