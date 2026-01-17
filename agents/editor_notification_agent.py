"""
Video Editor Notification Agent
Notifies video editor when files are ready for editing via Notion.
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from notion_client import Client
from .base_agent import BaseAgent


class EditorNotificationAgent(BaseAgent):
    """Agent that notifies video editor when content is ready for editing."""

    def __init__(self):
        super().__init__(name="Editor Notification Agent")

        # Initialize Notion client
        notion_api_key = os.getenv("NOTION_API_KEY")
        if not notion_api_key:
            self.logger.warning("NOTION_API_KEY not found. Notion integration will not work.")
            self.notion_client = None
        else:
            self.notion_client = Client(auth=notion_api_key)

        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.editor_user_id = os.getenv("VIDEO_EDITOR_NOTION_USER_ID")

    def assign_to_editor(self,
                        page_id: str,
                        video_files: List[str],
                        notes: Optional[str] = None) -> bool:
        """
        Assign a video to the editor in Notion.

        Args:
            page_id: Notion page ID for the video
            video_files: List of video file paths/URLs
            notes: Additional notes for the editor

        Returns:
            True if successful
        """
        if not self.notion_client:
            self.logger.error("Notion client not initialized")
            return False

        try:
            self.logger.info(f"Assigning page {page_id} to editor")

            # Update the page status and assignment
            update_properties = {
                "Status": {
                    "select": {
                        "name": "Ready for Editing"
                    }
                },
                "Recording Date": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }

            # Assign to editor if user ID is configured
            if self.editor_user_id:
                update_properties["Assigned To"] = {
                    "people": [
                        {
                            "id": self.editor_user_id
                        }
                    ]
                }

            self.notion_client.pages.update(
                page_id=page_id,
                properties=update_properties
            )

            # Add a comment with video file information
            comment_blocks = []

            # Add video files section
            comment_blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Raw Video Files"}}]
                }
            })

            for i, file_path in enumerate(video_files, 1):
                comment_blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": f"File {i}: {file_path}"}}]
                    }
                })

            # Add editor notes if provided
            if notes:
                comment_blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": "Editor Notes"}}]
                    }
                })
                comment_blocks.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{"type": "text", "text": {"content": notes}}],
                        "icon": {"emoji": "📝"}
                    }
                })

            # Add editing checklist
            comment_blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Editing Checklist"}}]
                }
            })

            checklist_items = [
                "Color correction and grading",
                "Audio mixing and enhancement",
                "Insert mindmap visuals at key points",
                "Add intro/outro animations",
                "Add lower thirds and text overlays",
                "Insert B-roll footage",
                "Export in 1080p and 4K",
                "Add thumbnail options"
            ]

            for item in checklist_items:
                comment_blocks.append({
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [{"type": "text", "text": {"content": item}}],
                        "checked": False
                    }
                })

            # Append blocks to the page
            self.notion_client.blocks.children.append(
                block_id=page_id,
                children=comment_blocks
            )

            self.logger.info(f"Successfully assigned to editor with {len(video_files)} files")
            return True

        except Exception as e:
            self.logger.error(f"Error assigning to editor: {str(e)}")
            return False

    def create_editing_task(self,
                           video_title: str,
                           video_files: List[str],
                           script_page_id: str,
                           deadline: Optional[str] = None,
                           priority: str = "Medium") -> Optional[str]:
        """
        Create a new editing task in Notion.

        Args:
            video_title: Title of the video
            video_files: List of video file paths
            script_page_id: ID of the Notion page with the script
            deadline: Deadline for editing (ISO format)
            priority: Priority level (Low, Medium, High)

        Returns:
            Task page ID if successful
        """
        if not self.notion_client or not self.database_id:
            self.logger.error("Notion client not initialized")
            return None

        try:
            self.logger.info(f"Creating editing task for: {video_title}")

            # Create task properties
            properties = {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": f"Edit: {video_title}"
                            }
                        }
                    ]
                },
                "Type": {
                    "select": {
                        "name": "Editing Task"
                    }
                },
                "Status": {
                    "select": {
                        "name": "To Do"
                    }
                },
                "Priority": {
                    "select": {
                        "name": priority
                    }
                },
                "Created Date": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }

            if deadline:
                properties["Due Date"] = {
                    "date": {
                        "start": deadline
                    }
                }

            if self.editor_user_id:
                properties["Assigned To"] = {
                    "people": [
                        {
                            "id": self.editor_user_id
                        }
                    ]
                }

            # Build task content
            children = []

            # Link to script
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Script: "
                            }
                        },
                        {
                            "type": "mention",
                            "mention": {
                                "type": "page",
                                "page": {
                                    "id": script_page_id
                                }
                            }
                        }
                    ]
                }
            })

            # Add video files
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Raw Files"}}]
                }
            })

            for file_path in video_files:
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": file_path}}]
                    }
                })

            # Create the task page
            response = self.notion_client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )

            task_id = response['id']
            self.logger.info(f"Created editing task: {task_id}")

            return task_id

        except Exception as e:
            self.logger.error(f"Error creating editing task: {str(e)}")
            return None

    def execute(self,
                page_id: str,
                video_files: List[str],
                notes: Optional[str] = None,
                deadline: Optional[str] = None,
                priority: str = "Medium") -> Dict[str, Any]:
        """
        Execute editor notification.

        Args:
            page_id: Notion page ID for the video content
            video_files: List of video file paths
            notes: Additional notes for the editor
            deadline: Deadline for editing
            priority: Priority level

        Returns:
            Dictionary with notification status
        """
        # Assign to editor
        assigned = self.assign_to_editor(page_id, video_files, notes)

        result = {
            "page_id": page_id,
            "assigned_to_editor": assigned,
            "video_files_count": len(video_files),
            "notification_time": datetime.now().isoformat()
        }

        if assigned:
            self.logger.info(f"Successfully notified editor about {len(video_files)} files")
        else:
            self.logger.warning("Failed to assign to editor")

        return result


if __name__ == "__main__":
    # Example usage
    agent = EditorNotificationAgent()
    print("Editor Notification Agent initialized")
