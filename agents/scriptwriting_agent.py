"""
Scriptwriting Agent
Writes compelling scripts for videos and copy for posts that hook and educate.
"""

import json
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from datetime import datetime


class ScriptwritingAgent(BaseAgent):
    """Agent that writes video scripts and post copy for marketing content."""

    def __init__(self):
        super().__init__(name="Scriptwriting Agent")
        self.system_prompt = """You are an expert scriptwriter and copywriter specializing in marketing agency content.

Your expertise includes:
- Writing engaging YouTube video scripts (10-30 minutes)
- Crafting compelling text-based posts (150+ words)
- Creating powerful hooks that grab attention
- Educational content about operations, marketing, and growth
- Storytelling that resonates with marketing agency owners

Script Structure for Videos:
1. HOOK (first 15-20 seconds) - Grab attention immediately with a problem/result
2. EARLY CTA (5-10 seconds) - Ask viewers to like/subscribe/engage BEFORE they lose interest
3. INTRO (30-45 seconds) - Set expectations, intro yourself/topic
4. MAIN CONTENT (80-90% of video) - Deliver value with clear segments
5. FINAL CTA (30-60 seconds) - What should viewers do next (try tool, book call, etc.)

Post Structure:
1. HOOK (first 1-2 sentences) - Grab attention
2. MAIN BODY - Deliver insights, tell story, educate
3. KEY TAKEAWAYS - Bullet points or summary
4. CALL TO ACTION - Engage, comment, try something

Style Guidelines:
- Conversational yet professional tone
- Use concrete examples and case studies
- Include specific numbers and data when possible
- Address pain points directly
- Provide actionable advice
- Use formatting (bold, italics, lists) strategically in posts

Output Format:
Return scripts/copy in structured JSON format with clear sections."""

    def write_video_script(self,
                           idea: Dict[str, Any],
                           tone: str = "professional",
                           target_length: int = 15) -> Dict[str, Any]:
        """
        Write a video script based on a content idea.

        Args:
            idea: Content idea dictionary from research agent
            tone: Tone of the script (professional, casual, educational)
            target_length: Target length in minutes

        Returns:
            Dictionary containing the complete script
        """
        self.logger.info(f"Writing video script for: {idea.get('title', 'Untitled')}")

        user_message = f"""Write a complete video script for the following content idea:

TITLE: {idea.get('title', 'Untitled')}
DESCRIPTION: {idea.get('description', '')}
HOOK CONCEPT: {idea.get('hook', '')}
KEY POINTS TO COVER:
{chr(10).join(f"- {point}" for point in idea.get('key_points', []))}

TARGET LENGTH: {target_length} minutes
TONE: {tone}
AUDIENCE: Marketing agency owners and operators

Return the script in this JSON structure:
{{
  "title": "string",
  "estimated_length_minutes": number,
  "hook": {{
    "duration_seconds": 20,
    "script": "string"
  }},
  "early_cta": {{
    "duration_seconds": 10,
    "script": "string (ask viewers to like, subscribe, comment - keep it brief and natural)"
  }},
  "intro": {{
    "duration_seconds": 45,
    "script": "string"
  }},
  "main_sections": [
    {{
      "section_title": "string",
      "duration_minutes": number,
      "script": "string",
      "visual_notes": "string (suggestions for what to show on screen)"
    }}
  ],
  "call_to_action": {{
    "duration_seconds": 45,
    "script": "string"
  }},
  "notes": {{
    "total_duration_estimate": "string",
    "b_roll_suggestions": ["string"],
    "on_screen_text_suggestions": ["string"]
  }}
}}"""

        response = self.call_claude(
            system_prompt=self.system_prompt,
            user_message=user_message,
            max_tokens=8192,
            temperature=0.8
        )

        # Parse response
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            script = json.loads(json_str)
            self.logger.info(f"Script complete: {script.get('title', 'Untitled')}")

            return script

        except Exception as e:
            self.logger.error(f"Error parsing script: {str(e)}")
            return {
                "error": str(e),
                "raw_response": response
            }

    def write_post_copy(self,
                       idea: Dict[str, Any],
                       tone: str = "professional",
                       target_length: int = 200) -> Dict[str, Any]:
        """
        Write post copy based on a content idea.

        Args:
            idea: Content idea dictionary from research agent
            tone: Tone of the copy (professional, casual, educational)
            target_length: Target length in words

        Returns:
            Dictionary containing the complete post copy
        """
        self.logger.info(f"Writing post copy for: {idea.get('title', 'Untitled')}")

        user_message = f"""Write compelling post copy for the following content idea:

TITLE: {idea.get('title', 'Untitled')}
DESCRIPTION: {idea.get('description', '')}
HOOK CONCEPT: {idea.get('hook', '')}
KEY POINTS TO COVER:
{chr(10).join(f"- {point}" for point in idea.get('key_points', []))}

TARGET LENGTH: {target_length} words
TONE: {tone}
AUDIENCE: Marketing agency owners and operators
PLATFORM: LinkedIn / Twitter / General text post

Return the post in this JSON structure:
{{
  "title": "string",
  "hook": "string (first 1-2 sentences)",
  "body": "string (main content with formatting)",
  "key_takeaways": ["string"],
  "call_to_action": "string",
  "full_post": "string (complete formatted post ready to publish)",
  "hashtags": ["string"],
  "word_count": number,
  "notes": {{
    "best_platform": "string",
    "posting_tips": "string"
  }}
}}"""

        response = self.call_claude(
            system_prompt=self.system_prompt,
            user_message=user_message,
            max_tokens=4096,
            temperature=0.8
        )

        # Parse response
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            post = json.loads(json_str)
            self.logger.info(f"Post complete: {post.get('title', 'Untitled')}")

            return post

        except Exception as e:
            self.logger.error(f"Error parsing post: {str(e)}")
            return {
                "error": str(e),
                "raw_response": response
            }

    def execute(self,
                content_type: str = "video",
                idea: Optional[Dict[str, Any]] = None,
                tone: str = "professional",
                target_length: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute scriptwriting for a content idea.

        Args:
            content_type: Type of content ("video" or "post")
            idea: Content idea dictionary
            tone: Tone of the content
            target_length: Target length (minutes for video, words for post)

        Returns:
            Dictionary containing the script or post copy
        """
        if not idea:
            raise ValueError("Content idea is required")

        if content_type == "video":
            if target_length is None:
                target_length = idea.get('target_length', 15)
            result = self.write_video_script(idea, tone, target_length)

            # Save script
            output_path = self.save_output(
                result,
                f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "output/scripts"
            )
            result['output_file'] = output_path

        elif content_type == "post":
            if target_length is None:
                target_length = idea.get('target_length', 200)
            result = self.write_post_copy(idea, tone, target_length)

            # Save post
            output_path = self.save_output(
                result,
                f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "output/scripts"
            )
            result['output_file'] = output_path

        else:
            raise ValueError(f"Invalid content_type: {content_type}")

        return result


if __name__ == "__main__":
    # Example usage
    agent = ScriptwritingAgent()

    # Example video idea
    video_idea = {
        "title": "5 Automation Workflows Every Marketing Agency Needs",
        "description": "Show agency owners how to automate repetitive tasks",
        "hook": "You're wasting 15 hours per week on tasks that could be automated",
        "key_points": [
            "Client onboarding automation",
            "Report generation",
            "Invoice processing",
            "Lead qualification",
            "Social media scheduling"
        ],
        "target_length": 15
    }

    script = agent.execute(content_type="video", idea=video_idea)
    print(json.dumps(script, indent=2))
