#!/usr/bin/env python3
"""Find the 'New Page' template in Notion database"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv('/Users/jordanhayes/content-creation-agents/.env')

client = Client(auth=os.getenv('NOTION_API_KEY'))
db_id = os.getenv('NOTION_DATABASE_ID')

try:
    print('🔍 Searching for "New Page" template...\n')

    # Query all pages in the database
    response = client.databases.query(database_id=db_id)

    template_id = None

    for page in response.get('results', []):
        # Get the title
        props = page.get('properties', {})
        for prop_name, prop_data in props.items():
            if prop_data.get('type') == 'title':
                title_array = prop_data.get('title', [])
                if title_array:
                    title = title_array[0].get('plain_text', '')

                    # Check if this is the template
                    if title.lower() == 'new page' or 'new page' in title.lower():
                        template_id = page['id']
                        print(f'✅ Found template: "{title}"')
                        print(f'   Template ID: {template_id}')
                        print(f'   URL: {page["url"]}')

                        # Check if it's marked as a template
                        is_template = page.get('is_template', False)
                        print(f'   Is Template: {is_template}')

                        # Save template ID for later use
                        with open('/tmp/notion_template_id.txt', 'w') as f:
                            f.write(template_id)

                        print(f'\n💾 Template ID saved to /tmp/notion_template_id.txt')
                        break

        if template_id:
            break

    if not template_id:
        print('❌ No "New Page" template found in database')
        print('\nSearched through the following pages:')
        for page in response.get('results', [])[:5]:
            props = page.get('properties', {})
            for prop_name, prop_data in props.items():
                if prop_data.get('type') == 'title':
                    title_array = prop_data.get('title', [])
                    if title_array:
                        title = title_array[0].get('plain_text', '')
                        print(f'  • {title}')
                        break

except Exception as e:
    print(f'❌ Error: {str(e)}')
    import traceback
    traceback.print_exc()
