# Publish to Notion

Publish content to the Hayes Media Notion content database.

## Content to Publish
$ARGUMENTS

## Process

1. **Parse the content** to extract:
   - Title (from hook or first line)
   - Hook (opening line)
   - Full post content
   - Key takeaways (3 bullet points)
   - Theme category

2. **Use the NotionAgent** to create the page:

```python
import sys
sys.path.insert(0, '/Users/jordanhayes/content-creation-agents')

from agents import NotionAgent

agent = NotionAgent()

idea = {
    "title": "<extracted title>",
    "theme": "<theme category>"
}

content = {
    "hook": "<opening line>",
    "full_post": "<complete post text>",
    "key_takeaways": ["<takeaway 1>", "<takeaway 2>", "<takeaway 3>"]
}

result = agent.create_post_entry(idea, content)
print(f"Created: https://notion.so/{result.replace('-', '')}")
```

3. **Return the Notion URL** to confirm success

## Theme Categories
- Team Management & Workload
- Client Relationships & Retention
- Service Delivery & Quality
- Agency Operations & Systems
- Leadership & Culture
- Value: We Trust You to Own It
- Value: Under-Promise and Over-Deliver Early
- Value: When They Win, We Win

## Notes
- Posts are created with "Ideation" status by default
- The page includes the full post, hook, and key takeaways
- Content is formatted with proper Notion blocks
