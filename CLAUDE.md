# Content Creation Agents - Project Instructions

## Project Overview

AI-powered content generation system for Hayes Media. Generates LinkedIn posts, YouTube scripts, and manages content via Notion.

## Key Files

- `agents/` - All agent implementations
- `data/jordan_hayes_info.txt` - Creator context (update quarterly)
- `data/daily_content_themes.json` - Theme rotation config
- `data/content_style_references.json` - Writing style patterns
- `scripts/run_daily_content.py` - Daily automation script

## Writing Style Rules

When generating content for Jordan Hayes:

### Format
- **Hook**: Bold statement, under 8 words
- **Paragraphs**: 1-3 sentences max
- **Line breaks**: After every thought
- **Length**: 150-300 words for posts
- **NO emojis**
- **NO hashtags**

### Tone
- Direct and confident
- Speaks from experience, not theory
- Uses specific examples and numbers
- Avoids fluff - every point provides value

### Structure Patterns
- Hook > Story > Lesson > Takeaway
- Problem > Insight > Action
- Bold claim > Evidence > Application

### Themes to Rotate
1. Team Management & Workload
2. Client Relationships & Retention
3. Service Delivery & Quality
4. Agency Operations & Systems
5. Leadership & Culture
6. Value: We Trust You to Own It
7. Value: Under-Promise and Over-Deliver Early
8. Value: When They Win, We Win

## Company Values (use in content)

1. **We trust you to own it** - Ownership mindset, autonomy earned through reliability
2. **Under-promise and over-deliver early** - Timing matters, early delivery builds trust
3. **When they win, we win** - Be an extension of client's team, care about outcomes

## Notion Integration

- Database ID is in `.env` (NOTION_DATABASE_ID)
- New posts go to "Ideation" status
- Use NotionAgent for all Notion operations

## Common Tasks

### Write a post
```
/write-post <topic or angle>
```

### Publish to Notion
```
/publish-notion <content>
```

### Run daily generation
```
/daily-content <count>
```
Or: `python3 scripts/run_daily_content.py --count 3`

## Testing

```bash
# Test a single post generation
python3 -c "from agents import DailyContentAgent; a = DailyContentAgent(); print(a.run_daily(1))"

# Test Notion connection
python3 -c "from agents import NotionAgent; a = NotionAgent(); print(a.get_page_titles(7))"
```

## Context Maintenance

**Review quarterly:**
- `data/jordan_hayes_info.txt` - Update revenue figures, new achievements
- `data/daily_content_themes.json` - Add new prompts, retire stale ones
- `data/content_style_references.json` - Refresh style patterns if needed
