#!/usr/bin/env python3
"""Test creating a page with 'Content' toggle matching the New Page template"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv('/Users/jordanhayes/content-creation-agents/.env')

client = Client(auth=os.getenv('NOTION_API_KEY'))
db_id = os.getenv('NOTION_DATABASE_ID')

print('🧪 Creating test page with "Content" toggle structure...\n')

try:
    # Build content for the toggle
    toggle_content = [
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Hook"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "This is where the hook goes - the first 30 seconds to grab attention..."}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Intro"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "The introduction sets expectations and introduces yourself..."}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Main Content"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Here's where the main script content goes - all the valuable information..."}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Call to Action"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "What should viewers do next? Subscribe, comment, try something..."}
                }]
            }
        }
    ]

    # Create the page with "Content" toggle structure
    new_page = client.pages.create(
        parent={"database_id": db_id},
        properties={
            "Name": {
                "title": [{
                    "text": {
                        "content": "🧪 Test - New Page Template Structure"
                    }
                }]
            },
            "Status": {
                "select": {"name": "Ideation"}
            },
            "Where": {
                "multi_select": [{"name": "YouTube"}]
            },
            "Media": {
                "select": {"name": "video"}
            }
        },
        children=[
            # Create "Content" as H1 toggle block (matching template)
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "Content"}
                    }],
                    "is_toggleable": True,
                    "children": toggle_content
                }
            },
            # Add additional info outside the toggle
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "🗺️ Mindmap: output/mindmaps/test_mindmap.svg"}
                    }]
                }
            }
        ]
    )

    print('✅ Test page created successfully!')
    print(f'   Page ID: {new_page["id"]}')
    print(f'   URL: {new_page["url"]}')
    print('\n📋 Structure:')
    print('   ├─ Properties:')
    print('   │   ├─ Status: Ideation')
    print('   │   ├─ Where: YouTube')
    print('   │   └─ Media: video')
    print('   └─ Content:')
    print('       └─ Toggle: "Content"')
    print('           ├─ Hook')
    print('           ├─ Intro')
    print('           ├─ Main Content')
    print('           └─ Call to Action')
    print('\n🎯 Check Notion - the page should match your "New Page" template structure!')

except Exception as e:
    print(f'❌ Error: {str(e)}')
    import traceback
    traceback.print_exc()
