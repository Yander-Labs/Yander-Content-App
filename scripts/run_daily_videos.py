#!/usr/bin/env python3
"""
Daily YouTube Video Generation Script
Run this script daily (via cron) to automatically generate video ideas and scripts.

Usage:
    python scripts/run_daily_videos.py
    python scripts/run_daily_videos.py --count 2

Cron setup (runs at 7am daily):
    crontab -e
    0 7 * * * cd /Users/jordanhayes/content-creation-agents && /usr/bin/python3 scripts/run_daily_videos.py >> output/logs/cron.log 2>&1
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from orchestrator import ContentCreationOrchestrator


# Video themes to rotate through
VIDEO_THEMES = [
    {
        "name": "agency_operations",
        "topics": ["agency operations", "systems", "processes", "efficiency"],
        "description": "How to run a more efficient agency"
    },
    {
        "name": "team_management",
        "topics": ["team management", "hiring", "remote teams", "leadership"],
        "description": "Building and managing agency teams"
    },
    {
        "name": "client_relationships",
        "topics": ["client retention", "client communication", "account management"],
        "description": "Better client relationships and retention"
    },
    {
        "name": "scaling",
        "topics": ["scaling agency", "growth strategies", "revenue growth"],
        "description": "Scaling your agency sustainably"
    },
    {
        "name": "service_delivery",
        "topics": ["service delivery", "quality control", "project management"],
        "description": "Delivering exceptional client work"
    },
    {
        "name": "financial_management",
        "topics": ["agency finances", "pricing", "profitability", "cash flow"],
        "description": "Financial management for agencies"
    },
]


def setup_logging():
    """Set up logging to file and console."""
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "output",
        "logs"
    )
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir,
        f"daily_videos_{datetime.now().strftime('%Y%m%d')}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("DailyVideos")


def get_theme_index():
    """Get the current theme index and rotate."""
    state_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "daily_video_state.json"
    )

    # Load or initialize state
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
    else:
        state = {"last_theme_index": -1}

    # Get next theme index
    next_index = (state["last_theme_index"] + 1) % len(VIDEO_THEMES)

    # Save state
    state["last_theme_index"] = next_index
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)

    return next_index


def save_results(results: list):
    """Save results to JSON file for tracking."""
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "output",
        "videos",
        f"daily_{datetime.now().strftime('%Y%m%d')}"
    )
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "results.json")
    with open(output_file, "w") as f:
        json.dump({
            "date": datetime.now().isoformat(),
            "videos": results
        }, f, indent=2)

    return output_file


def main():
    """Main entry point for daily video generation."""
    parser = argparse.ArgumentParser(description="Generate daily YouTube video ideas and scripts")
    parser.add_argument(
        "--count",
        type=int,
        default=2,
        help="Number of videos to generate (default: 2)"
    )
    args = parser.parse_args()

    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("DAILY YOUTUBE VIDEO GENERATION STARTED")
    logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Videos requested: {args.count}")
    logger.info("=" * 60)

    results = []
    successful = 0
    failed = 0

    try:
        # Load creator context
        context_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data",
            "jordan_hayes_info.txt"
        )
        user_data = None
        if os.path.exists(context_file):
            with open(context_file, "r") as f:
                user_data = f.read()

        # Initialize orchestrator
        orchestrator = ContentCreationOrchestrator()

        for i in range(args.count):
            # Get rotating theme
            theme_index = get_theme_index()
            theme = VIDEO_THEMES[theme_index]

            logger.info(f"\n--- Video {i+1}/{args.count} ---")
            logger.info(f"Theme: {theme['name']} - {theme['description']}")
            logger.info(f"Topics: {', '.join(theme['topics'])}")

            try:
                # Create video content
                result = orchestrator.create_video_content(
                    user_data=user_data,
                    topics=theme['topics'],
                    video_index=0,
                    tone="professional"
                )

                if "error" in result:
                    logger.error(f"Failed: {result.get('error')}")
                    results.append({
                        "success": False,
                        "theme": theme['name'],
                        "error": result.get('error')
                    })
                    failed += 1
                else:
                    logger.info(f"SUCCESS: {result.get('idea', {}).get('title', 'Unknown')}")
                    if result.get('notion', {}).get('page_url'):
                        logger.info(f"  Notion: {result['notion']['page_url']}")

                    results.append({
                        "success": True,
                        "theme": theme['name'],
                        "title": result.get('idea', {}).get('title'),
                        "notion_url": result.get('notion', {}).get('page_url'),
                        "mindmap_file": result.get('mindmap', {}).get('svg_file')
                    })
                    successful += 1

            except Exception as e:
                logger.exception(f"Error creating video: {e}")
                results.append({
                    "success": False,
                    "theme": theme['name'],
                    "error": str(e)
                })
                failed += 1

        # Log summary
        logger.info("\n" + "-" * 60)
        logger.info("RESULTS SUMMARY")
        logger.info(f"Total requested: {args.count}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info("-" * 60)

        # Save results
        output_file = save_results(results)
        logger.info(f"Results saved to: {output_file}")

        logger.info("=" * 60)
        logger.info("DAILY YOUTUBE VIDEO GENERATION COMPLETE")
        logger.info("=" * 60)

        return 0 if failed == 0 else (0 if successful > 0 else 1)

    except Exception as e:
        logger.exception(f"Fatal error in daily video generation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
