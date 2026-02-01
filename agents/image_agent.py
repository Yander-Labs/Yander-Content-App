"""
AI Image Generation Agent
Generates illustrations using Replicate API for video content.
"""

import os
import time
import replicate
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_agent import BaseAgent
from .image_uploader import ImageUploader


class ImageAgent(BaseAgent):
    """Agent that generates AI illustrations using Replicate."""

    # Default style prompt for consistent Notion-style illustrations
    DEFAULT_STYLE = (
        "flat 2D illustration style, grainy film texture, sketchy hairy pen stroke outlines, "
        "rough textured edges on all shapes, monochrome grayscale with subtle blue-gray tones, "
        "risograph print aesthetic, conceptual metaphorical imagery, minimalist playful style "
        "like Notion illustrations, editorial illustration, no 3D, no photorealistic, no text, no words"
    )

    def __init__(self, model: str = "black-forest-labs/flux-schnell"):
        """
        Initialize the Image Agent.

        Args:
            model: Replicate model to use. Options:
                - "black-forest-labs/flux-schnell" (fast, good quality)
                - "black-forest-labs/flux-dev" (slower, higher quality)
                - "stability-ai/sdxl" (stable diffusion)
        """
        super().__init__(name="Image Agent")

        self.api_token = os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            self.logger.warning("REPLICATE_API_TOKEN not found. Image generation will not work.")
            self.client = None
        else:
            os.environ["REPLICATE_API_TOKEN"] = self.api_token
            self.client = replicate

        self.model = model
        self.output_dir = "output/images"
        os.makedirs(self.output_dir, exist_ok=True)

        # Image uploader for permanent hosting
        self.uploader = ImageUploader()

    def generate_image(self,
                       concept: str,
                       style: Optional[str] = None,
                       aspect_ratio: str = "16:9",
                       save_locally: bool = True,
                       upload_to_imgur: bool = True) -> Optional[Dict[str, Any]]:
        """
        Generate an image for a given concept.

        Args:
            concept: The concept/scene to illustrate (e.g., "confused business owner looking at unequal workloads")
            style: Style prompt override. Uses DEFAULT_STYLE if not provided.
            aspect_ratio: Image aspect ratio ("1:1", "16:9", "9:16", "4:3")
            save_locally: Whether to download and save the image locally
            upload_to_imgur: Whether to upload to Imgur for permanent hosting (default True)

        Returns:
            Dictionary with image URL and local path if successful.
            If upload_to_imgur is True, 'url' will be the permanent Imgur URL.
        """
        if not self.client:
            self.logger.error("Replicate client not initialized")
            return None

        try:
            # Combine concept with style
            style_prompt = style or self.DEFAULT_STYLE
            full_prompt = f"{concept}, {style_prompt}"

            self.logger.info(f"Generating image for: {concept[:50]}...")

            # Generate image using Replicate
            if "flux" in self.model:
                output = self.client.run(
                    self.model,
                    input={
                        "prompt": full_prompt,
                        "aspect_ratio": aspect_ratio,
                        "output_format": "png",
                        "output_quality": 90,
                        "num_outputs": 1,
                    }
                )
            else:
                # SDXL fallback
                output = self.client.run(
                    self.model,
                    input={
                        "prompt": full_prompt,
                        "negative_prompt": "3D, photorealistic, photo, realistic, text, words, letters, watermark",
                        "width": 1024,
                        "height": 576 if aspect_ratio == "16:9" else 1024,
                        "num_outputs": 1,
                    }
                )

            # Get the image URL
            if isinstance(output, list) and len(output) > 0:
                image_url = str(output[0])
            else:
                image_url = str(output)

            self.logger.info(f"Generated image: {image_url}")

            result = {
                "url": image_url,
                "replicate_url": image_url,  # Keep original Replicate URL
                "concept": concept,
                "prompt": full_prompt,
            }

            # Download and save locally if requested
            if save_locally:
                local_path = self._download_image(image_url, concept)
                if local_path:
                    result["local_path"] = local_path

                    # Upload to Imgur for permanent hosting
                    if upload_to_imgur:
                        self.logger.info(f"Uploading to Imgur for permanent hosting...")
                        upload_result = self.uploader.upload_file(local_path, concept[:40])
                        if upload_result:
                            result["url"] = upload_result["url"]  # Use Imgur URL as primary
                            result["imgur_url"] = upload_result["url"]
                            self.logger.info(f"Permanent URL: {upload_result['url']}")
                        else:
                            self.logger.warning("Imgur upload failed, using temporary Replicate URL")

            return result

        except Exception as e:
            self.logger.error(f"Error generating image: {str(e)}")
            return None

    def _download_image(self, url: str, concept: str) -> Optional[str]:
        """
        Download an image from URL and save locally.

        Args:
            url: Image URL to download
            concept: Concept name for filename

        Returns:
            Local file path if successful
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Create filename from concept
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_name = "".join(c if c.isalnum() or c in "_ -" else "_" for c in concept[:40])
            filename = f"{safe_name}_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            self.logger.info(f"Saved image to: {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"Error downloading image: {str(e)}")
            return None

    def generate_section_images(self,
                                script: Dict[str, Any],
                                include_hook: bool = True,
                                include_intro: bool = False,
                                rate_limit_delay: float = 12.0) -> List[Dict[str, Any]]:
        """
        Generate images for all sections of a video script.

        Args:
            script: Video script dictionary with main_sections
            include_hook: Whether to generate an image for the hook
            include_intro: Whether to generate an image for the intro
            rate_limit_delay: Seconds to wait between API calls (default 12s for free tier)

        Returns:
            List of dictionaries with section titles and image data
        """
        if not self.client:
            self.logger.error("Replicate client not initialized")
            return []

        images = []
        is_first = True

        # Generate hook image
        if include_hook:
            hook_text = script.get('hook', {}).get('script', '')
            if hook_text:
                if not is_first:
                    self.logger.info(f"Waiting {rate_limit_delay}s for rate limit...")
                    time.sleep(rate_limit_delay)
                is_first = False

                concept = self._extract_visual_concept(hook_text, "Hook")
                image = self.generate_image(concept)
                if image:
                    images.append({
                        "section": "Hook",
                        "concept": concept,
                        **image
                    })

        # Generate intro image
        if include_intro:
            intro_text = script.get('intro', {}).get('script', '')
            if intro_text:
                if not is_first:
                    self.logger.info(f"Waiting {rate_limit_delay}s for rate limit...")
                    time.sleep(rate_limit_delay)
                is_first = False

                concept = self._extract_visual_concept(intro_text, "Intro")
                image = self.generate_image(concept)
                if image:
                    images.append({
                        "section": "Intro",
                        "concept": concept,
                        **image
                    })

        # Generate images for main sections
        for section in script.get('main_sections', []):
            section_title = section.get('section_title', 'Section')
            section_text = section.get('script', '')

            if not is_first:
                self.logger.info(f"Waiting {rate_limit_delay}s for rate limit...")
                time.sleep(rate_limit_delay)
            is_first = False

            concept = self._extract_visual_concept(section_text, section_title)
            image = self.generate_image(concept)
            if image:
                images.append({
                    "section": section_title,
                    "concept": concept,
                    **image
                })

        return images

    def _extract_visual_concept(self, text: str, section_title: str) -> str:
        """
        Extract a visual concept from script text for image generation.

        Creates a concise, visual description suitable for image generation.

        Args:
            text: Script text to extract concept from
            section_title: Section title for context

        Returns:
            Visual concept description
        """
        # Map common section themes to visual concepts
        concept_mappings = {
            "hook": "attention-grabbing scene",
            "intro": "person introducing themselves",
            "client count": "business owner looking at client folders of different sizes",
            "workload": "scale or balance showing unequal distribution of work",
            "remote": "remote worker at laptop with hidden stress",
            "metrics": "dashboard or measurement tools showing data",
            "rebalancing": "person redistributing items on a scale",
            "systems": "gears and processes working together",
            "yander": "software dashboard showing team health metrics",
            "retention": "hand holding onto valued employees",
            "collaboration": "team members working together then drifting apart",
            "communication": "message bubbles changing in size and frequency",
            "disengagement": "person fading or becoming transparent",
            "burnout": "person overwhelmed with tasks",
            "prevention": "shield or protective barrier",
            "leadership": "person transitioning from worker to conductor",
            "scaling": "business growing from small to large",
            "margin": "money flowing through a funnel",
            "reinvest": "seeds being planted for growth",
            "specialize": "focusing lens on specific target",
            "personal brand": "person stepping into spotlight",
            "identity": "reflection showing different versions of self",
        }

        # Find matching concept
        title_lower = section_title.lower()
        text_lower = text.lower()

        for keyword, visual in concept_mappings.items():
            if keyword in title_lower or keyword in text_lower[:200]:
                return f"{visual}, business metaphor"

        # Default: create concept from section title
        return f"conceptual illustration of {section_title.lower()}, business metaphor"

    def execute(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute image generation for a video script.

        Args:
            script: Video script dictionary

        Returns:
            Dictionary with generated images
        """
        images = self.generate_section_images(script)

        return {
            "success": len(images) > 0,
            "images": images,
            "count": len(images)
        }


if __name__ == "__main__":
    # Test the image agent
    agent = ImageAgent()
    print("Image Agent initialized")

    if agent.client:
        test_result = agent.generate_image(
            "confused business owner looking at three folders of different sizes representing unequal workloads"
        )
        print(f"Test result: {test_result}")
    else:
        print("No REPLICATE_API_TOKEN found. Add it to your .env file.")
