"""
Video Editing Agent
Automatically edits raw video footage by removing silences and adding enhancements.
"""

import os
import subprocess
import tempfile
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
from .base_agent import BaseAgent


class VideoEditingAgent(BaseAgent):
    """Agent that automatically edits video by removing silences and adding enhancements."""

    def __init__(self):
        super().__init__(name="Video Editing Agent")
        self.system_prompt = """You are an expert video editor assistant.

Your role is to:
1. Analyze video transcripts to identify key moments
2. Suggest where to add emphasis (face cam cutaways)
3. Identify important statements for text overlays
4. Help create engaging, well-paced video content

When analyzing transcripts, look for:
- Key conclusions or insights
- Important statistics or numbers
- Emotional emphasis moments
- Section transitions
- Memorable quotes or statements
"""

    def detect_silences(
        self,
        video_path: str,
        silence_thresh: int = -40,
        min_silence_ms: int = 800
    ) -> List[Tuple[int, int]]:
        """
        Detect silent segments in video audio.

        Args:
            video_path: Path to the video file
            silence_thresh: dB threshold for silence (default -40dB)
            min_silence_ms: Minimum silence duration in ms (default 800ms)

        Returns:
            List of (start_ms, end_ms) tuples for silent segments
        """
        from pydub import AudioSegment
        from pydub.silence import detect_silence

        self.logger.info(f"Detecting silences in: {video_path}")

        # Extract audio from video to temp file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            temp_audio_path = temp_audio.name

        try:
            # Use ffmpeg to extract audio
            cmd = [
                'ffmpeg', '-y', '-i', video_path,
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1',
                temp_audio_path
            ]
            self.logger.info(f"Extracting audio: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode != 0:
                self.logger.error(f"FFmpeg error: {result.stderr}")
                raise RuntimeError(f"Failed to extract audio: {result.stderr}")

            # Load audio and detect silences
            audio = AudioSegment.from_file(temp_audio_path)
            self.logger.info(f"Audio duration: {len(audio)}ms")

            silences = detect_silence(
                audio,
                min_silence_len=min_silence_ms,
                silence_thresh=silence_thresh
            )

            self.logger.info(f"Found {len(silences)} silent segments")
            return silences

        finally:
            # Cleanup temp file
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)

    def generate_keep_segments(
        self,
        video_duration_ms: int,
        silences: List[Tuple[int, int]],
        padding_ms: int = 100
    ) -> List[Tuple[int, int]]:
        """
        Generate list of segments to KEEP (inverse of silences).

        Args:
            video_duration_ms: Total video duration in milliseconds
            silences: List of (start_ms, end_ms) silent segments
            padding_ms: Padding to add around cuts for natural transitions

        Returns:
            List of (start_ms, end_ms) segments to keep
        """
        keep_segments = []
        current_pos = 0

        for silence_start, silence_end in silences:
            # Keep segment before this silence
            if silence_start > current_pos + padding_ms:
                segment_end = min(silence_start + padding_ms, video_duration_ms)
                keep_segments.append((current_pos, segment_end))

            # Move past the silence (with padding)
            current_pos = max(silence_end - padding_ms, current_pos)

        # Keep final segment
        if current_pos < video_duration_ms:
            keep_segments.append((current_pos, video_duration_ms))

        # Merge very close segments
        merged = []
        for segment in keep_segments:
            if merged and segment[0] - merged[-1][1] < 50:  # Less than 50ms gap
                merged[-1] = (merged[-1][0], segment[1])
            else:
                merged.append(segment)

        self.logger.info(f"Generated {len(merged)} keep segments")
        return merged

    def get_video_duration_ms(self, video_path: str) -> int:
        """Get video duration in milliseconds using ffprobe."""
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffprobe failed: {result.stderr}")

        duration_seconds = float(result.stdout.strip())
        return int(duration_seconds * 1000)

    def assemble_video(
        self,
        input_path: str,
        segments: List[Tuple[int, int]],
        output_path: str
    ) -> str:
        """
        Assemble video from segments using FFmpeg.

        Args:
            input_path: Path to input video
            segments: List of (start_ms, end_ms) segments to keep
            output_path: Path for output video

        Returns:
            Path to the output video
        """
        self.logger.info(f"Assembling video with {len(segments)} segments")

        # Create temp directory for segment files
        with tempfile.TemporaryDirectory() as temp_dir:
            segment_files = []

            # Extract each segment
            for i, (start_ms, end_ms) in enumerate(segments):
                segment_path = os.path.join(temp_dir, f"segment_{i:04d}.mp4")
                segment_files.append(segment_path)

                start_sec = start_ms / 1000
                duration_sec = (end_ms - start_ms) / 1000

                cmd = [
                    'ffmpeg', '-y',
                    '-ss', str(start_sec),
                    '-i', input_path,
                    '-t', str(duration_sec),
                    '-c', 'copy',
                    '-avoid_negative_ts', 'make_zero',
                    segment_path
                ]

                self.logger.info(f"Extracting segment {i+1}/{len(segments)}: {start_sec:.2f}s - {start_sec + duration_sec:.2f}s")

                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.warning(f"Segment extraction warning: {result.stderr}")

            # Create concat list file
            concat_list_path = os.path.join(temp_dir, "concat_list.txt")
            with open(concat_list_path, 'w') as f:
                for segment_path in segment_files:
                    f.write(f"file '{segment_path}'\n")

            # Concatenate all segments
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_list_path,
                '-c', 'copy',
                output_path
            ]

            self.logger.info(f"Concatenating segments to: {output_path}")

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error(f"Concatenation error: {result.stderr}")
                raise RuntimeError(f"Failed to concatenate: {result.stderr}")

        self.logger.info(f"Video assembled successfully: {output_path}")
        return output_path

    def edit_video(
        self,
        screen_recording: str,
        face_cam: str = None,
        output_path: str = None,
        silence_thresh: int = -40,
        min_silence_ms: int = 800,
        padding_ms: int = 100
    ) -> Dict[str, Any]:
        """
        Edit video by removing silent segments.

        Args:
            screen_recording: Path to screen recording video
            face_cam: Path to face cam video (optional, for future use)
            output_path: Path for output video (auto-generated if not provided)
            silence_thresh: dB threshold for silence detection
            min_silence_ms: Minimum silence duration to cut
            padding_ms: Padding around cuts

        Returns:
            Dictionary with editing results
        """
        self.logger.info(f"Starting video edit: {screen_recording}")

        # Validate input
        if not os.path.exists(screen_recording):
            raise FileNotFoundError(f"Video not found: {screen_recording}")

        # Generate output path if not provided
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            input_name = Path(screen_recording).stem
            output_path = f"output/edited_{input_name}_{timestamp}.mp4"

        # Get video duration
        original_duration_ms = self.get_video_duration_ms(screen_recording)
        self.logger.info(f"Original duration: {original_duration_ms/1000:.2f}s")

        # Detect silences
        silences = self.detect_silences(
            screen_recording,
            silence_thresh=silence_thresh,
            min_silence_ms=min_silence_ms
        )

        # Calculate total silence time
        total_silence_ms = sum(end - start for start, end in silences)
        self.logger.info(f"Total silence detected: {total_silence_ms/1000:.2f}s")

        # Generate keep segments
        keep_segments = self.generate_keep_segments(
            original_duration_ms,
            silences,
            padding_ms=padding_ms
        )

        # Assemble final video
        self.assemble_video(screen_recording, keep_segments, output_path)

        # Get final duration
        final_duration_ms = self.get_video_duration_ms(output_path)

        result = {
            "output_path": output_path,
            "original_duration_sec": original_duration_ms / 1000,
            "final_duration_sec": final_duration_ms / 1000,
            "time_removed_sec": (original_duration_ms - final_duration_ms) / 1000,
            "segments_kept": len(keep_segments),
            "silences_detected": len(silences),
            "settings": {
                "silence_thresh": silence_thresh,
                "min_silence_ms": min_silence_ms,
                "padding_ms": padding_ms
            }
        }

        self.logger.info(f"Edit complete: {original_duration_ms/1000:.2f}s -> {final_duration_ms/1000:.2f}s")
        return result

    def execute(
        self,
        screen_recording: str,
        face_cam: str = None,
        output_path: str = None,
        silence_thresh: int = -40,
        min_silence_ms: int = 800,
        padding_ms: int = 100,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute the video editing agent.

        Args:
            screen_recording: Path to screen recording
            face_cam: Path to face cam (optional)
            output_path: Output path (optional)
            silence_thresh: Silence threshold in dB
            min_silence_ms: Minimum silence duration
            padding_ms: Padding around cuts

        Returns:
            Dictionary with editing results
        """
        return self.edit_video(
            screen_recording=screen_recording,
            face_cam=face_cam,
            output_path=output_path,
            silence_thresh=silence_thresh,
            min_silence_ms=min_silence_ms,
            padding_ms=padding_ms
        )


if __name__ == "__main__":
    # Example usage
    agent = VideoEditingAgent()

    # Test with sample video
    test_video = "video_samples/video_samples_unedited/Yander pitch demo screen.mp4"

    if os.path.exists(test_video):
        result = agent.edit_video(screen_recording=test_video)
        print(json.dumps(result, indent=2))
    else:
        print(f"Test video not found: {test_video}")
