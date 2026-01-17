# API Setup Guide

Complete guide for setting up all API integrations.

## Table of Contents

1. [Anthropic API (Required)](#anthropic-api)
2. [Notion API (Optional - Tasks 4 & 5)](#notion-api)
3. [Testing Your Setup](#testing-your-setup)

---

## Anthropic API

**Required for:** All features
**Cost:** Pay-as-you-go (est. $0.10-0.20 per video, $0.03-0.05 per post)

### Step-by-Step Setup

#### 1. Create Account

1. Go to [https://console.anthropic.com](https://console.anthropic.com)
2. Click "Sign Up" (or "Sign In" if you have an account)
3. Complete registration with email
4. Verify your email

#### 2. Add Payment Method

1. Go to Settings → Billing
2. Click "Add Payment Method"
3. Enter credit card details
4. Set up usage limits (recommended: $10-50/month for testing)

#### 3. Create API Key

1. Go to [Settings → API Keys](https://console.anthropic.com/settings/keys)
2. Click "Create Key"
3. Give it a name (e.g., "Content Creation Agents")
4. Copy the key immediately (starts with `sk-ant-`)
5. Store it securely - you won't see it again!

#### 4. Add to .env File

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 5. Test It

```bash
python3 -c "from anthropic import Anthropic; c=Anthropic(); print('✓ API key works!')"
```

### Billing & Costs

- **Claude Sonnet 4.5** pricing:
  - Input: $3 per million tokens
  - Output: $15 per million tokens

- **Typical usage:**
  - Video creation: ~50K tokens → ~$0.15
  - Post creation: ~10K tokens → ~$0.03
  - Batch of 10 videos: ~$1.50

- **Monitor usage:** [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing)

---

## Notion API

**Required for:** Tasks 4 (Notion database) and 5 (Editor notifications)
**Cost:** Free

### Overview

Notion integration allows the system to:
- Create pages in your database with scripts and ideas
- Organize all content in one place
- Assign tasks to your video editor
- Track content status (Script Ready → Recording → Editing → Published)

### Step-by-Step Setup

#### 1. Create Integration

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "+ New integration"
3. Fill in details:
   - **Name:** Content Creation Agents
   - **Associated workspace:** Select your workspace
   - **Type:** Internal integration
4. Click "Submit"
5. Copy the "Internal Integration Token" (starts with `secret_`)
6. Add to `.env`:
   ```
   NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### 2. Create Content Database

##### Option A: Use Template (Recommended)

1. Duplicate this template: [Coming soon - create manually for now]

##### Option B: Create Manually

1. In Notion, create a new page
2. Type `/database` and select "Database - Full page"
3. Name it "Content Calendar" or similar
4. Add these properties (click "+ New property"):

| Property Name | Type | Options |
|--------------|------|---------|
| Title | Title | (default) |
| Type | Select | Video, Post, Editing Task |
| Status | Select | Script Ready, Recording, Ready for Editing, In Editing, Published |
| Target Length | Number | - |
| Word Count | Number | - |
| Keywords | Multi-select | - |
| Platform | Select | YouTube, LinkedIn, Twitter, Blog |
| Created Date | Date | - |
| Recording Date | Date | - |
| Due Date | Date | - |
| Priority | Select | Low, Medium, High |
| Assigned To | Person | - |

#### 3. Share Database with Integration

1. Open your database
2. Click "..." (three dots) in top right
3. Select "Add connections"
4. Search for "Content Creation Agents"
5. Click to connect

⚠️ **Important:** The integration won't work until you share the database!

#### 4. Get Database ID

1. Open your database as a full page
2. Copy the URL from browser address bar
3. URL format: `https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=yyyyyyy`
4. The database ID is the `xxxxx` part (32 characters, may contain hyphens)
5. Add to `.env`:
   ```
   NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Example:**
```
URL: https://www.notion.so/myworkspace/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6?v=...
Database ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

#### 5. Get Video Editor's User ID (Optional)

Only needed for automatic editor assignment (Task 5).

1. Open Notion
2. Click on your workspace name (top left) → Settings & members
3. Go to "Members" tab
4. Find your video editor's name
5. Right-click their name → "Copy link"
6. Extract the user ID from the URL
7. Add to `.env`:
   ```
   VIDEO_EDITOR_NOTION_USER_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### 6. Test Notion Connection

```bash
python3 -c "from notion_client import Client; import os; from dotenv import load_dotenv; load_dotenv(); c=Client(auth=os.getenv('NOTION_API_KEY')); print('✓ Notion connection works!')"
```

### Troubleshooting Notion Setup

#### "object not found" Error

**Cause:** Database not shared with integration

**Fix:**
1. Open database in Notion
2. Click "..." → "Add connections"
3. Select your integration

#### "Invalid database_id"

**Cause:** Wrong database ID format

**Fix:**
- Database ID should be 32 characters (with or without hyphens)
- Copy from the URL, not the page title
- Remove any `?v=` query parameters

#### Integration Not Showing Up

**Cause:** Integration created in wrong workspace

**Fix:**
1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Check the "Associated workspace"
3. Create new integration in correct workspace

---

## Testing Your Setup

### Minimal Test (Anthropic Only)

```bash
python3 main.py create-video --topics "test topic" --tone professional
```

Expected output:
```
✓ Content Creation Orchestrator initialized
All agents loaded and ready

============================================================
CREATING VIDEO CONTENT
============================================================

[1/5] Researching content ideas...
✓ Selected idea: ...

[2/5] Writing video script...
✓ Script complete (15 minutes)

[3/5] Generating mindmap...
✓ Mindmap saved: output/mindmaps/mindmap_20260117_123456.svg

[4/5] Creating Notion database entry...
✗ Notion entry creation failed

[5/5] Video content package complete!
```

If you see the above (even with Notion failure), Anthropic API is working! ✓

### Full Test (With Notion)

```bash
python3 main.py create-video --topics "marketing automation" --tone professional
```

Expected output:
```
...
[4/5] Creating Notion database entry...
✓ Notion page created: https://notion.so/abc123

[5/5] Video content package complete!
```

If you see a Notion URL, everything works! ✓✓

### Test Editor Notification

First, create a video to get a page ID:
```bash
python3 main.py create-video --topics "test"
# Note the Notion page_id from output
```

Then test notification:
```bash
python3 main.py notify-editor \
  --page-id <your-page-id> \
  --files "test_video.mp4" \
  --notes "Test notification"
```

Check Notion - the page should update to "Ready for Editing"!

---

## Environment File Reference

Complete `.env` file example:

```bash
# Required - Anthropic API
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional - Notion API (for Tasks 4 & 5)
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional - Editor assignment (for Task 5)
VIDEO_EDITOR_NOTION_USER_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional - Custom settings
CONTENT_TONE=professional
TARGET_AUDIENCE=marketing_agency_owners
DEFAULT_VIDEO_LENGTH=15
DEFAULT_POST_LENGTH=200
```

---

## Security Best Practices

### DO:
- ✅ Keep `.env` file private (it's in `.gitignore`)
- ✅ Use different API keys for development/production
- ✅ Set usage limits on Anthropic billing
- ✅ Rotate keys periodically
- ✅ Use environment variables, never hardcode keys

### DON'T:
- ❌ Commit `.env` to git
- ❌ Share API keys in screenshots/demos
- ❌ Use production keys for testing
- ❌ Leave old keys active after rotation

---

## Cost Management

### Monitor Usage

**Anthropic:**
- Dashboard: [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing)
- Set monthly budgets
- Get email alerts

**Notion:**
- Free for API usage
- Check workspace plan limits

### Optimize Costs

1. **Use batch operations** - More efficient than one-at-a-time
2. **Reduce temperature** in config - Less creative = fewer tokens
3. **Shorten max_tokens** - But may truncate long scripts
4. **Cache tool info** - Don't regenerate same research

### Expected Monthly Costs

| Usage | Videos/Month | Posts/Month | Est. Cost |
|-------|--------------|-------------|-----------|
| Light | 4-8 | 8-16 | $2-5 |
| Medium | 12-20 | 20-40 | $10-20 |
| Heavy | 40+ | 80+ | $30-50 |

---

## Getting Help

### Check Logs

```bash
# View agent logs
ls logs/
cat logs/research_agent.log
cat logs/notion_agent.log
```

### Common Issues

See [README.md#troubleshooting](README.md#troubleshooting)

### Still Stuck?

Include in your issue report:
1. Error message
2. Command you ran
3. Relevant logs from `logs/` directory
4. Python version: `python3 --version`
5. OS: `uname -a` (Mac/Linux) or `ver` (Windows)

---

**Setup complete!** Return to [README.md](README.md) for usage examples.
