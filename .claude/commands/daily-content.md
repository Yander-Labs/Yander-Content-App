# Daily Content Generation

Generate and publish daily content automatically.

## Count
$ARGUMENTS

Default: 3 posts

## Command

```bash
cd /Users/jordanhayes/content-creation-agents
python3 scripts/run_daily_content.py --count <number>
```

## What It Does

1. Selects themes from rotation (see CLAUDE.md for themes)
2. Checks Notion for recent posts (avoids duplicates)
3. Generates ideas based on theme + creator context
4. Writes posts following style rules in CLAUDE.md
5. Publishes to Notion with "Ideation" status

## Output

- Logs: `output/logs/daily_content_YYYYMMDD.log`
- Results: `output/posts/daily_YYYYMMDD/results.json`

## Cron Setup

```bash
0 6 * * * cd /Users/jordanhayes/content-creation-agents && python3 scripts/run_daily_content.py >> output/logs/cron.log 2>&1
```
