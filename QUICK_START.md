# Quick Start Guide

Get up and running with Content Creation Agents in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
cd ~/content-creation-agents
pip3 install -r requirements.txt
```

## Step 2: Get Your Anthropic API Key (2 minutes)

1. Visit [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Sign in (or create free account)
3. Click "Create Key"
4. Copy the key

## Step 3: Configure (1 minute)

```bash
# Copy the example file
cp .env.example .env

# Edit it
nano .env  # or use any text editor
```

Add your API key:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Save and exit (Ctrl+X, then Y, then Enter in nano)

## Step 4: Create Your First Video! (30 seconds)

```bash
python3 main.py create-video --topics "marketing automation tips"
```

That's it! 🎉

## What Just Happened?

The system just:
1. ✅ Researched 3 video ideas about marketing automation
2. ✅ Wrote a complete 15-minute video script with hook, intro, main content, and CTA
3. ✅ Generated a beautiful SVG mindmap visualization
4. ✅ Saved everything to the `output/` directory

## Check Your Results

```bash
# See the mindmap
open output/mindmaps/mindmap_*.svg

# See the full results
cat output/video_result_*.json | grep -A 5 "title"
```

## Next Steps

### Want Notion Integration?

Follow the [Notion Setup Guide](API_SETUP.md#notion-setup) (5-10 minutes)

### Create More Content

```bash
# Create a post
python3 main.py create-post --topics "agency growth strategies"

# Create 5 videos at once
python3 main.py batch --type video --count 5 --topics "operations,growth,automation"
```

### Customize

Edit `config/config.yaml` to change:
- Default video length
- Post word count
- Writing tone
- Agent behavior

## Common First-Time Issues

### "command not found: python3"
Try `python` instead:
```bash
python main.py create-video --topics "your topic"
```

### "No module named 'anthropic'"
Install dependencies:
```bash
pip3 install -r requirements.txt
```

### "ANTHROPIC_API_KEY not found"
Make sure you created the `.env` file and added your key!

## Full Documentation

See [README.md](README.md) for:
- Complete API setup (Notion, etc.)
- Advanced usage
- Python API examples
- Troubleshooting

---

**You're all set!** Start creating content with AI assistance. 🚀
