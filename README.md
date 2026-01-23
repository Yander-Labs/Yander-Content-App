# Content Creation Agents

An AI-powered multi-agent system for automating content creation workflows for marketing agencies. This system handles everything from ideation to production-ready scripts, mindmaps, and Notion database management.

## Features

### 🔍 **Task 1: Content Research Agent**
- Researches ideas for long-form YouTube videos (10-30 minutes)
- Generates text-based post ideas (150+ words)
- Analyzes your tool information and user-provided data
- Sources knowledge from online resources
- Generates compelling content ideas focused on marketing agency operations, growth, and strategy

### ✍️ **Task 2: Scriptwriting Agent**
- Writes complete video scripts with hooks, intro, main content, and CTAs
- Creates engaging post copy that educates and converts
- Structures content for maximum viewer/reader retention
- Optimizes for educational content about operations, marketing, and growth

### 🗺️ **Task 3: Visual Mindmap Generator**
- Creates beautiful SVG mindmaps for YouTube videos
- Visualizes key concepts and relationships
- Generates high-quality graphics (1920x1080) ready for video editing
- Uses modern, professional design with color-coded branches

### 📊 **Task 4: Notion Database Integration**
- Automatically creates entries in your Notion database
- Organizes scripts, ideas, and mindmaps in one place
- Includes full scripts, production notes, and metadata
- Tracks content status (Script Ready, Recording, Editing, Published)

### 🎬 **Task 5: Video Editor Notification**
- Automatically notifies your video editor when files are ready
- Assigns tasks with checklists in Notion
- Includes raw video file references and editing notes
- Streamlines the post-recording workflow

### 🔄 **Task 6: Autonomous Daily Content Generation**
- Runs daily via cron to generate and publish content automatically
- Rotates through 8 themes (team management, client relationships, operations, leadership, company values)
- Avoids duplicate content by checking recent Notion posts
- Generates 2-3 posts per day with zero manual intervention
- Publishes directly to Notion with "Ideation" status

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│          Content Creation Orchestrator              │
│                                                      │
│  Coordinates all agents and manages workflow        │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
   ┌────▼───┐ ┌───▼────┐ ┌──▼──────┐
   │Research│ │Script  │ │Mindmap  │
   │ Agent  │ │Agent   │ │Generator│
   └────┬───┘ └───┬────┘ └──┬──────┘
        │         │          │
        └─────────┼──────────┘
                  │
         ┌────────▼─────────┐
         │  Notion Agent    │
         └────────┬─────────┘
                  │
         ┌────────▼─────────┐
         │ Editor Notifier  │
         └──────────────────┘


┌─────────────────────────────────────────────────────┐
│        Daily Content Agent (Autonomous)             │
│                                                      │
│  Runs via cron, generates content automatically     │
└──────────────────┬──────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐    ┌────▼────┐   ┌────▼────┐
│ Theme │    │  Idea   │   │  Post   │
│Select │───▶│Generate │──▶│ Writer  │
└───────┘    └─────────┘   └────┬────┘
                                │
                       ┌────────▼─────────┐
                       │  Notion Agent    │
                       └──────────────────┘
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

```bash
cd ~/content-creation-agents
```

### Step 2: Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys (see **API Setup Guide** below)

## API Setup Guide

### Required: Anthropic API Key

1. Go to [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Sign in or create an account
3. Click "Create Key"
4. Copy the key and add to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### Optional: Notion API Setup

Required for Tasks 4 & 5 (Notion integration and editor notifications).

#### 1. Create a Notion Integration

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Give it a name (e.g., "Content Creation Agents")
4. Select the workspace
5. Copy the "Internal Integration Token"
6. Add to `.env`:
   ```
   NOTION_API_KEY=secret_...
   ```

#### 2. Create a Content Database

1. In Notion, create a new database (full page)
2. Add these properties:
   - **Title** (title) - automatically created
   - **Type** (select) - Options: "Video", "Post", "Editing Task"
   - **Status** (select) - Options: "Script Ready", "Recording", "Ready for Editing", "In Editing", "Published"
   - **Target Length** (number)
   - **Word Count** (number)
   - **Keywords** (multi-select)
   - **Platform** (select) - Options: "YouTube", "LinkedIn", "Twitter", "Blog"
   - **Created Date** (date)
   - **Recording Date** (date)
   - **Due Date** (date)
   - **Priority** (select) - Options: "Low", "Medium", "High"
   - **Assigned To** (person)

3. Share the database with your integration:
   - Click "..." in top right
   - Select "Add connections"
   - Choose your integration

4. Get the database ID:
   - Copy the database URL: `https://notion.so/xxxxx?v=yyyy`
   - The database ID is the `xxxxx` part (32 characters)
   - Add to `.env`:
     ```
     NOTION_DATABASE_ID=xxxxx
     ```

#### 3. Get Video Editor's User ID (Optional)

1. In Notion, click on your workspace name → Settings
2. Go to "Members"
3. Right-click on your video editor's name → "Copy link"
4. Extract the user ID from the URL
5. Add to `.env`:
   ```
   VIDEO_EDITOR_NOTION_USER_ID=xxxxx
   ```

## Usage

### Create a Single Video

```bash
python3 main.py create-video \
  --topics "client retention,agency automation" \
  --tone professional
```

### Create a Single Post

```bash
python3 main.py create-post \
  --topics "agency growth strategies" \
  --tone educational
```

### Batch Create Videos

```bash
python3 main.py batch \
  --type video \
  --count 5 \
  --topics "marketing,operations,growth"
```

### Batch Create Posts

```bash
python3 main.py batch \
  --type post \
  --count 10 \
  --topics "automation,client management"
```

### Notify Editor After Recording

```bash
python3 main.py notify-editor \
  --page-id abc123def456 \
  --files "recording1.mp4,recording2.mp4" \
  --notes "Great energy in take 2!"
```

### Daily Content Generation (Automated)

Run the daily content generator manually:

```bash
python3 scripts/run_daily_content.py
```

Or specify the number of posts:

```bash
python3 scripts/run_daily_content.py --count 2
```

#### Setting Up Cron for Daily Automation

To run automatically every day at 6am:

```bash
# Open crontab editor
crontab -e

# Add this line (adjust path as needed)
0 6 * * * cd /Users/jordanhayes/content-creation-agents && /usr/bin/python3 scripts/run_daily_content.py >> output/logs/cron.log 2>&1
```

#### Theme Configuration

Edit `data/daily_content_themes.json` to customize themes:

```json
{
  "themes": [
    {
      "name": "team_management",
      "display_name": "Team Management & Workload",
      "keywords": ["team", "hiring", "burnout"],
      "prompts": ["How to spot burnout before it's too late"]
    }
  ],
  "last_used_index": 0,
  "rotation_strategy": "sequential"
}
```

The system rotates through themes sequentially, tracking progress in `last_used_index`.

#### Daily Content Output

Results are saved to:
- **Logs**: `output/logs/daily_content_YYYYMMDD.log`
- **Results**: `output/posts/daily_YYYYMMDD/results.json`

### Using Data Files

Create a file with your tool information:

```bash
# data/tool_info.txt
Our platform is a marketing automation tool designed specifically for agencies.
Key features include:
- Client portal with white-label branding
- Automated reporting and analytics
- Campaign management across channels
- Team collaboration tools
```

Then use it:

```bash
python3 main.py create-video \
  --tool-info-file data/tool_info.txt \
  --topics "automation workflows"
```

## Output Structure

All generated content is saved in the `output/` directory:

```
output/
├── scripts/              # Video scripts and post copy (JSON)
├── mindmaps/            # SVG mindmap files
├── videos/              # Video-related files
└── *.json               # Full result files
```

Each result file contains:
- Original content idea
- Complete script/copy
- Mindmap structure (if applicable)
- Notion page URL and ID
- Timestamps and metadata

## Advanced Usage

### Python API

You can also use the agents programmatically:

```python
from orchestrator import ContentCreationOrchestrator

# Initialize
orchestrator = ContentCreationOrchestrator()

# Create video content
result = orchestrator.create_video_content(
    tool_info="Your marketing tool description",
    topics=["client retention", "automation"],
    tone="professional"
)

# Access results
notion_url = result['notion']['page_url']
mindmap_file = result['mindmap']['svg_file']
script = result['script']

print(f"Notion page: {notion_url}")
print(f"Mindmap: {mindmap_file}")
```

### Individual Agents

You can use agents individually:

```python
from agents.research_agent import ResearchAgent
from agents.scriptwriting_agent import ScriptwritingAgent

# Research only
research = ResearchAgent()
ideas = research.execute(
    tool_info="Your tool info",
    topics=["agency growth"],
    num_video_ideas=5
)

# Write script for a specific idea
writer = ScriptwritingAgent()
script = writer.execute(
    content_type="video",
    idea=ideas['video_ideas'][0],
    tone="professional"
)
```

## Customization

### Modify Content Settings

Edit `config/config.yaml`:

```yaml
content:
  video:
    default_length_minutes: 20  # Change default video length
  post:
    default_length_words: 300   # Change default post length
  default_tone: "casual"         # Change default tone
```

### Adjust Agent Behavior

Each agent has customizable parameters in `config/config.yaml`:

```yaml
agents:
  research:
    max_tokens: 4096
    temperature: 1.0
  scriptwriting:
    temperature: 0.8  # Lower = more focused, Higher = more creative
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Ensure you've created a `.env` file
- Check that your API key is correctly formatted
- Verify the key is valid at console.anthropic.com

### "Notion client not initialized"
- Tasks 4 & 5 require Notion API credentials
- Check NOTION_API_KEY and NOTION_DATABASE_ID in `.env`
- Ensure the database is shared with your integration

### "No video ideas generated"
- Claude may need more context. Add `--tool-info-file` or `--user-data-file`
- Try different topics
- Check your API quota/limits

### SVG Mindmap Not Displaying
- Ensure svgwrite is installed: `pip3 install svgwrite`
- SVG files can be opened in browsers, design tools, or video editors

## Workflow Example

Here's a complete content creation workflow:

### 1. Research & Plan (Weekly)
```bash
# Create 3 video ideas for the week
python3 main.py batch --type video --count 3 --topics "operations,growth,automation"
```

Result: 3 Notion pages with complete scripts and mindmaps, status "Script Ready"

### 2. Record Videos
- Review scripts in Notion
- Record videos using the scripts
- Save raw footage with descriptive names

### 3. Notify Editor
```bash
# Send to editor
python3 main.py notify-editor \
  --page-id <notion-page-id> \
  --files "2026-01-17_agency_automation.mp4" \
  --notes "Used mindmap at 5:30 and 12:45"
```

Result: Notion page updated to "Ready for Editing", editor assigned with checklist

### 4. Create Social Posts
```bash
# Create 5 posts while videos are being edited
python3 main.py batch --type post --count 5 --topics "quick wins,tips,case studies"
```

Result: 5 Notion pages with ready-to-publish post copy

## Tips for Best Results

1. **Be Specific with Topics**: Instead of "marketing", use "email marketing for B2B agencies"
2. **Provide Tool Context**: The more information about your tool, the better the content
3. **Use Batch Creation**: Generate multiple ideas, pick the best ones
4. **Review Before Recording**: Scripts are starting points - personalize them!
5. **Organize in Notion**: Use filters and views to manage your content pipeline

## System Requirements

- Python 3.8+
- Internet connection (for API calls)
- ~100MB disk space for dependencies
- ~10MB per content piece (scripts + mindmaps)

## Cost Estimates

Using Claude Sonnet 4.5:
- Video creation: ~$0.10-0.20 per video (research + script + mindmap)
- Post creation: ~$0.03-0.05 per post
- Batch of 10 videos: ~$1-2

*Costs are estimates and depend on content length and complexity.*

## Support & Contributions

For issues, feature requests, or contributions:
1. Check existing issues
2. Provide detailed error messages and logs from `logs/` directory
3. Include your Python version and OS

## License

MIT License - Feel free to modify and use for your agency!

## Credits

Built with:
- Claude AI (Anthropic)
- Notion API
- Python ecosystem (requests, beautifulsoup4, svgwrite, etc.)

---

**Ready to automate your content creation?** Start with `python3 main.py create-video --topics "your topic here"`
