#!/usr/bin/env python3
"""
Daily Content Generation Script
Run this script daily (via cron) to automatically generate and publish content.

Usage:
    python scripts/run_daily_content.py
    python scripts/run_daily_content.py --count 2

Cron setup (runs at 6am daily):
    crontab -e
    0 6 * * * cd /Users/jordanhayes/content-creation-agents && /usr/bin/python3 scripts/run_daily_content.py >> output/logs/cron.log 2>&1
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

from agents import DailyContentAgent


def setup_logging():
    """Set up logging to file and console."""
    # Create logs directory
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "output",
        "logs"
    )
    os.makedirs(log_dir, exist_ok=True)

    # Log file with date
    log_file = os.path.join(
        log_dir,
        f"daily_content_{datetime.now().strftime('%Y%m%d')}.log"
    )

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("DailyContent")


def save_results(results: dict):
    """Save results to JSON file for tracking."""
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "output",
        "posts",
        f"daily_{datetime.now().strftime('%Y%m%d')}"
    )
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "results.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    return output_file


def main():
    """Main entry point for daily content generation."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate daily content")
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="Number of posts to generate (default: 3)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate content but don't publish to Notion"
    )
    args = parser.parse_args()

    # Set up logging
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("DAILY CONTENT GENERATION STARTED")
    logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Posts requested: {args.count}")
    logger.info("=" * 60)

    try:
        # Initialize agent
        agent = DailyContentAgent()

        # Run daily generation
        results = agent.execute(post_count=args.count)

        # Log results
        logger.info("-" * 60)
        logger.info("RESULTS SUMMARY")
        logger.info(f"Total requested: {results['total_requested']}")
        logger.info(f"Successful: {results['successful']}")
        logger.info(f"Failed: {results['failed']}")
        logger.info("-" * 60)

        # Log each post
        for post in results.get("posts", []):
            if post.get("success"):
                logger.info(f"SUCCESS: {post.get('title')}")
                logger.info(f"  Theme: {post.get('theme')}")
                logger.info(f"  Hook: {post.get('hook', '')[:50]}...")
                logger.info(f"  URL: {post.get('notion_url')}")
            else:
                logger.error(f"FAILED: {post.get('title')}")
                logger.error(f"  Error: {post.get('error')}")

        # Save results
        output_file = save_results(results)
        logger.info(f"Results saved to: {output_file}")

        logger.info("=" * 60)
        logger.info("DAILY CONTENT GENERATION COMPLETE")
        logger.info("=" * 60)

        # Return exit code based on success
        if results["failed"] == 0:
            return 0
        elif results["successful"] > 0:
            return 0  # Partial success is still success
        else:
            return 1  # Complete failure

    except Exception as e:
        logger.exception(f"Fatal error in daily content generation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
