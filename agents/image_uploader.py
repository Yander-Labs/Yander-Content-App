"""
Image Uploader Module
Uploads images to permanent hosting services (Imgur).
"""

import os
import base64
import requests
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class ImageUploader:
    """Uploads images to Imgur for permanent hosting."""

    # Imgur's anonymous upload endpoint
    IMGUR_UPLOAD_URL = "https://api.imgur.com/3/image"

    # Default client ID for anonymous uploads
    # This is a public client ID - for production, use your own
    DEFAULT_CLIENT_ID = "546c25a59c58ad7"

    def __init__(self, client_id: Optional[str] = None):
        """
        Initialize the uploader.

        Args:
            client_id: Imgur client ID. Uses default if not provided.
        """
        self.client_id = client_id or os.getenv("IMGUR_CLIENT_ID", self.DEFAULT_CLIENT_ID)
        self.headers = {"Authorization": f"Client-ID {self.client_id}"}

    def upload_file(self, file_path: str, title: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Upload a local image file to Imgur.

        Args:
            file_path: Path to the image file
            title: Optional title for the image

        Returns:
            Dict with 'url' and 'delete_hash' if successful, None otherwise
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        try:
            # Read and encode the image
            with open(file_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()

            # Prepare payload
            payload = {"image": image_data, "type": "base64"}
            if title:
                payload["title"] = title

            # Upload to Imgur
            response = requests.post(
                self.IMGUR_UPLOAD_URL,
                headers=self.headers,
                data=payload,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                result = {
                    "url": data["data"]["link"],
                    "delete_hash": data["data"]["deletehash"],
                    "id": data["data"]["id"],
                    "local_path": file_path
                }
                logger.info(f"Uploaded image: {result['url']}")
                return result
            else:
                logger.error(f"Imgur upload failed: {data}")
                return None

        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return None

    def upload_multiple(self, file_paths: List[str], titles: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Upload multiple images.

        Args:
            file_paths: List of paths to image files
            titles: Optional list of titles (same length as file_paths)

        Returns:
            List of upload results (only successful uploads)
        """
        results = []
        for i, path in enumerate(file_paths):
            title = titles[i] if titles and i < len(titles) else None
            result = self.upload_file(path, title)
            if result:
                results.append(result)
        return results


def upload_image(file_path: str, title: Optional[str] = None) -> Optional[str]:
    """
    Convenience function to upload a single image and return URL.

    Args:
        file_path: Path to the image file
        title: Optional title

    Returns:
        Permanent URL if successful, None otherwise
    """
    uploader = ImageUploader()
    result = uploader.upload_file(file_path, title)
    return result["url"] if result else None


if __name__ == "__main__":
    # Test upload
    import sys
    if len(sys.argv) > 1:
        url = upload_image(sys.argv[1])
        if url:
            print(f"Uploaded: {url}")
        else:
            print("Upload failed")
    else:
        print("Usage: python image_uploader.py <image_path>")
