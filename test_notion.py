#!/usr/bin/env python3
"""Test Notion integration and create test card"""

import os
import json
from dotenv import load_dotenv
from notion_client import Client

# Load env from specific path
load_dotenv('/Users/jordanhayes/content-creation-agents/.env')

client = Client(auth=os.getenv('NOTION_API_KEY'))
db_id = os.getenv('NOTION_DATABASE_ID')

print(f'API Key: {os.getenv("NOTION_API_KEY")[:20]}...')
print(f'Database ID: {db_id}\n')

try:
    # Get database info
    db = client.databases.retrieve(database_id=db_id)
    print(f'✅ Database: {db.get("title", [{}])[0].get("plain_text", "Untitled")}\n')

    # Check properties
    props = db.get('properties', {})
    print(f'Properties found: {len(props)}')

    if props:
        for name, data in props.items():
            print(f'  • {name}: {data.get("type")}')
    else:
        print('  (No standard properties - likely a board/gallery view)\n')

    # Create test page
    print('\n🧪 Creating test card...')

    new_page = client.pages.create(
        parent={"database_id": db_id},
        properties={
            "title": {
                "title": [
                    {
                        "text": {
                            "content": "🧪 Test Card from AI Content Agent"
                        }
                    }
                ]
            }
        },
        children=[
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "Test Content"}
                    }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "This is a test card created by your AI content creation system to verify the Notion integration is working correctly."}
                    }]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "Script Content"}
                    }],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "Your video script or post content will go here in a toggle block, just like you requested!"}
                                }]
                            }
                        }
                    ]
                }
            }
        ]
    )

    print(f'✅ Test card created successfully!')
    print(f'   Page ID: {new_page["id"]}')
    print(f'   URL: {new_page["url"]}')
    print(f'\n🎯 Check your Notion board - the test card should appear!')
    print(f'   (It might be in a default view/column)')

    # Save response
    with open('/tmp/created_page.json', 'w') as f:
        json.dump(new_page, f, indent=2)

except Exception as e:
    print(f'\n❌ Error: {str(e)}')
    import traceback
    traceback.print_exc()
