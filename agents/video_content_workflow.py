"""
Video Content Workflow
Unified workflow for creating video scripts with Notion pages, talking points, and AI images.
"""

import os
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime

from .notion_agent import NotionAgent
from .image_agent import ImageAgent
from .base_agent import BaseAgent


class VideoContentWorkflow(BaseAgent):
    """
    Unified workflow for creating complete video content packages.

    Creates:
    1. Notion page with full script
    2. AI-generated images for each section
    3. Talking Points subpage with bullet points and images
    """

    def __init__(self, generate_images: bool = True):
        """
        Initialize the video content workflow.

        Args:
            generate_images: Whether to generate AI images (requires REPLICATE_API_TOKEN)
        """
        super().__init__(name="Video Content Workflow")

        self.notion_agent = NotionAgent()
        self.generate_images = generate_images

        if generate_images:
            self.image_agent = ImageAgent()
            if not self.image_agent.client:
                self.logger.warning("REPLICATE_API_TOKEN not found. Images will be skipped.")
                self.generate_images = False
        else:
            self.image_agent = None

        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)

    def create_video_content(self,
                             script: Dict[str, Any],
                             save_locally: bool = True,
                             include_hook_image: bool = True,
                             include_intro_image: bool = False) -> Dict[str, Any]:
        """
        Create complete video content package.

        Args:
            script: Video script dictionary with title, hook, intro, main_sections, call_to_action
            save_locally: Whether to save script JSON locally
            include_hook_image: Whether to generate image for hook section
            include_intro_image: Whether to generate image for intro section

        Returns:
            Dictionary with page URLs, image count, and file paths
        """
        result = {
            "success": False,
            "title": script.get("title", "Untitled"),
            "notion_page_url": None,
            "talking_points_url": None,
            "images_generated": 0,
            "local_script_path": None,
        }

        try:
            title = script.get("title", "Untitled")
            self.logger.info(f"Creating video content for: {title}")

            # Step 1: Save script locally
            if save_locally:
                result["local_script_path"] = self._save_script_locally(script)
                self.logger.info(f"Saved script to: {result['local_script_path']}")

            # Step 2: Create Notion page with full script
            self.logger.info("Creating Notion page...")
            idea = {
                "title": title,
                "hook": script.get("hook", {}).get("script", ""),
                "key_points": [s.get("section_title", "") for s in script.get("main_sections", [])]
            }

            page_id = self.notion_agent.create_video_entry(idea, script)

            if not page_id:
                self.logger.error("Failed to create Notion page")
                return result

            result["notion_page_url"] = f"https://notion.so/{page_id.replace('-', '')}"
            self.logger.info(f"Created Notion page: {result['notion_page_url']}")

            # Step 3: Generate AI images (if enabled)
            images = []
            if self.generate_images and self.image_agent:
                self.logger.info("Generating AI images...")
                images = self.image_agent.generate_section_images(
                    script,
                    include_hook=include_hook_image,
                    include_intro=include_intro_image
                )
                result["images_generated"] = len(images)
                self.logger.info(f"Generated {len(images)} images")

            # Step 4: Create Talking Points subpage with images
            self.logger.info("Creating Talking Points subpage...")
            subpage_id = self.notion_agent.create_talking_points_subpage(
                parent_page_id=page_id,
                script=script,
                images=images
            )

            if subpage_id:
                result["talking_points_url"] = f"https://notion.so/{subpage_id.replace('-', '')}"
                self.logger.info(f"Created Talking Points: {result['talking_points_url']}")

            result["success"] = True
            return result

        except Exception as e:
            self.logger.error(f"Error in video content workflow: {str(e)}")
            return result

    def _save_script_locally(self, script: Dict[str, Any]) -> str:
        """Save script to local JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        title = script.get("title", "untitled")
        safe_title = "".join(c if c.isalnum() or c in "_ -" else "_" for c in title[:50]).lower()
        filename = f"script_{safe_title}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2)

        return filepath

    def execute(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the video content workflow."""
        return self.create_video_content(script)


def create_video_with_talking_points(script: Dict[str, Any],
                                     generate_images: bool = True,
                                     print_progress: bool = True) -> Dict[str, Any]:
    """
    Convenience function to create a complete video content package.

    Args:
        script: Video script dictionary
        generate_images: Whether to generate AI images
        print_progress: Whether to print progress to console

    Returns:
        Dictionary with URLs and status
    """
    if print_progress:
        print("=" * 60)
        print(f"CREATING VIDEO CONTENT")
        print(f"Title: {script.get('title', 'Untitled')}")
        print("=" * 60)

    workflow = VideoContentWorkflow(generate_images=generate_images)
    result = workflow.create_video_content(script)

    if print_progress:
        print()
        if result["success"]:
            print("SUCCESS!")
            print(f"  Notion Page: {result['notion_page_url']}")
            print(f"  Talking Points: {result['talking_points_url']}")
            print(f"  Images Generated: {result['images_generated']}")
            if result["local_script_path"]:
                print(f"  Local Script: {result['local_script_path']}")
        else:
            print("FAILED - Check logs for details")
        print("=" * 60)

    return result


if __name__ == "__main__":
    # Example usage
    example_script = {
        "title": "Test Video Script",
        "hook": {"script": "This is a test hook to grab attention."},
        "intro": {"script": "I'm testing the video content workflow."},
        "main_sections": [
            {"section_title": "Section 1", "script": "Content for section 1."},
            {"section_title": "Section 2", "script": "Content for section 2."},
        ],
        "call_to_action": {"script": "Subscribe and like!"}
    }

    result = create_video_with_talking_points(example_script, generate_images=False)
    print(f"\nResult: {result}")
