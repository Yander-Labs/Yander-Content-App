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

    def _split_text_into_chunks(self, text: str, max_length: int = 1800) -> List[str]:
        """
        Split text into chunks at sentence boundaries.

        Args:
            text: Text to split
            max_length: Maximum length per chunk

        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]

        chunks = []
        current_chunk = ""

        # Split by sentences (period followed by space)
        sentences = text.replace('. ', '.|').split('|')

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_length:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

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
            for section in script.get('main_sections', [])[:8]:  # Limit sections to avoid too many blocks
                toggle_children.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": section.get('section_title', 'Section')[:100]}}]
                    }
                })

                # Split long script content into multiple paragraphs to avoid truncation
                script_text = section.get('script', '')
                # Split into chunks of ~1800 chars at sentence boundaries
                chunks = self._split_text_into_chunks(script_text, max_length=1800)
                for chunk in chunks[:3]:  # Limit to 3 paragraphs per section
                    toggle_children.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": chunk}}]
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

    def search_page_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Search for a page by title in the database.

        Args:
            title: Title to search for

        Returns:
            Page data if found, None otherwise
        """
        if not self.notion_client or not self.database_id:
            self.logger.error("Notion client not initialized")
            return None

        try:
            self.logger.info(f"Searching for page: {title}")

            response = self.notion_client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Name",
                    "title": {
                        "contains": title[:50]  # Use first 50 chars for matching
                    }
                }
            )

            results = response.get("results", [])
            if results:
                page = results[0]
                self.logger.info(f"Found page: {page['id']}")
                return {
                    "page_id": page["id"],
                    "title": page["properties"]["Name"]["title"][0]["text"]["content"] if page["properties"]["Name"]["title"] else "Untitled",
                    "url": page["url"]
                }

            self.logger.info("Page not found")
            return None

        except Exception as e:
            self.logger.error(f"Error searching for page: {str(e)}")
            return None

    def archive_page(self, page_id: str) -> bool:
        """
        Archive (soft delete) a Notion page.

        Args:
            page_id: Notion page ID to archive

        Returns:
            True if successful
        """
        if not self.notion_client:
            return False

        try:
            self.notion_client.pages.update(
                page_id=page_id,
                archived=True
            )
            self.logger.info(f"Archived page: {page_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error archiving page: {str(e)}")
            return False

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

    def create_talking_points_subpage(self,
                                      parent_page_id: str,
                                      script: Dict[str, Any],
                                      images: Optional[List[Dict[str, Any]]] = None) -> Optional[str]:
        """
        Create a talking points subpage under a video page.

        This creates a quick-reference document with main points and
        bullet points to help stay on track while recording.

        Args:
            parent_page_id: The parent video page ID
            script: Video script dictionary with main_sections
            images: Optional list of image dicts with 'section' and 'url' keys

        Returns:
            Subpage ID if successful
        """
        if not self.notion_client:
            self.logger.error("Notion client not initialized")
            return None

        try:
            self.logger.info(f"Creating talking points subpage for: {parent_page_id}")

            # Build image lookup by section name
            image_lookup = {}
            if images:
                for img in images:
                    section_name = img.get('section', '').lower()
                    image_lookup[section_name] = img.get('url')

            # Build content blocks
            children = []

            # Add intro reminder
            children.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": "Quick reference for recording. Each section has key points to hit."}}],
                    "icon": {"emoji": "🎬"}
                }
            })

            # Add hook section
            hook_text = script.get('hook', {}).get('script', '')
            if hook_text:
                # Add image if available
                if 'hook' in image_lookup:
                    children.append({
                        "object": "block",
                        "type": "image",
                        "image": {
                            "type": "external",
                            "external": {"url": image_lookup['hook']}
                        }
                    })

                children.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "Hook"}}]
                    }
                })
                # Extract key phrases from hook
                hook_points = self._extract_talking_points(hook_text)
                for point in hook_points:
                    children.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": point}}]
                        }
                    })

            # Add intro section
            intro_text = script.get('intro', {}).get('script', '')
            if intro_text:
                # Add image if available
                if 'intro' in image_lookup:
                    children.append({
                        "object": "block",
                        "type": "image",
                        "image": {
                            "type": "external",
                            "external": {"url": image_lookup['intro']}
                        }
                    })

                children.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "Intro"}}]
                    }
                })
                intro_points = self._extract_talking_points(intro_text)
                for point in intro_points:
                    children.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": point}}]
                        }
                    })

            # Add main sections
            for section in script.get('main_sections', [])[:10]:
                section_title = section.get('section_title', 'Section')
                section_text = section.get('script', '')

                # Add image if available for this section
                section_key = section_title.lower()
                if section_key in image_lookup:
                    children.append({
                        "object": "block",
                        "type": "image",
                        "image": {
                            "type": "external",
                            "external": {"url": image_lookup[section_key]}
                        }
                    })

                children.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": section_title}}]
                    }
                })

                # Extract talking points from section
                talking_points = self._extract_talking_points(section_text)
                for point in talking_points:
                    children.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": point}}]
                        }
                    })

            # Add CTA section
            cta_text = script.get('call_to_action', {}).get('script', '')
            if cta_text:
                # Add image if available
                if 'call to action' in image_lookup:
                    children.append({
                        "object": "block",
                        "type": "image",
                        "image": {
                            "type": "external",
                            "external": {"url": image_lookup['call to action']}
                        }
                    })

                children.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "Call to Action"}}]
                    }
                })
                cta_points = self._extract_talking_points(cta_text)
                for point in cta_points:
                    children.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": point}}]
                        }
                    })

            # Create the subpage
            response = self.notion_client.pages.create(
                parent={"page_id": parent_page_id},
                properties={
                    "title": {
                        "title": [
                            {
                                "text": {
                                    "content": "Talking Points"
                                }
                            }
                        ]
                    }
                },
                children=children[:100]  # Notion limit
            )

            subpage_id = response['id']
            self.logger.info(f"Created talking points subpage: {subpage_id}")

            return subpage_id

        except Exception as e:
            self.logger.error(f"Error creating talking points subpage: {str(e)}")
            return None

    def _extract_talking_points(self, text: str, max_points: int = 5) -> List[str]:
        """
        Extract key talking points from script text.

        Splits text into sentences and selects the most important ones
        as bullet points for quick reference.

        Args:
            text: Script text to extract points from
            max_points: Maximum number of points to extract

        Returns:
            List of talking point strings
        """
        if not text:
            return []

        # Split into sentences
        sentences = []
        for part in text.replace('? ', '?|').replace('! ', '!|').replace('. ', '.|').split('|'):
            part = part.strip()
            if part and len(part) > 10:  # Skip very short fragments
                sentences.append(part)

        if not sentences:
            return [text[:200]] if text else []

        # Select key sentences - prioritize first, last, and those with key phrases
        points = []

        # Always include first sentence (sets up the point)
        if sentences:
            points.append(sentences[0])

        # Look for sentences with strong statements or key concepts
        key_indicators = ['this is', 'here\'s', 'the key', 'important', 'remember',
                         'you need', 'the problem', 'the solution', 'i learned',
                         'the difference', 'this means', 'in other words']

        for sentence in sentences[1:-1]:  # Skip first and last
            lower = sentence.lower()
            if any(indicator in lower for indicator in key_indicators):
                if sentence not in points:
                    points.append(sentence)
                    if len(points) >= max_points - 1:
                        break

        # Fill remaining slots with evenly spaced sentences
        if len(points) < max_points - 1 and len(sentences) > 2:
            remaining = sentences[1:-1]
            step = max(1, len(remaining) // (max_points - len(points) - 1))
            for i in range(0, len(remaining), step):
                if remaining[i] not in points:
                    points.append(remaining[i])
                    if len(points) >= max_points - 1:
                        break

        # Include last sentence if different (often a key takeaway)
        if len(sentences) > 1 and sentences[-1] not in points:
            points.append(sentences[-1])

        # Truncate long points
        return [p[:300] + '...' if len(p) > 300 else p for p in points[:max_points]]

    def get_recent_pages(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get recently created pages from the database.

        Args:
            days: Number of days to look back

        Returns:
            List of page info dicts with title, created_date, page_id
        """
        if not self.notion_client or not self.database_id:
            self.logger.error("Notion client not initialized")
            return []

        try:
            from datetime import datetime, timedelta

            # Calculate date threshold
            threshold = datetime.now() - timedelta(days=days)

            self.logger.info(f"Fetching pages from last {days} days")

            # Use search to find pages in the database
            response = self.notion_client.search(
                filter={
                    "property": "object",
                    "value": "page"
                },
                sort={
                    "direction": "descending",
                    "timestamp": "last_edited_time"
                },
                page_size=100
            )

            pages = []
            for page in response.get("results", []):
                # Filter to only pages from our database
                parent = page.get("parent", {})
                if parent.get("type") != "database_id":
                    continue
                if parent.get("database_id", "").replace("-", "") != self.database_id.replace("-", ""):
                    continue

                # Check date
                created_time = page.get("created_time", "")
                if created_time:
                    try:
                        page_date = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
                        if page_date.replace(tzinfo=None) < threshold:
                            continue
                    except:
                        pass

                title = "Untitled"
                if page.get("properties", {}).get("Name", {}).get("title"):
                    title_list = page["properties"]["Name"]["title"]
                    if title_list:
                        title = title_list[0].get("text", {}).get("content", "Untitled")

                pages.append({
                    "page_id": page["id"],
                    "title": title,
                    "created_date": created_time,
                    "url": page.get("url", "")
                })

            self.logger.info(f"Found {len(pages)} pages from last {days} days")
            return pages

        except Exception as e:
            self.logger.error(f"Error fetching recent pages: {str(e)}")
            return []

    def get_page_titles(self, days: int = 30) -> List[str]:
        """
        Get just the titles of recent pages (for duplicate checking).

        Args:
            days: Number of days to look back

        Returns:
            List of page titles
        """
        pages = self.get_recent_pages(days)
        return [p["title"] for p in pages]

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
