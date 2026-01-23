"""
Daily Content Agent
Autonomous agent that generates and publishes content daily.
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from anthropic import Anthropic
from .base_agent import BaseAgent
from .notion_agent import NotionAgent


class DailyContentAgent(BaseAgent):
    """Agent that autonomously generates daily content and publishes to Notion."""

    def __init__(self):
        super().__init__(name="Daily Content Agent")

        # Initialize Anthropic client
        self.client = Anthropic()
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

        # Initialize Notion agent
        self.notion_agent = NotionAgent()

        # Load themes configuration
        self.themes = self._load_themes()

        # Load creator context
        self.creator_context = self._load_creator_context()

        # Load style references
        self.style_references = self._load_style_references()

    def _load_themes(self) -> Dict[str, Any]:
        """Load themes configuration from file."""
        themes_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "daily_content_themes.json"
        )
        try:
            with open(themes_path, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load themes: {e}")
            return {"themes": [], "last_used_index": 0}

    def _save_themes(self):
        """Save updated themes configuration (for rotation tracking)."""
        themes_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "daily_content_themes.json"
        )
        try:
            with open(themes_path, "w") as f:
                json.dump(self.themes, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save themes: {e}")

    def _load_creator_context(self) -> str:
        """Load Jordan Hayes context from file."""
        context_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "jordan_hayes_info.txt"
        )
        try:
            with open(context_path, "r") as f:
                return f.read()
        except Exception as e:
            self.logger.warning(f"Could not load creator context: {e}")
            return ""

    def _load_style_references(self) -> Dict[str, Any]:
        """Load style references from file."""
        style_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "content_style_references.json"
        )
        try:
            with open(style_path, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load style references: {e}")
            return {}

    def select_theme(self) -> Dict[str, Any]:
        """Select the next theme in rotation."""
        if not self.themes.get("themes"):
            return {
                "name": "general",
                "display_name": "General Agency Content",
                "keywords": ["agency", "growth", "team"],
                "prompts": ["Share an insight from running your agency"]
            }

        themes_list = self.themes["themes"]
        current_index = self.themes.get("last_used_index", 0)

        # Get current theme
        theme = themes_list[current_index]

        # Update index for next time
        self.themes["last_used_index"] = (current_index + 1) % len(themes_list)
        self._save_themes()

        self.logger.info(f"Selected theme: {theme['display_name']}")
        return theme

    def get_recent_post_titles(self, days: int = 30) -> List[str]:
        """Get titles of recent posts to avoid duplicates."""
        return self.notion_agent.get_page_titles(days=days)

    def generate_ideas(self, theme: Dict[str, Any], existing_titles: List[str], count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate post ideas based on theme and avoiding duplicates.

        Args:
            theme: Theme configuration
            existing_titles: List of existing post titles to avoid
            count: Number of ideas to generate

        Returns:
            List of idea dictionaries
        """
        self.logger.info(f"Generating {count} ideas for theme: {theme['display_name']}")

        # Build prompt
        prompt = f"""You are a content strategist for Jordan Hayes, owner of Hayes Media.

CREATOR CONTEXT:
{self.creator_context}

TODAY'S THEME: {theme['display_name']}
Keywords: {', '.join(theme.get('keywords', []))}
Prompt ideas: {', '.join(theme.get('prompts', []))}

EXISTING POST TITLES (avoid similar topics):
{chr(10).join(existing_titles[-20:]) if existing_titles else 'None yet'}

Generate {count} unique LinkedIn post ideas for this theme. Each idea should:
1. Have a strong, attention-grabbing hook (under 10 words)
2. Be based on real agency experience (not generic advice)
3. Provide actionable value for agency owners
4. Be different from existing posts listed above

Return as JSON array with this structure:
[
  {{
    "title": "Short descriptive title",
    "hook": "The opening line that grabs attention",
    "angle": "Brief description of the post's unique angle",
    "key_points": ["Point 1", "Point 2", "Point 3"]
  }}
]

Return ONLY the JSON array, no other text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()

            # Parse JSON from response
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]

            ideas = json.loads(content)
            self.logger.info(f"Generated {len(ideas)} ideas")
            return ideas

        except Exception as e:
            self.logger.error(f"Error generating ideas: {e}")
            return []

    def write_post(self, idea: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Write a full post from an idea.

        Args:
            idea: Post idea dictionary
            theme: Theme configuration

        Returns:
            Full post dictionary with hook, content, takeaways
        """
        self.logger.info(f"Writing post: {idea.get('title', 'Untitled')}")

        # Get style patterns
        style_patterns = ""
        if self.style_references.get("pattern_analysis"):
            patterns = self.style_references["pattern_analysis"]
            style_patterns = f"""
WRITING STYLE PATTERNS:
- Hook styles: {', '.join(patterns.get('common_hooks', []))}
- Content structures: {', '.join(patterns.get('content_structures', []))}
- Engagement tactics: {', '.join(patterns.get('engagement_tactics', []))}
"""

        prompt = f"""You are writing a LinkedIn post for Jordan Hayes, owner of Hayes Media.

CREATOR CONTEXT:
{self.creator_context}

{style_patterns}

POST IDEA:
Title: {idea.get('title', '')}
Hook: {idea.get('hook', '')}
Angle: {idea.get('angle', '')}
Key Points: {', '.join(idea.get('key_points', []))}

THEME: {theme['display_name']}

Write a complete LinkedIn post following these guidelines:
1. Start with the hook provided (or improve it if needed)
2. Keep paragraphs short - 1-3 sentences max
3. Use line breaks liberally for readability
4. Be direct and confident - speak from experience
5. Include specific examples or numbers where possible
6. End with a thought-provoking question or clear takeaway
7. NO emojis, NO hashtags
8. Total length: 150-300 words

Return as JSON:
{{
  "hook": "The opening line",
  "full_post": "The complete post text including hook",
  "key_takeaways": ["Takeaway 1", "Takeaway 2", "Takeaway 3"]
}}

Return ONLY the JSON, no other text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()

            # Parse JSON from response
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]

            post = json.loads(content)
            post["title"] = idea.get("title", "Untitled Post")
            post["theme"] = theme["display_name"]

            self.logger.info(f"Post written: {len(post.get('full_post', ''))} characters")
            return post

        except Exception as e:
            self.logger.error(f"Error writing post: {e}")
            return {}

    def publish_to_notion(self, post: Dict[str, Any]) -> Optional[str]:
        """
        Publish a post to Notion.

        Args:
            post: Post dictionary with hook, full_post, key_takeaways

        Returns:
            Notion page URL if successful
        """
        self.logger.info(f"Publishing to Notion: {post.get('title', 'Untitled')}")

        idea = {
            "title": post.get("title", "Untitled Post"),
            "theme": post.get("theme", "General")
        }

        result = self.notion_agent.create_post_entry(idea, post)

        if result:
            url = f"https://notion.so/{result.replace('-', '')}"
            self.logger.info(f"Published to Notion: {url}")
            return url
        else:
            self.logger.error("Failed to publish to Notion")
            return None

    def run_daily(self, post_count: int = 3) -> List[Dict[str, Any]]:
        """
        Run the daily content generation workflow.

        Args:
            post_count: Number of posts to generate

        Returns:
            List of results with post info and Notion URLs
        """
        self.logger.info(f"Starting daily content generation for {post_count} posts")
        results = []

        try:
            # Get existing posts to avoid duplicates
            existing_titles = self.get_recent_post_titles(days=30)
            self.logger.info(f"Found {len(existing_titles)} existing posts to avoid")

            # Generate posts for different themes
            posts_created = 0
            themes_used = []

            while posts_created < post_count:
                # Select theme
                theme = self.select_theme()

                # Skip if we've already used this theme this run
                if theme["name"] in themes_used and len(self.themes.get("themes", [])) > post_count:
                    continue

                themes_used.append(theme["name"])

                # Generate ideas
                ideas = self.generate_ideas(theme, existing_titles, count=3)

                if not ideas:
                    self.logger.warning(f"No ideas generated for theme: {theme['display_name']}")
                    continue

                # Write and publish the best idea
                idea = ideas[0]  # Take top idea
                post = self.write_post(idea, theme)

                if not post:
                    self.logger.warning(f"Failed to write post for: {idea.get('title')}")
                    continue

                # Publish to Notion
                url = self.publish_to_notion(post)

                if url:
                    # Add to existing titles to avoid duplicates in same run
                    existing_titles.append(post.get("title", ""))

                    results.append({
                        "title": post.get("title"),
                        "theme": theme["display_name"],
                        "hook": post.get("hook"),
                        "notion_url": url,
                        "success": True
                    })
                    posts_created += 1
                    self.logger.info(f"Created post {posts_created}/{post_count}: {post.get('title')}")
                else:
                    results.append({
                        "title": post.get("title"),
                        "theme": theme["display_name"],
                        "error": "Failed to publish to Notion",
                        "success": False
                    })

            self.logger.info(f"Daily content generation complete: {posts_created} posts created")
            return results

        except Exception as e:
            self.logger.error(f"Error in daily content generation: {e}")
            return results

    def execute(self, post_count: int = 3) -> Dict[str, Any]:
        """
        Execute daily content generation.

        Args:
            post_count: Number of posts to generate

        Returns:
            Dictionary with results
        """
        results = self.run_daily(post_count=post_count)

        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]

        return {
            "total_requested": post_count,
            "successful": len(successful),
            "failed": len(failed),
            "posts": results,
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Test run
    agent = DailyContentAgent()
    results = agent.run_daily(post_count=1)
    print(json.dumps(results, indent=2))
