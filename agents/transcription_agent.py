"""
Video Transcription Agent
Transcribes video/audio to plain text using OpenAI's Whisper model locally.
"""

import os
import subprocess
import tempfile
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from .base_agent import BaseAgent


class TranscriptionAgent(BaseAgent):
    """Agent that transcribes video/audio to plain text using Whisper."""

    # Model size to approximate requirements
    MODEL_REQUIREMENTS = {
        "tiny": {"ram_gb": 1, "relative_speed": 32},
        "base": {"ram_gb": 1, "relative_speed": 16},
        "small": {"ram_gb": 2, "relative_speed": 6},
        "medium": {"ram_gb": 5, "relative_speed": 2},
        "large-v3": {"ram_gb": 10, "relative_speed": 1},
    }

    def __init__(
        self,
        model_size: str = "base",
        device: str = "auto",
        compute_type: str = "auto",
        language: Optional[str] = "en",
    ):
        """
        Initialize the transcription agent.

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large-v3)
            device: Device to run on (auto, cpu, cuda)
            compute_type: Compute type (auto, int8, float16, float32)
            language: Language code or None for auto-detection
        """
        super().__init__(name="Transcription Agent")

        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.language = language
        self.model = None  # Lazy-loaded

        self.system_prompt = """You are an expert at cleaning and formatting transcripts.

Your role is to:
1. Fix obvious transcription errors
2. Add proper punctuation and capitalization
3. Remove filler words (um, uh, like) when excessive
4. Format the text into readable paragraphs

Maintain the original meaning and speaker's voice."""

    def _check_dependencies(self) -> Dict[str, bool]:
        """Check if required dependencies are available."""
        checks = {
            "faster_whisper": False,
            "ffmpeg": False,
        }

        # Check faster-whisper
        try:
            import faster_whisper
            checks["faster_whisper"] = True
        except ImportError:
            self.logger.warning(
                "faster-whisper not installed. Run: pip install faster-whisper"
            )

        # Check FFmpeg
        if shutil.which("ffmpeg"):
            checks["ffmpeg"] = True
        else:
            self.logger.warning("FFmpeg not found in PATH.")

        return checks

    def _cuda_available(self) -> bool:
        """Check if CUDA is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def _load_model(self):
        """Lazy-load the Whisper model."""
        if self.model is not None:
            return

        self.logger.info(f"Loading Whisper model: {self.model_size}")

        try:
            from faster_whisper import WhisperModel

            # Determine compute type based on device
            compute_type = self.compute_type
            if compute_type == "auto":
                if self.device == "cuda" or (
                    self.device == "auto" and self._cuda_available()
                ):
                    compute_type = "float16"
                else:
                    compute_type = "int8"

            device = self.device
            if device == "auto":
                device = "cuda" if self._cuda_available() else "cpu"

            self.model = WhisperModel(
                self.model_size, device=device, compute_type=compute_type
            )

            self.logger.info(f"Model loaded on {device} with {compute_type} precision")

        except Exception as e:
            self.logger.error(f"Failed to load Whisper model: {str(e)}")
            raise RuntimeError(f"Failed to load Whisper model: {str(e)}")

    def _extract_audio(self, video_path: str) -> str:
        """
        Extract audio from video file.

        Args:
            video_path: Path to video file

        Returns:
            Path to extracted audio file (WAV format)
        """
        self.logger.info(f"Extracting audio from: {video_path}")

        # Create temp file for audio
        temp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_audio_path = temp_audio.name
        temp_audio.close()

        try:
            # Use FFmpeg to extract audio (16kHz mono WAV - optimal for Whisper)
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                video_path,
                "-vn",  # No video
                "-acodec",
                "pcm_s16le",  # 16-bit PCM
                "-ar",
                "16000",  # 16kHz sample rate
                "-ac",
                "1",  # Mono
                temp_audio_path,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg audio extraction failed: {result.stderr}")

            self.logger.info(f"Audio extracted to: {temp_audio_path}")
            return temp_audio_path

        except subprocess.TimeoutExpired:
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
            raise RuntimeError("Audio extraction timed out (>5 minutes)")
        except Exception as e:
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
            raise

    def _get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds."""
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            audio_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            self.logger.warning(f"ffprobe failed: {result.stderr}")
            return 0.0

        try:
            return float(result.stdout.strip())
        except ValueError:
            return 0.0

    def _cleanup_transcript(self, transcript: str) -> str:
        """Use Claude to clean up the transcript."""
        try:
            user_message = f"""Please clean up this transcript. Fix any obvious errors,
add proper punctuation, and format into readable paragraphs.
Keep the original meaning intact.

TRANSCRIPT:
{transcript}

Return only the cleaned transcript, no explanations."""

            cleaned = self.call_claude(
                system_prompt=self.system_prompt,
                user_message=user_message,
                max_tokens=len(transcript) * 2,  # Allow for expansion
                temperature=0.3,
            )

            return cleaned.strip()

        except Exception as e:
            self.logger.warning(f"Claude cleanup failed, using raw transcript: {str(e)}")
            return transcript

    def transcribe(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        beam_size: int = 5,
        vad_filter: bool = True,
        cleanup_with_claude: bool = False,
    ) -> Dict[str, Any]:
        """
        Transcribe video or audio file to plain text.

        Args:
            input_path: Path to video or audio file
            output_path: Path for output text file (auto-generated if not provided)
            beam_size: Beam size for decoding (higher = more accurate, slower)
            vad_filter: Use Voice Activity Detection to filter silence
            cleanup_with_claude: Use Claude to clean up the transcript

        Returns:
            Dictionary with transcription results
        """
        self.logger.info(f"Starting transcription: {input_path}")

        # Validate input
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Check dependencies
        deps = self._check_dependencies()
        if not deps["faster_whisper"]:
            raise RuntimeError(
                "faster-whisper not installed. Run: pip install faster-whisper"
            )

        # Determine if input is video or audio
        video_extensions = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv"}
        audio_extensions = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac"}

        input_ext = Path(input_path).suffix.lower()
        is_video = input_ext in video_extensions

        audio_path = None
        temp_audio_created = False

        try:
            # Extract audio if video
            if is_video:
                if not deps["ffmpeg"]:
                    raise RuntimeError(
                        "FFmpeg required for video transcription but not found"
                    )
                audio_path = self._extract_audio(input_path)
                temp_audio_created = True
            else:
                audio_path = input_path

            # Get audio duration
            duration = self._get_audio_duration(audio_path)
            if duration > 0:
                self.logger.info(f"Audio duration: {duration:.2f} seconds")

            # Load model (lazy)
            self._load_model()

            # Perform transcription
            self.logger.info("Transcribing audio...")

            segments, info = self.model.transcribe(
                audio_path,
                language=self.language,
                beam_size=beam_size,
                vad_filter=vad_filter,
            )

            # Collect segments
            transcript_parts = []
            segment_count = 0

            for segment in segments:
                transcript_parts.append(segment.text.strip())
                segment_count += 1

            raw_transcript = " ".join(transcript_parts)

            self.logger.info(f"Transcription complete: {len(raw_transcript)} characters")

            # Optional: Clean up with Claude
            final_transcript = raw_transcript
            if cleanup_with_claude and raw_transcript:
                self.logger.info("Cleaning transcript with Claude...")
                final_transcript = self._cleanup_transcript(raw_transcript)

            # Generate output path if not provided
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                input_name = Path(input_path).stem
                output_dir = "output/transcripts"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{input_name}_{timestamp}.txt")

            # Save transcript
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_transcript)

            self.logger.info(f"Transcript saved to: {output_path}")

            result = {
                "output_path": output_path,
                "transcript": final_transcript,
                "raw_transcript": raw_transcript if cleanup_with_claude else None,
                "duration_seconds": duration,
                "language": info.language if hasattr(info, "language") else self.language,
                "language_probability": (
                    info.language_probability
                    if hasattr(info, "language_probability")
                    else None
                ),
                "segment_count": segment_count,
                "character_count": len(final_transcript),
                "word_count": len(final_transcript.split()),
                "model_size": self.model_size,
                "settings": {
                    "beam_size": beam_size,
                    "vad_filter": vad_filter,
                    "cleanup_with_claude": cleanup_with_claude,
                },
            }

            # Save metadata
            metadata_path = output_path.replace(".txt", "_metadata.json")
            self.save_output(result, os.path.basename(metadata_path), os.path.dirname(metadata_path))

            return result

        finally:
            # Cleanup temp audio file
            if temp_audio_created and audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)

    def execute(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        beam_size: int = 5,
        vad_filter: bool = True,
        cleanup_with_claude: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Execute the transcription agent.

        Args:
            input_path: Path to video or audio file
            output_path: Output path for transcript
            beam_size: Beam size for decoding
            vad_filter: Use Voice Activity Detection
            cleanup_with_claude: Clean up with Claude

        Returns:
            Dictionary with transcription results
        """
        return self.transcribe(
            input_path=input_path,
            output_path=output_path,
            beam_size=beam_size,
            vad_filter=vad_filter,
            cleanup_with_claude=cleanup_with_claude,
        )


if __name__ == "__main__":
    import json

    agent = TranscriptionAgent(model_size="base")

    # Test with sample video
    test_video = "video_samples/test.mp4"

    if os.path.exists(test_video):
        result = agent.transcribe(input_path=test_video)
        print(json.dumps({k: v for k, v in result.items() if k != "transcript"}, indent=2))
        print(f"\nTranscript preview:\n{result['transcript'][:500]}...")
    else:
        print(f"Test video not found: {test_video}")
