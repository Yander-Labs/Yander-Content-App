# Publish to Notion

Publish content to Hayes Media Notion database.

## Content
$ARGUMENTS

## Process

1. Extract from content:
   - Title (from hook/first line)
   - Hook
   - Full post
   - 3 key takeaways
   - Theme category

2. Publish using NotionAgent:

```python
import sys
sys.path.insert(0, '/Users/jordanhayes/content-creation-agents')
from agents import NotionAgent

agent = NotionAgent()
idea = {"title": "<title>", "theme": "<theme>"}
content = {
    "hook": "<hook>",
    "full_post": "<post>",
    "key_takeaways": ["<1>", "<2>", "<3>"]
}
result = agent.create_post_entry(idea, content)
print(f"https://notion.so/{result.replace('-', '')}")
```

3. Return the Notion URL

## Theme Categories
See CLAUDE.md for the 8 theme categories.
