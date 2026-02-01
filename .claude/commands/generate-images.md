# Generate Images

Generate AI illustrations with permanent hosting for video content.

## Usage

```
/generate-images <concept or section description>
```

Or for multiple images from a script:
```
/generate-images --script <path-to-script.json>
```

## Instructions

You are generating images for video content that will be displayed in Notion. Follow these steps:

### For a single concept:

1. Parse the user's concept/description
2. Generate the image using ImageAgent with Imgur upload enabled
3. Return the permanent Imgur URL

```python
from dotenv import load_dotenv
load_dotenv()
from agents import ImageAgent

agent = ImageAgent()
result = agent.generate_image(
    concept="<user's concept>",
    upload_to_imgur=True  # This is the default
)

if result:
    print(f"Image generated!")
    print(f"Permanent URL: {result['url']}")
    print(f"Local path: {result.get('local_path', 'N/A')}")
```

### For a full script:

1. Load the script JSON
2. Generate images for each main section
3. Return all permanent URLs

```python
from dotenv import load_dotenv
load_dotenv()
from agents import ImageAgent
import json

agent = ImageAgent()

with open("<script_path>", "r") as f:
    script = json.load(f)

images = agent.generate_section_images(
    script,
    include_hook=True,
    include_intro=False,
    rate_limit_delay=12.0  # Free tier rate limit
)

for img in images:
    print(f"{img['section']}: {img['url']}")
```

### Image style

The default style creates Notion-like illustrations:
- Flat 2D illustration style
- Grainy film texture
- Sketchy pen stroke outlines
- Monochrome grayscale with blue-gray tones
- Conceptual/metaphorical imagery

### Output format

Return to the user:
1. The permanent Imgur URL(s)
2. The local file path(s) for reference
3. A brief description of what was generated

### Rate limits

- Replicate free tier: ~10 requests per minute
- Default delay between images: 12 seconds
- Imgur: 50 uploads per hour (anonymous)

## Examples

**Single image:**
```
/generate-images confused business owner looking at unequal workloads on a scale
```

**From script:**
```
/generate-images --script output/scripts/communication_video.json
```

**Custom concept:**
```
/generate-images team members collaborating around a whiteboard, remote work setting
```
