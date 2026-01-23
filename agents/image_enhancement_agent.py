"""
Image Enhancement Agent
Enhances images using PIL - brightening, contrast, sharpness adjustments.
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime

from PIL import Image, ImageEnhance

from .base_agent import BaseAgent


class ImageEnhancementAgent(BaseAgent):
    """Agent for enhancing images using PIL."""

    def __init__(self, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize the Image Enhancement Agent.

        Args:
            model: Claude model (not used for basic enhancement, but kept for consistency)
        """
        super().__init__(name="Image Enhancement Agent", model=model)
        self.output_dir = "output/images/enhanced"
        os.makedirs(self.output_dir, exist_ok=True)

    def _load_image(self, image_path: str) -> Optional[Image.Image]:
        """
        Load an image from path.

        Args:
            image_path: Path to the image file

        Returns:
            PIL Image object or None if failed
        """
        try:
            if not os.path.exists(image_path):
                self.logger.error(f"Image not found: {image_path}")
                return None
            return Image.open(image_path)
        except Exception as e:
            self.logger.error(f"Failed to load image: {e}")
            return None

    def _save_image(
        self,
        image: Image.Image,
        original_path: str,
        suffix: str = "enhanced"
    ) -> str:
        """
        Save enhanced image with timestamp.

        Args:
            image: PIL Image to save
            original_path: Original image path (for naming)
            suffix: Suffix for output filename

        Returns:
            Path to saved image
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        basename = os.path.splitext(os.path.basename(original_path))[0]
        extension = os.path.splitext(original_path)[1] or ".png"

        # Ensure extension is valid for PIL
        if extension.lower() not in ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif']:
            extension = '.png'

        output_filename = f"{basename}_{suffix}_{timestamp}{extension}"
        output_path = os.path.join(self.output_dir, output_filename)

        # Convert RGBA to RGB for JPEG
        if extension.lower() in ['.jpg', '.jpeg'] and image.mode == 'RGBA':
            image = image.convert('RGB')

        image.save(output_path, quality=95)
        self.logger.info(f"Saved enhanced image: {output_path}")
        return output_path

    def brighten(
        self,
        image_path: str,
        factor: float = 1.3
    ) -> Dict[str, Any]:
        """
        Brighten an image.

        Args:
            image_path: Path to the image
            factor: Brightness factor (1.0 = original, >1 = brighter, <1 = darker)

        Returns:
            Dictionary with result
        """
        self.logger.info(f"Brightening image by factor {factor}: {image_path}")

        image = self._load_image(image_path)
        if image is None:
            return {"error": "Failed to load image", "status": "error"}

        enhancer = ImageEnhance.Brightness(image)
        enhanced = enhancer.enhance(factor)

        output_path = self._save_image(enhanced, image_path, f"bright_{factor}")

        return {
            "original_path": image_path,
            "output_path": output_path,
            "enhancement": "brightness",
            "factor": factor,
            "status": "success"
        }

    def adjust_contrast(
        self,
        image_path: str,
        factor: float = 1.2
    ) -> Dict[str, Any]:
        """
        Adjust image contrast.

        Args:
            image_path: Path to the image
            factor: Contrast factor (1.0 = original, >1 = more contrast)

        Returns:
            Dictionary with result
        """
        self.logger.info(f"Adjusting contrast by factor {factor}: {image_path}")

        image = self._load_image(image_path)
        if image is None:
            return {"error": "Failed to load image", "status": "error"}

        enhancer = ImageEnhance.Contrast(image)
        enhanced = enhancer.enhance(factor)

        output_path = self._save_image(enhanced, image_path, f"contrast_{factor}")

        return {
            "original_path": image_path,
            "output_path": output_path,
            "enhancement": "contrast",
            "factor": factor,
            "status": "success"
        }

    def sharpen(
        self,
        image_path: str,
        factor: float = 1.5
    ) -> Dict[str, Any]:
        """
        Sharpen an image.

        Args:
            image_path: Path to the image
            factor: Sharpness factor (1.0 = original, >1 = sharper)

        Returns:
            Dictionary with result
        """
        self.logger.info(f"Sharpening by factor {factor}: {image_path}")

        image = self._load_image(image_path)
        if image is None:
            return {"error": "Failed to load image", "status": "error"}

        enhancer = ImageEnhance.Sharpness(image)
        enhanced = enhancer.enhance(factor)

        output_path = self._save_image(enhanced, image_path, f"sharp_{factor}")

        return {
            "original_path": image_path,
            "output_path": output_path,
            "enhancement": "sharpness",
            "factor": factor,
            "status": "success"
        }

    def enhance_color(
        self,
        image_path: str,
        factor: float = 1.2
    ) -> Dict[str, Any]:
        """
        Enhance color saturation.

        Args:
            image_path: Path to the image
            factor: Color factor (1.0 = original, >1 = more saturated)

        Returns:
            Dictionary with result
        """
        self.logger.info(f"Enhancing color by factor {factor}: {image_path}")

        image = self._load_image(image_path)
        if image is None:
            return {"error": "Failed to load image", "status": "error"}

        enhancer = ImageEnhance.Color(image)
        enhanced = enhancer.enhance(factor)

        output_path = self._save_image(enhanced, image_path, f"color_{factor}")

        return {
            "original_path": image_path,
            "output_path": output_path,
            "enhancement": "color",
            "factor": factor,
            "status": "success"
        }

    def auto_enhance(
        self,
        image_path: str,
        brightness: float = 1.2,
        contrast: float = 1.1,
        sharpness: float = 1.2,
        color: float = 1.1
    ) -> Dict[str, Any]:
        """
        Apply balanced auto-enhancement with default settings.

        Args:
            image_path: Path to the image
            brightness: Brightness factor
            contrast: Contrast factor
            sharpness: Sharpness factor
            color: Color saturation factor

        Returns:
            Dictionary with result
        """
        self.logger.info(f"Auto-enhancing image: {image_path}")

        image = self._load_image(image_path)
        if image is None:
            return {"error": "Failed to load image", "status": "error"}

        # Apply all enhancements in sequence
        enhanced = image

        if brightness != 1.0:
            enhanced = ImageEnhance.Brightness(enhanced).enhance(brightness)

        if contrast != 1.0:
            enhanced = ImageEnhance.Contrast(enhanced).enhance(contrast)

        if sharpness != 1.0:
            enhanced = ImageEnhance.Sharpness(enhanced).enhance(sharpness)

        if color != 1.0:
            enhanced = ImageEnhance.Color(enhanced).enhance(color)

        output_path = self._save_image(enhanced, image_path, "auto_enhanced")

        return {
            "original_path": image_path,
            "output_path": output_path,
            "enhancement": "auto",
            "settings": {
                "brightness": brightness,
                "contrast": contrast,
                "sharpness": sharpness,
                "color": color
            },
            "status": "success"
        }

    def execute(
        self,
        image_path: str,
        brightness: float = 1.0,
        contrast: float = 1.0,
        sharpness: float = 1.0,
        color: float = 1.0,
        auto: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Enhance an image with specified settings.

        Args:
            image_path: Path to the image
            brightness: Brightness factor (1.0 = no change)
            contrast: Contrast factor (1.0 = no change)
            sharpness: Sharpness factor (1.0 = no change)
            color: Color saturation factor (1.0 = no change)
            auto: If True, use auto_enhance with default good settings

        Returns:
            Dictionary with enhancement results
        """
        self.logger.info(f"Enhancing image: {image_path}")

        if auto:
            return self.auto_enhance(image_path)

        image = self._load_image(image_path)
        if image is None:
            return {"error": "Failed to load image", "status": "error"}

        enhanced = image
        applied = []

        if brightness != 1.0:
            enhanced = ImageEnhance.Brightness(enhanced).enhance(brightness)
            applied.append(f"brightness={brightness}")

        if contrast != 1.0:
            enhanced = ImageEnhance.Contrast(enhanced).enhance(contrast)
            applied.append(f"contrast={contrast}")

        if sharpness != 1.0:
            enhanced = ImageEnhance.Sharpness(enhanced).enhance(sharpness)
            applied.append(f"sharpness={sharpness}")

        if color != 1.0:
            enhanced = ImageEnhance.Color(enhanced).enhance(color)
            applied.append(f"color={color}")

        if not applied:
            return {
                "error": "No enhancements specified. Use --brightness, --contrast, --sharpness, --color, or --auto",
                "status": "error"
            }

        suffix = "_".join(applied).replace("=", "")
        output_path = self._save_image(enhanced, image_path, suffix)

        return {
            "original_path": image_path,
            "output_path": output_path,
            "enhancements_applied": applied,
            "settings": {
                "brightness": brightness,
                "contrast": contrast,
                "sharpness": sharpness,
                "color": color
            },
            "status": "success"
        }
