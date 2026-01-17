"""
Notion Integration Agent
Manages content in Notion databases for video/post ideas and editor workflow.
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from notion_client import Client
from .base_agent import BaseAgent


class NotionAgent(BaseAgent):
    """Agent that manages content in Notion databases."""

    def __init__(self):
        super().__init__(name="Notion Agent")

        # Initialize Notion client
        notion_api_key = os.getenv("NOTION_API_KEY")
        if not notion_api_key:
            self.logger.warning("NOTION_API_KEY not found. Notion integration will not work.")
            self.notion_client = None
        else:
            self.notion_client = Client(auth=notion_api_key)

        self.database_id = os.getenv("NOTION_DATABASE_ID")

    def create_video_entry(self,
                          idea: Dict[str, Any],
                          script: Dict[str, Any],
                          mindmap_path: Optional[str] = None) -> Optional[str]:
        """
        Create a new video entry in Notion database.

        Args:
            idea: Content idea from research agent
            script: Video script from scriptwriting agent
            mindmap_path: Path to mindmap SVG file

        Returns:
            Notion page ID if successful
        """
        if not self.notion_client or not self.database_id:
            self.logger.error("Notion client not initialized")
            return None

        try:
            self.logger.info(f"Creating Notion entry for: {idea.get('title', 'Untitled')}")

            # Prepare properties for Yander Content Board structure
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": idea.get('title', 'Untitled Video')
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "Ideation"
                    }
                },
                "Where": {
                    "multi_select": [
                        {"name": "YouTube"}
                    ]
                },
                "Media": {
                    "select": {
                        "name": "video"
                    }
                },
                "Date Briefed": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }

            # Build content blocks with toggle structure
            children = []

            # Build script content for toggle
            toggle_children = []

            # Add hook
            toggle_children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Hook"}}]
                }
            })
            toggle_children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": script.get('hook', {}).get('script', '')[:2000]}}]
                }
            })

            # Add early CTA (like/subscribe request in first 30 seconds)
            if script.get('early_cta'):
                toggle_children.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": "Early CTA"}}]
                    }
                })
                toggle_children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": script.get('early_cta', {}).get('script', '')[:2000]}}]
                    }
                })

            # Add intro
            toggle_children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Intro"}}]
                }
            })
            toggle_children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": script.get('intro', {}).get('script', '')[:2000]}}]
                }
            })

            # Add main sections
            for section in script.get('main_sections', [])[:5]:  # Limit sections to avoid too many blocks
                toggle_children.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": section.get('section_title', 'Section')[:100]}}]
                    }
                })

                # Add script content (truncated to avoid Notion limits)
                script_text = section.get('script', '')[:1900]
                toggle_children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": script_text}}]
                    }
                })

            # Add CTA
            toggle_children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Call to Action"}}]
                }
            })
            toggle_children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": script.get('call_to_action', {}).get('script', '')[:2000]}}]
                }
            })

            # Create H1 toggle heading named "Content" to match template
            children.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "Content"}}],
                    "is_toggleable": True,
                    "children": toggle_children[:90]  # Notion API limit is 100 blocks
                }
            })

            # Add mindmap reference outside toggle
            if mindmap_path:
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"🗺️ Mindmap: {mindmap_path}"}}]
                    }
                })

            # Create the page
            response = self.notion_client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )

            page_id = response['id']
            self.logger.info(f"Created Notion page: {page_id}")

            return page_id

        except Exception as e:
            self.logger.error(f"Error creating Notion entry: {str(e)}")
            return None

    def create_post_entry(self,
                         idea: Dict[str, Any],
                         post: Dict[str, Any]) -> Optional[str]:
        """
        Create a new post entry in Notion database.

        Args:
            idea: Content idea from research agent
            post: Post copy from scriptwriting agent

        Returns:
            Notion page ID if successful
        """
        if not self.notion_client or not self.database_id:
            self.logger.error("Notion client not initialized")
            return None

        try:
            self.logger.info(f"Creating Notion post entry for: {idea.get('title', 'Untitled')}")

            # Prepare properties for Yander Content Board
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": idea.get('title', 'Untitled Post')
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "Ideation"
                    }
                },
                "Where": {
                    "multi_select": [
                        {"name": "LinkedIn"}
                    ]
                },
                "Media": {
                    "select": {
                        "name": "image"
                    }
                },
                "Date Briefed": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }

            # Build content blocks with toggle structure
            children = []
            toggle_children = []

            # Add hook
            toggle_children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Hook"}}]
                }
            })
            toggle_children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": post.get('hook', '')[:2000]}}]
                }
            })

            # Add full post
            toggle_children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Full Post"}}]
                }
            })
            full_post = post.get('full_post', '')
            if len(full_post) > 2000:
                # Split if too long
                toggle_children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": full_post[:1900]}}]
                    }
                })
                toggle_children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": full_post[1900:3800]}}]
                    }
                })
            else:
                toggle_children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": full_post}}]
                    }
                })

            # Add key takeaways to toggle
            toggle_children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Key Takeaways"}}]
                }
            })

            for takeaway in post.get('key_takeaways', [])[:5]:
                toggle_children.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": takeaway[:2000]}}]
                    }
                })

            # Create H1 toggle heading named "Content" to match template
            children.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "Content"}}],
                    "is_toggleable": True,
                    "children": toggle_children[:90]
                }
            })

            # Add hashtags outside toggle
            hashtags = post.get('hashtags', [])
            if hashtags:
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "#️⃣ " + " ".join(hashtags[:10])}}]
                    }
                })

            # Create the page
            response = self.notion_client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )

            page_id = response['id']
            self.logger.info(f"Created Notion page: {page_id}")

            return page_id

        except Exception as e:
            self.logger.error(f"Error creating Notion post entry: {str(e)}")
            return None

    def update_status(self, page_id: str, status: str) -> bool:
        """
        Update the status of a Notion page.

        Args:
            page_id: Notion page ID
            status: New status (e.g., "Recording", "In Editing", "Published")

        Returns:
            True if successful
        """
        if not self.notion_client:
            return False

        try:
            self.notion_client.pages.update(
                page_id=page_id,
                properties={
                    "Status": {
                        "select": {
                            "name": status
                        }
                    }
                }
            )
            self.logger.info(f"Updated page {page_id} status to: {status}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating status: {str(e)}")
            return False

    def execute(self,
                content_type: str,
                idea: Dict[str, Any],
                content: Dict[str, Any],
                mindmap_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute Notion integration.

        Args:
            content_type: Type of content ("video" or "post")
            idea: Content idea dictionary
            content: Script or post content
            mindmap_path: Path to mindmap file (for videos)

        Returns:
            Dictionary with Notion page information
        """
        if content_type == "video":
            page_id = self.create_video_entry(idea, content, mindmap_path)
        elif content_type == "post":
            page_id = self.create_post_entry(idea, content)
        else:
            raise ValueError(f"Invalid content_type: {content_type}")

        if page_id:
            return {
                "success": True,
                "page_id": page_id,
                "page_url": f"https://notion.so/{page_id.replace('-', '')}"
            }
        else:
            return {
                "success": False,
                "error": "Failed to create Notion page"
            }


if __name__ == "__main__":
    # Example usage (requires valid Notion credentials)
    agent = NotionAgent()
    print("Notion Agent initialized")
