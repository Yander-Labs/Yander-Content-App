"""
Content Creation Orchestrator
Coordinates all agents to execute the full content creation workflow.
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from colorama import Fore, Style, init

# Add agents to path
sys.path.insert(0, os.path.dirname(__file__))

from agents.research_agent import ResearchAgent
from agents.scriptwriting_agent import ScriptwritingAgent
from agents.mindmap_agent import MindmapAgent
from agents.notion_agent import NotionAgent
from agents.editor_notification_agent import EditorNotificationAgent
from agents.transcription_agent import TranscriptionAgent
from agents.video_editing_agent import VideoEditingAgent
from agents.youtube_transcript_agent import YouTubeTranscriptAgent
from agents.image_agent import ImageAgent

# Initialize colorama
init(autoreset=True)


class ContentCreationOrchestrator:
    """Main orchestrator that coordinates all content creation agents."""

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.scriptwriting_agent = ScriptwritingAgent()
        self.mindmap_agent = MindmapAgent()
        self.notion_agent = NotionAgent()
        self.editor_agent = EditorNotificationAgent()
        self.transcription_agent = None  # Lazy-loaded due to model size
        self.video_editing_agent = None  # Lazy-loaded
        self.youtube_transcript_agent = None  # Lazy-loaded
        self.image_agent = None  # Lazy-loaded

        print(f"{Fore.GREEN}✓ Content Creation Orchestrator initialized{Style.RESET_ALL}")
        print(f"{Fore.CYAN}All agents loaded and ready{Style.RESET_ALL}\n")

    def create_video_content(self,
                            tool_info: Optional[str] = None,
                            user_data: Optional[str] = None,
                            topics: Optional[List[str]] = None,
                            video_index: int = 0,
                            tone: str = "professional",
                            generate_images: bool = True) -> Dict[str, Any]:
        """
        Create complete video content (idea, script, images, Notion entry with talking points).

        Args:
            tool_info: Information about the marketing tool
            user_data: Additional user-provided data
            topics: Topics to focus on
            video_index: Index of video idea to use
            tone: Tone for the script
            generate_images: Whether to generate sketch images for each section

        Returns:
            Dictionary with all created content
        """
        total_steps = 6 if generate_images else 5
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}CREATING VIDEO CONTENT")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")

        result = {}

        # Step 1: Research content ideas
        print(f"{Fore.CYAN}[1/{total_steps}] Researching content ideas...{Style.RESET_ALL}")
        research_results = self.research_agent.execute(
            tool_info=tool_info,
            user_data=user_data,
            topics=topics,
            num_video_ideas=3,
            num_post_ideas=0
        )

        if 'error' in research_results:
            print(f"{Fore.RED}✗ Research failed: {research_results['error']}{Style.RESET_ALL}")
            return {"error": "Research failed", "details": research_results}

        video_ideas = research_results.get('video_ideas', [])
        if not video_ideas:
            print(f"{Fore.RED}✗ No video ideas generated{Style.RESET_ALL}")
            return {"error": "No video ideas generated"}

        selected_idea = video_ideas[min(video_index, len(video_ideas) - 1)]
        print(f"{Fore.GREEN}✓ Selected idea: {selected_idea['title']}{Style.RESET_ALL}\n")
        result['idea'] = selected_idea

        # Step 2: Write script
        print(f"{Fore.CYAN}[2/{total_steps}] Writing video script...{Style.RESET_ALL}")
        script_result = self.scriptwriting_agent.execute(
            content_type="video",
            idea=selected_idea,
            tone=tone
        )

        if 'error' in script_result:
            print(f"{Fore.RED}✗ Scriptwriting failed: {script_result['error']}{Style.RESET_ALL}")
            return {"error": "Scriptwriting failed", "details": script_result}

        print(f"{Fore.GREEN}✓ Script complete ({script_result.get('estimated_length_minutes', 0)} minutes){Style.RESET_ALL}\n")
        result['script'] = script_result

        # Step 3: Generate images for each section (if enabled)
        images = []
        if generate_images:
            print(f"{Fore.CYAN}[3/{total_steps}] Generating section images...{Style.RESET_ALL}")

            # Lazy-load image agent
            if self.image_agent is None:
                self.image_agent = ImageAgent()

            if self.image_agent.client:
                num_sections = len(script_result.get('main_sections', []))
                print(f"{Fore.CYAN}    Generating {num_sections} images (this may take a few minutes)...{Style.RESET_ALL}")

                image_result = self.image_agent.generate_section_images(
                    script_result,
                    include_hook=False,
                    include_intro=False,
                    rate_limit_delay=12.0
                )

                if image_result:
                    images = image_result
                    print(f"{Fore.GREEN}✓ Generated {len(images)} section images{Style.RESET_ALL}\n")
                    result['images'] = images
                else:
                    print(f"{Fore.YELLOW}⚠ No images generated{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.YELLOW}⚠ Image generation skipped (no REPLICATE_API_TOKEN){Style.RESET_ALL}\n")

        # Step 4: Generate mindmap (adjusted step number)
        step_num = 4 if generate_images else 3
        print(f"{Fore.CYAN}[{step_num}/{total_steps}] Generating mindmap...{Style.RESET_ALL}")
        mindmap_result = self.mindmap_agent.execute(
            content=script_result,
            content_type="video"
        )

        if 'error' in mindmap_result:
            print(f"{Fore.RED}✗ Mindmap generation failed: {mindmap_result['error']}{Style.RESET_ALL}")
            result['mindmap'] = None
        else:
            print(f"{Fore.GREEN}✓ Mindmap saved: {mindmap_result['svg_file']}{Style.RESET_ALL}\n")
            result['mindmap'] = mindmap_result

        # Step 5: Create Notion entry
        step_num = 5 if generate_images else 4
        print(f"{Fore.CYAN}[{step_num}/{total_steps}] Creating Notion database entry...{Style.RESET_ALL}")
        notion_result = self.notion_agent.execute(
            content_type="video",
            idea=selected_idea,
            content=script_result,
            mindmap_path=mindmap_result.get('svg_file') if mindmap_result else None
        )

        if not notion_result.get('success'):
            print(f"{Fore.RED}✗ Notion entry creation failed{Style.RESET_ALL}")
            result['notion'] = None
        else:
            print(f"{Fore.GREEN}✓ Notion page created: {notion_result['page_url']}{Style.RESET_ALL}\n")
            result['notion'] = notion_result

            # Create talking points subpage with images
            if notion_result.get('page_id') and (images or script_result):
                print(f"{Fore.CYAN}    Creating talking points page with images...{Style.RESET_ALL}")
                subpage_id = self.notion_agent.create_talking_points_subpage(
                    parent_page_id=notion_result['page_id'],
                    script=script_result,
                    images=images
                )
                if subpage_id:
                    print(f"{Fore.GREEN}    ✓ Talking points page created{Style.RESET_ALL}\n")
                    result['talking_points_page_id'] = subpage_id

        # Final step: Summary
        step_num = 6 if generate_images else 5
        print(f"{Fore.CYAN}[{step_num}/{total_steps}] Video content package complete!{Style.RESET_ALL}\n")

        result['status'] = 'complete'
        result['created_at'] = datetime.now().isoformat()

        return result

    def create_post_content(self,
                           tool_info: Optional[str] = None,
                           user_data: Optional[str] = None,
                           topics: Optional[List[str]] = None,
                           post_index: int = 0,
                           tone: str = "professional") -> Dict[str, Any]:
        """
        Create complete post content (idea, copy, Notion entry).

        Args:
            tool_info: Information about the marketing tool
            user_data: Additional user-provided data
            topics: Topics to focus on
            post_index: Index of post idea to use
            tone: Tone for the copy

        Returns:
            Dictionary with all created content
        """
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}CREATING POST CONTENT")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")

        result = {}

        # Step 1: Research content ideas
        print(f"{Fore.CYAN}[1/3] Researching content ideas...{Style.RESET_ALL}")
        research_results = self.research_agent.execute(
            tool_info=tool_info,
            user_data=user_data,
            topics=topics,
            num_video_ideas=0,
            num_post_ideas=5
        )

        if 'error' in research_results:
            print(f"{Fore.RED}✗ Research failed: {research_results['error']}{Style.RESET_ALL}")
            return {"error": "Research failed", "details": research_results}

        post_ideas = research_results.get('post_ideas', [])
        if not post_ideas:
            print(f"{Fore.RED}✗ No post ideas generated{Style.RESET_ALL}")
            return {"error": "No post ideas generated"}

        selected_idea = post_ideas[min(post_index, len(post_ideas) - 1)]
        print(f"{Fore.GREEN}✓ Selected idea: {selected_idea['title']}{Style.RESET_ALL}\n")
        result['idea'] = selected_idea

        # Step 2: Write post copy
        print(f"{Fore.CYAN}[2/3] Writing post copy...{Style.RESET_ALL}")
        post_result = self.scriptwriting_agent.execute(
            content_type="post",
            idea=selected_idea,
            tone=tone
        )

        if 'error' in post_result:
            print(f"{Fore.RED}✗ Post writing failed: {post_result['error']}{Style.RESET_ALL}")
            return {"error": "Post writing failed", "details": post_result}

        print(f"{Fore.GREEN}✓ Post complete ({post_result.get('word_count', 0)} words){Style.RESET_ALL}\n")
        result['post'] = post_result

        # Step 3: Create Notion entry
        print(f"{Fore.CYAN}[3/3] Creating Notion database entry...{Style.RESET_ALL}")
        notion_result = self.notion_agent.execute(
            content_type="post",
            idea=selected_idea,
            content=post_result
        )

        if not notion_result.get('success'):
            print(f"{Fore.RED}✗ Notion entry creation failed{Style.RESET_ALL}")
            result['notion'] = None
        else:
            print(f"{Fore.GREEN}✓ Notion page created: {notion_result['page_url']}{Style.RESET_ALL}\n")
            result['notion'] = notion_result

        result['status'] = 'complete'
        result['created_at'] = datetime.now().isoformat()

        return result

    def notify_editor(self,
                     notion_page_id: str,
                     video_files: List[str],
                     notes: Optional[str] = None) -> Dict[str, Any]:
        """
        Notify video editor that files are ready.

        Args:
            notion_page_id: Notion page ID for the video
            video_files: List of video file paths
            notes: Additional notes for editor

        Returns:
            Dictionary with notification status
        """
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}NOTIFYING VIDEO EDITOR")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")

        print(f"{Fore.CYAN}Assigning {len(video_files)} file(s) to editor...{Style.RESET_ALL}")

        result = self.editor_agent.execute(
            page_id=notion_page_id,
            video_files=video_files,
            notes=notes
        )

        if result.get('assigned_to_editor'):
            print(f"{Fore.GREEN}✓ Editor notified successfully{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}✗ Failed to notify editor{Style.RESET_ALL}\n")

        return result

    def batch_create_videos(self,
                           count: int = 3,
                           **kwargs) -> List[Dict[str, Any]]:
        """
        Create multiple video content packages.

        Args:
            count: Number of videos to create
            **kwargs: Arguments to pass to create_video_content

        Returns:
            List of results
        """
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}BATCH CREATING {count} VIDEOS")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")

        results = []
        for i in range(count):
            print(f"{Fore.MAGENTA}Video {i+1}/{count}{Style.RESET_ALL}")
            result = self.create_video_content(video_index=i, **kwargs)
            results.append(result)

        print(f"\n{Fore.GREEN}✓ Batch creation complete: {count} videos{Style.RESET_ALL}\n")
        return results

    def batch_create_posts(self,
                          count: int = 5,
                          **kwargs) -> List[Dict[str, Any]]:
        """
        Create multiple post content packages.

        Args:
            count: Number of posts to create
            **kwargs: Arguments to pass to create_post_content

        Returns:
            List of results
        """
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}BATCH CREATING {count} POSTS")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")

        results = []
        for i in range(count):
            print(f"{Fore.MAGENTA}Post {i+1}/{count}{Style.RESET_ALL}")
            result = self.create_post_content(post_index=i, **kwargs)
            results.append(result)

        print(f"\n{Fore.GREEN}✓ Batch creation complete: {count} posts{Style.RESET_ALL}\n")
        return results

    def transcribe_video(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        model_size: str = "base",
        cleanup_with_claude: bool = False,
    ) -> Dict[str, Any]:
        """
        Transcribe a video to text.

        Args:
            video_path: Path to video file
            output_path: Output path for transcript
            model_size: Whisper model size (tiny, base, small, medium, large-v3)
            cleanup_with_claude: Use Claude to clean up transcript

        Returns:
            Dictionary with transcription results
        """
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}TRANSCRIBING VIDEO")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")

        # Lazy-load transcription agent
        if self.transcription_agent is None or self.transcription_agent.model_size != model_size:
            self.transcription_agent = TranscriptionAgent(model_size=model_size)

        result = self.transcription_agent.execute(
            input_path=video_path,
            output_path=output_path,
            cleanup_with_claude=cleanup_with_claude,
        )

        print(f"{Fore.GREEN}✓ Transcription complete: {result['word_count']} words{Style.RESET_ALL}\n")

        return result

    def edit_and_transcribe_video(
        self,
        screen_recording: str,
        output_dir: str = "output",
        model_size: str = "base",
    ) -> Dict[str, Any]:
        """
        Full workflow: edit video (remove silences) then transcribe.

        Args:
            screen_recording: Path to raw video
            output_dir: Output directory
            model_size: Whisper model size for transcription

        Returns:
            Dictionary with editing and transcription results
        """
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}EDIT AND TRANSCRIBE WORKFLOW")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")

        result = {}

        # Lazy-load video editing agent
        if self.video_editing_agent is None:
            self.video_editing_agent = VideoEditingAgent()

        # Step 1: Edit video
        print(f"{Fore.CYAN}[1/2] Editing video...{Style.RESET_ALL}")
        edit_result = self.video_editing_agent.execute(screen_recording=screen_recording)
        result["edit"] = edit_result

        # Step 2: Transcribe edited video
        print(f"{Fore.CYAN}[2/2] Transcribing edited video...{Style.RESET_ALL}")
        transcript_result = self.transcribe_video(
            video_path=edit_result["output_path"], model_size=model_size
        )
        result["transcript"] = transcript_result

        result["status"] = "complete"
        result["created_at"] = datetime.now().isoformat()

        return result

    def analyze_youtube_video(
        self,
        url: str,
        prompt: str = "Summarize the key points and main takeaways from this video.",
        save_transcript: bool = True,
    ) -> Dict[str, Any]:
        """
        Fetch and analyze a YouTube video transcript.

        Args:
            url: YouTube video URL
            prompt: Analysis prompt/question
            save_transcript: Whether to save transcript to file

        Returns:
            Dictionary with transcript and analysis
        """
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}ANALYZING YOUTUBE VIDEO")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")

        # Lazy-load YouTube transcript agent
        if self.youtube_transcript_agent is None:
            self.youtube_transcript_agent = YouTubeTranscriptAgent()

        print(f"{Fore.CYAN}[1/2] Fetching transcript...{Style.RESET_ALL}")
        result = self.youtube_transcript_agent.execute(
            youtube_url=url,
            prompt=prompt,
            save_transcript=save_transcript,
        )

        if result.get("status") == "error":
            print(f"{Fore.RED}✗ Failed to fetch transcript: {result.get('error')}{Style.RESET_ALL}")
            return result

        print(f"{Fore.GREEN}✓ Transcript fetched ({result['word_count']} words){Style.RESET_ALL}")

        if result.get("analysis"):
            print(f"{Fore.CYAN}[2/2] Analysis complete{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Insights generated{Style.RESET_ALL}\n")

        result["created_at"] = datetime.now().isoformat()

        return result


def main():
    """Example usage of the orchestrator."""
    orchestrator = ContentCreationOrchestrator()

    # Example: Create a video
    result = orchestrator.create_video_content(
        tool_info="Marketing automation platform for agencies",
        topics=["client retention", "agency automation"],
        tone="professional"
    )

    print(f"\n{Fore.CYAN}Result:{Style.RESET_ALL}")
    print(json.dumps({k: v for k, v in result.items() if k not in ['script', 'mindmap']}, indent=2))


if __name__ == "__main__":
    main()
