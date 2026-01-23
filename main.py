#!/usr/bin/env python3
"""
Content Creation Agents CLI
Main entry point for the content creation agent system.
"""

import argparse
import json
import os
import sys
from dotenv import load_dotenv
from orchestrator import ContentCreationOrchestrator
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()


def check_environment():
    """Check if required environment variables are set."""
    required_vars = ['ANTHROPIC_API_KEY']
    optional_vars = ['NOTION_API_KEY', 'NOTION_DATABASE_ID']

    missing_required = [var for var in required_vars if not os.getenv(var)]

    if missing_required:
        print(f"{Fore.RED}✗ Missing required environment variables:{Style.RESET_ALL}")
        for var in missing_required:
            print(f"  - {var}")
        print(f"\n{Fore.YELLOW}Please create a .env file based on .env.example{Style.RESET_ALL}")
        return False

    missing_optional = [var for var in optional_vars if not os.getenv(var)]
    if missing_optional:
        print(f"{Fore.YELLOW}⚠ Optional environment variables not set:{Style.RESET_ALL}")
        for var in missing_optional:
            print(f"  - {var}")
        print(f"{Fore.YELLOW}Some features may not work without these.{Style.RESET_ALL}\n")

    return True


def create_video_command(args):
    """Handle video creation command."""
    if not check_environment():
        sys.exit(1)

    orchestrator = ContentCreationOrchestrator()

    # Load tool info from file if provided
    tool_info = None
    if args.tool_info_file:
        with open(args.tool_info_file, 'r') as f:
            tool_info = f.read()

    # Load user data from file if provided
    user_data = None
    if args.user_data_file:
        with open(args.user_data_file, 'r') as f:
            user_data = f.read()

    # Parse topics
    topics = args.topics.split(',') if args.topics else None

    # Create video
    result = orchestrator.create_video_content(
        tool_info=tool_info,
        user_data=user_data,
        topics=topics,
        video_index=args.index,
        tone=args.tone
    )

    # Save full result
    output_file = f"output/video_result_{result.get('created_at', 'unknown').replace(':', '-')}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n{Fore.GREEN}Full result saved to: {output_file}{Style.RESET_ALL}")


def create_post_command(args):
    """Handle post creation command."""
    if not check_environment():
        sys.exit(1)

    orchestrator = ContentCreationOrchestrator()

    # Load tool info from file if provided
    tool_info = None
    if args.tool_info_file:
        with open(args.tool_info_file, 'r') as f:
            tool_info = f.read()

    # Load user data from file if provided
    user_data = None
    if args.user_data_file:
        with open(args.user_data_file, 'r') as f:
            user_data = f.read()

    # Parse topics
    topics = args.topics.split(',') if args.topics else None

    # Create post
    result = orchestrator.create_post_content(
        tool_info=tool_info,
        user_data=user_data,
        topics=topics,
        post_index=args.index,
        tone=args.tone
    )

    # Save full result
    output_file = f"output/post_result_{result.get('created_at', 'unknown').replace(':', '-')}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n{Fore.GREEN}Full result saved to: {output_file}{Style.RESET_ALL}")


def batch_command(args):
    """Handle batch creation command."""
    if not check_environment():
        sys.exit(1)

    orchestrator = ContentCreationOrchestrator()

    # Load tool info and user data
    tool_info = None
    if args.tool_info_file:
        with open(args.tool_info_file, 'r') as f:
            tool_info = f.read()

    user_data = None
    if args.user_data_file:
        with open(args.user_data_file, 'r') as f:
            user_data = f.read()

    topics = args.topics.split(',') if args.topics else None

    # Create batch
    if args.type == 'video':
        results = orchestrator.batch_create_videos(
            count=args.count,
            tool_info=tool_info,
            user_data=user_data,
            topics=topics,
            tone=args.tone
        )
    else:
        results = orchestrator.batch_create_posts(
            count=args.count,
            tool_info=tool_info,
            user_data=user_data,
            topics=topics,
            tone=args.tone
        )

    # Save results
    output_file = f"output/batch_{args.type}_{args.count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{Fore.GREEN}Batch results saved to: {output_file}{Style.RESET_ALL}")


def notify_editor_command(args):
    """Handle editor notification command."""
    if not check_environment():
        sys.exit(1)

    orchestrator = ContentCreationOrchestrator()

    # Parse video files
    video_files = args.files.split(',')

    result = orchestrator.notify_editor(
        notion_page_id=args.page_id,
        video_files=video_files,
        notes=args.notes
    )

    print(f"\n{Fore.CYAN}Notification result:{Style.RESET_ALL}")
    print(json.dumps(result, indent=2))


def edit_video_command(args):
    """Handle video editing command."""
    from agents import VideoEditingAgent

    print(f"{Fore.CYAN}Starting video editing...{Style.RESET_ALL}")

    agent = VideoEditingAgent()

    try:
        result = agent.edit_video(
            screen_recording=args.screen,
            face_cam=args.face_cam,
            output_path=args.output,
            silence_thresh=args.silence_thresh,
            min_silence_ms=args.min_silence,
            padding_ms=args.padding
        )

        print(f"\n{Fore.GREEN}Video editing complete!{Style.RESET_ALL}")
        print(f"  Original duration: {result['original_duration_sec']:.2f}s")
        print(f"  Final duration:    {result['final_duration_sec']:.2f}s")
        print(f"  Time removed:      {result['time_removed_sec']:.2f}s")
        print(f"  Segments kept:     {result['segments_kept']}")
        print(f"\n{Fore.GREEN}Output saved to: {result['output_path']}{Style.RESET_ALL}")

        # Save result JSON
        result_file = result['output_path'].replace('.mp4', '_result.json')
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Result details: {result_file}")

    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


def youtube_insights_command(args):
    """Handle YouTube insights command."""
    from agents import YouTubeTranscriptAgent

    print(f"{Fore.CYAN}Fetching YouTube transcript...{Style.RESET_ALL}")

    agent = YouTubeTranscriptAgent()

    try:
        result = agent.execute(
            youtube_url=args.url,
            prompt=args.prompt,
            save_transcript=not args.no_save,
        )

        if result.get("status") == "error":
            print(f"{Fore.RED}Error: {result.get('error')}{Style.RESET_ALL}")
            sys.exit(1)

        print(f"\n{Fore.GREEN}Transcript fetched successfully!{Style.RESET_ALL}")
        print(f"  Video ID:    {result['video_id']}")
        print(f"  Duration:    {result['duration_seconds']:.0f}s")
        print(f"  Words:       {result['word_count']}")
        print(f"  Language:    {result['language']}")
        print(f"  Auto-gen:    {result['is_auto_generated']}")

        if result.get('transcript_file'):
            print(f"\n{Fore.GREEN}Transcript saved to: {result['transcript_file']}{Style.RESET_ALL}")

        if result.get('analysis'):
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"ANALYSIS")
            print(f"{'='*60}{Style.RESET_ALL}\n")
            print(result['analysis'])

    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


def transcribe_command(args):
    """Handle transcription command."""
    from agents import TranscriptionAgent

    print(f"{Fore.CYAN}Starting transcription...{Style.RESET_ALL}")

    agent = TranscriptionAgent(
        model_size=args.model_size,
        device=args.device,
        language=args.language if args.language != "auto" else None,
    )

    try:
        result = agent.transcribe(
            input_path=args.input,
            output_path=args.output,
            beam_size=args.beam_size,
            vad_filter=not args.no_vad,
            cleanup_with_claude=args.cleanup,
        )

        print(f"\n{Fore.GREEN}Transcription complete!{Style.RESET_ALL}")
        print(f"  Duration:    {result['duration_seconds']:.2f}s")
        print(f"  Words:       {result['word_count']}")
        print(f"  Language:    {result['language']}")
        print(f"\n{Fore.GREEN}Transcript saved to: {result['output_path']}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Content Creation Agents - AI-powered content workflow automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a video with topics
  python main.py create-video --topics "client retention,automation" --tone professional

  # Create a post
  python main.py create-post --topics "agency growth" --user-data-file data/my_data.txt

  # Create 5 videos in batch
  python main.py batch --type video --count 5 --topics "marketing,growth"

  # Notify editor about recorded files
  python main.py notify-editor --page-id abc123 --files "video1.mp4,video2.mp4" --notes "Great takes!"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Create video command
    video_parser = subparsers.add_parser('create-video', help='Create a video content package')
    video_parser.add_argument('--tool-info-file', help='File containing tool information')
    video_parser.add_argument('--user-data-file', help='File containing user data')
    video_parser.add_argument('--topics', help='Comma-separated list of topics')
    video_parser.add_argument('--index', type=int, default=0, help='Index of idea to use')
    video_parser.add_argument('--tone', default='professional', choices=['professional', 'casual', 'educational'])
    video_parser.set_defaults(func=create_video_command)

    # Create post command
    post_parser = subparsers.add_parser('create-post', help='Create a post content package')
    post_parser.add_argument('--tool-info-file', help='File containing tool information')
    post_parser.add_argument('--user-data-file', help='File containing user data')
    post_parser.add_argument('--topics', help='Comma-separated list of topics')
    post_parser.add_argument('--index', type=int, default=0, help='Index of idea to use')
    post_parser.add_argument('--tone', default='professional', choices=['professional', 'casual', 'educational'])
    post_parser.set_defaults(func=create_post_command)

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Create multiple content pieces')
    batch_parser.add_argument('--type', required=True, choices=['video', 'post'], help='Type of content')
    batch_parser.add_argument('--count', type=int, required=True, help='Number of items to create')
    batch_parser.add_argument('--tool-info-file', help='File containing tool information')
    batch_parser.add_argument('--user-data-file', help='File containing user data')
    batch_parser.add_argument('--topics', help='Comma-separated list of topics')
    batch_parser.add_argument('--tone', default='professional', choices=['professional', 'casual', 'educational'])
    batch_parser.set_defaults(func=batch_command)

    # Notify editor command
    notify_parser = subparsers.add_parser('notify-editor', help='Notify video editor')
    notify_parser.add_argument('--page-id', required=True, help='Notion page ID')
    notify_parser.add_argument('--files', required=True, help='Comma-separated list of video files')
    notify_parser.add_argument('--notes', help='Additional notes for editor')
    notify_parser.set_defaults(func=notify_editor_command)

    # Edit video command
    edit_parser = subparsers.add_parser('edit-video', help='Auto-edit video by removing silences')
    edit_parser.add_argument('--screen', required=True, help='Path to screen recording video')
    edit_parser.add_argument('--face-cam', help='Path to face cam video (optional)')
    edit_parser.add_argument('--output', help='Output path for edited video')
    edit_parser.add_argument('--silence-thresh', type=int, default=-40, help='Silence threshold in dB (default: -40)')
    edit_parser.add_argument('--min-silence', type=int, default=800, help='Minimum silence duration in ms (default: 800)')
    edit_parser.add_argument('--padding', type=int, default=100, help='Padding around cuts in ms (default: 100)')
    edit_parser.set_defaults(func=edit_video_command)

    # Transcribe command
    transcribe_parser = subparsers.add_parser('transcribe', help='Transcribe video/audio to text')
    transcribe_parser.add_argument('--input', '-i', required=True, help='Path to video or audio file')
    transcribe_parser.add_argument('--output', '-o', help='Output path for transcript')
    transcribe_parser.add_argument('--model-size', default='base',
                                   choices=['tiny', 'base', 'small', 'medium', 'large-v3'],
                                   help='Whisper model size (default: base)')
    transcribe_parser.add_argument('--device', default='auto', choices=['auto', 'cpu', 'cuda'],
                                   help='Device to run on (default: auto)')
    transcribe_parser.add_argument('--language', default='en',
                                   help='Language code or "auto" for detection (default: en)')
    transcribe_parser.add_argument('--beam-size', type=int, default=5,
                                   help='Beam size for decoding (default: 5)')
    transcribe_parser.add_argument('--no-vad', action='store_true',
                                   help='Disable Voice Activity Detection')
    transcribe_parser.add_argument('--cleanup', action='store_true',
                                   help='Use Claude to clean up transcript')
    transcribe_parser.set_defaults(func=transcribe_command)

    # YouTube insights command
    youtube_parser = subparsers.add_parser('youtube-insights', help='Fetch YouTube transcript and get AI insights')
    youtube_parser.add_argument('--url', '-u', required=True, help='YouTube video URL')
    youtube_parser.add_argument('--prompt', '-p', default='Summarize the key points and main takeaways from this video.',
                                help='Analysis prompt (what insights do you want?)')
    youtube_parser.add_argument('--no-save', action='store_true',
                                help='Do not save transcript to file')
    youtube_parser.set_defaults(func=youtube_insights_command)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    from datetime import datetime
    main()
