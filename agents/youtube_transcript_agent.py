"""
YouTube Transcript Agent
Fetches transcripts from YouTube videos and provides AI-powered insights.
"""

import os
import re
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

from .base_agent import BaseAgent

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
    )
except ImportError:
    YouTubeTranscriptApi = None


class YouTubeTranscriptAgent(BaseAgent):
    """Agent for fetching YouTube transcripts and generating insights."""

    def __init__(self, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize the YouTube Transcript Agent.

        Args:
            model: Claude model to use for analysis
        """
        super().__init__(name="YouTube Transcript Agent", model=model)

        if YouTubeTranscriptApi is None:
            self.logger.warning(
                "youtube-transcript-api not installed. "
                "Run: pip install youtube-transcript-api"
            )

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats.

        Args:
            url: YouTube video URL

        Returns:
            Video ID or None if not found
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
            r'^([a-zA-Z0-9_-]{11})$',  # Direct video ID
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def fetch_transcript(
        self,
        video_id: str,
        languages: List[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch transcript for a YouTube video.

        Args:
            video_id: YouTube video ID
            languages: Preferred languages (defaults to English)

        Returns:
            Dictionary with transcript data
        """
        if YouTubeTranscriptApi is None:
            return {
                "error": "youtube-transcript-api not installed",
                "status": "error"
            }

        if languages is None:
            languages = ['en', 'en-US', 'en-GB']

        try:
            self.logger.info(f"Fetching transcript for video: {video_id}")

            # Create API instance (new API requires instantiation)
            ytt_api = YouTubeTranscriptApi()

            # Try to get transcript in preferred languages
            transcript_list = ytt_api.list(video_id)

            transcript = None
            is_auto_generated = False

            # First try manually created transcripts
            try:
                transcript = transcript_list.find_manually_created_transcript(languages)
                is_auto_generated = False
                self.logger.info("Found manually created transcript")
            except NoTranscriptFound:
                # Fall back to auto-generated
                try:
                    transcript = transcript_list.find_generated_transcript(languages)
                    is_auto_generated = True
                    self.logger.info("Using auto-generated transcript")
                except NoTranscriptFound:
                    # Try any available transcript and translate
                    try:
                        available = list(transcript_list)
                        if available:
                            transcript = available[0].translate('en')
                            is_auto_generated = True
                            self.logger.info(f"Translated from {available[0].language}")
                    except Exception as e:
                        self.logger.error(f"Translation failed: {e}")

            if transcript is None:
                return {
                    "error": "No transcript available for this video",
                    "status": "error"
                }

            # Fetch the actual transcript data
            transcript_data = transcript.fetch()

            # Combine into full text - handle both dict and object access
            full_text = " ".join([
                entry.get('text', '') if isinstance(entry, dict) else entry.text
                for entry in transcript_data
            ])

            # Calculate duration
            if transcript_data:
                last_entry = transcript_data[-1]
                if isinstance(last_entry, dict):
                    duration_seconds = last_entry.get('start', 0) + last_entry.get('duration', 0)
                else:
                    duration_seconds = last_entry.start + getattr(last_entry, 'duration', 0)
            else:
                duration_seconds = 0

            return {
                "video_id": video_id,
                "transcript": full_text,
                "segments": [
                    {"text": e.get('text', '') if isinstance(e, dict) else e.text,
                     "start": e.get('start', 0) if isinstance(e, dict) else e.start,
                     "duration": e.get('duration', 0) if isinstance(e, dict) else getattr(e, 'duration', 0)}
                    for e in transcript_data
                ],
                "duration_seconds": duration_seconds,
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_auto_generated": is_auto_generated,
                "word_count": len(full_text.split()),
                "status": "success"
            }

        except TranscriptsDisabled:
            self.logger.error("Transcripts are disabled for this video")
            return {
                "error": "Transcripts are disabled for this video",
                "status": "error"
            }
        except VideoUnavailable:
            self.logger.error("Video is unavailable")
            return {
                "error": "Video is unavailable",
                "status": "error"
            }
        except Exception as e:
            self.logger.error(f"Error fetching transcript: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }

    def analyze_transcript(
        self,
        transcript: str,
        prompt: str,
        max_tokens: int = 4096
    ) -> str:
        """
        Analyze transcript with Claude.

        Args:
            transcript: The video transcript
            prompt: Analysis prompt/question
            max_tokens: Maximum tokens in response

        Returns:
            Claude's analysis
        """
        system_prompt = """You are an expert content analyst. You analyze video transcripts and provide detailed, actionable insights.

When analyzing transcripts:
- Extract key points and main arguments
- Identify actionable takeaways
- Note any frameworks, strategies, or methodologies mentioned
- Highlight quotable statements or important statistics
- Structure your response clearly with headers and bullet points when appropriate

Be thorough but concise. Focus on value and actionability."""

        user_message = f"""Here is a video transcript to analyze:

<transcript>
{transcript}
</transcript>

{prompt}"""

        self.logger.info(f"Analyzing transcript with prompt: {prompt[:100]}...")

        return self.call_claude(
            system_prompt=system_prompt,
            user_message=user_message,
            max_tokens=max_tokens,
            temperature=0.7
        )

    def execute(
        self,
        youtube_url: str,
        prompt: Optional[str] = None,
        save_transcript: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Fetch YouTube transcript and optionally analyze it.

        Args:
            youtube_url: YouTube video URL
            prompt: Optional analysis prompt (if None, just returns transcript)
            save_transcript: Whether to save transcript to file

        Returns:
            Dictionary with transcript and optional analysis
        """
        self.logger.info(f"Processing YouTube video: {youtube_url}")

        # Extract video ID
        video_id = self.extract_video_id(youtube_url)
        if not video_id:
            return {
                "error": "Could not extract video ID from URL",
                "url": youtube_url,
                "status": "error"
            }

        # Fetch transcript
        transcript_result = self.fetch_transcript(video_id)

        if transcript_result.get("status") == "error":
            return transcript_result

        result = {
            "url": youtube_url,
            "video_id": video_id,
            "transcript": transcript_result["transcript"],
            "duration_seconds": transcript_result["duration_seconds"],
            "language": transcript_result["language"],
            "is_auto_generated": transcript_result["is_auto_generated"],
            "word_count": transcript_result["word_count"],
            "status": "success"
        }

        # Save transcript if requested
        if save_transcript:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"youtube_{video_id}_{timestamp}.txt"
            output_dir = "output/transcripts"
            os.makedirs(output_dir, exist_ok=True)

            filepath = self.save_output(
                transcript_result["transcript"],
                filename,
                output_dir
            )
            result["transcript_file"] = filepath

            # Also save metadata
            metadata = {
                "url": youtube_url,
                "video_id": video_id,
                "duration_seconds": transcript_result["duration_seconds"],
                "language": transcript_result["language"],
                "language_code": transcript_result["language_code"],
                "is_auto_generated": transcript_result["is_auto_generated"],
                "word_count": transcript_result["word_count"],
                "fetched_at": datetime.now().isoformat()
            }
            metadata_file = f"youtube_{video_id}_{timestamp}_metadata.json"
            self.save_output(metadata, metadata_file, output_dir)
            result["metadata_file"] = os.path.join(output_dir, metadata_file)

        # Analyze if prompt provided
        if prompt:
            self.logger.info("Analyzing transcript...")
            analysis = self.analyze_transcript(
                transcript_result["transcript"],
                prompt
            )
            result["analysis"] = analysis
            result["prompt"] = prompt

        return result
