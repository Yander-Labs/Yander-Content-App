# Run Daily Content Generation

Generate and publish daily content automatically.

## Arguments
$ARGUMENTS

Default: 3 posts if no count specified.

## Process

Run the daily content generator:

```bash
cd /Users/jordanhayes/content-creation-agents
python3 scripts/run_daily_content.py --count <number>
```

## What It Does

1. **Selects themes** from rotation (8 themes available)
2. **Checks recent posts** in Notion to avoid duplicates
3. **Generates ideas** based on theme and creator context
4. **Writes posts** following approved style guidelines
5. **Publishes to Notion** with "Ideation" status

## Theme Rotation
- Team Management & Workload
- Client Relationships & Retention
- Service Delivery & Quality
- Agency Operations & Systems
- Leadership & Culture
- Value: We Trust You to Own It
- Value: Under-Promise and Over-Deliver Early
- Value: When They Win, We Win

## Output

- **Logs**: `output/logs/daily_content_YYYYMMDD.log`
- **Results**: `output/posts/daily_YYYYMMDD/results.json`

## Cron Setup (for automation)

```bash
# Runs daily at 6am
0 6 * * * cd /Users/jordanhayes/content-creation-agents && python3 scripts/run_daily_content.py >> output/logs/cron.log 2>&1
```
