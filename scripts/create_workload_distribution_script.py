#!/usr/bin/env python3
"""
Creates a script about unequal workload distribution in remote marketing agencies.
Includes Notion page, AI-generated images, and Talking Points subpage.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import create_video_with_talking_points

WORKLOAD_DISTRIBUTION_SCRIPT = {
    "title": "Why '3 Clients Per Person' Is a Lie: The Hidden Workload Problem Killing Your Agency",
    "estimated_length_minutes": 15,
    "hook": {
        "duration_seconds": 15,
        "script": "You have three account managers. Each handles three clients. Perfectly balanced, right? Wrong. One of them is drowning while another is coasting. And you have no idea. This invisible imbalance is burning out your best people and you can't even see it happening."
    },
    "early_cta": {
        "duration_seconds": 8,
        "script": "If you run a remote agency and want to keep your team from burning out, subscribe. I share lessons from scaling my agency and building tools to solve exactly these problems."
    },
    "intro": {
        "duration_seconds": 30,
        "script": "I'm Jordan. I run a marketing agency that's done just over $1M in our best year. For a long time, I thought I had workload figured out. Three clients per account manager. Simple math. Then I lost two great employees in three months. Both cited burnout. Both had the same client count as everyone else. That's when I realized: client count is a terrible measure of workload. Today I'm breaking down why this happens and how to actually fix it."
    },
    "main_sections": [
        {
            "section_title": "The Client Count Illusion",
            "duration_minutes": 2,
            "script": "Here's what most agency owners do. They count clients per person and call it fair. Three clients each. Done. But clients aren't equal. One client might need five hours a week. Another needs twenty. One client is organized and responsive. Another sends midnight emergencies and changes scope constantly. One has a single decision-maker. Another has a committee of twelve. When you measure by client count, you're measuring the wrong thing entirely. You're blind to the actual work being done."
        },
        {
            "section_title": "Why This Problem Hides in Remote Teams",
            "duration_minutes": 2,
            "script": "In an office, you'd notice someone struggling. They're at their desk late. They look stressed. You overhear them on difficult calls. Remote work removes all these signals. Your overworked account manager is just a green dot on Slack. Their camera is off in meetings because they're exhausted. They're not complaining because they don't want to seem incapable. Meanwhile, the person with easy clients looks equally busy. Same message frequency, same meeting attendance. The inequality is completely invisible until someone quits."
        },
        {
            "section_title": "The Real Metrics That Matter",
            "duration_minutes": 2,
            "script": "Stop counting clients. Start measuring actual workload indicators. Hours logged per client, not just per person. Communication volume: emails, messages, calls per account. Revision cycles and scope changes. Client responsiveness and how long tasks sit waiting. Meeting frequency and duration. When I started tracking these, I found one account manager spending 30 hours weekly on three clients while another spent 15 hours on the same count. That's not a small difference. That's one person doing double the work."
        },
        {
            "section_title": "The Rebalancing Conversation",
            "duration_minutes": 2,
            "script": "Once you see the imbalance, you need to fix it. This is uncomfortable. You're essentially telling one person they've had it easy. Frame it around the data, not judgment. Show the actual hours and workload metrics. Explain that fair means equal effort, not equal client count. Then redistribute. Maybe the overloaded person keeps two high-touch clients while the other takes four low-maintenance ones. Maybe you reassign the most demanding client to someone with capacity. The key is making decisions based on real workload, not arbitrary counts."
        },
        {
            "section_title": "Building Systems for Ongoing Balance",
            "duration_minutes": 2,
            "script": "Rebalancing once isn't enough. Workload shifts constantly. Clients go through busy seasons. Projects ramp up and wind down. New clients onboard with unknown demands. You need a system for continuous visibility. Weekly workload check-ins where people self-report capacity. Monthly reviews of time tracking data. Clear escalation paths when someone's hitting their limit. The goal is catching imbalances in weeks, not months. Before burnout happens, not after."
        },
        {
            "section_title": "Why I Built Yander",
            "duration_minutes": 2,
            "script": "After losing those employees, I became obsessed with this problem. I tried spreadsheets, time tracking tools, weekly surveys. Everything was manual and lagging. By the time I spotted issues, the damage was done. So I built Yander. It tracks the signals that indicate workload: communication patterns, task volume, response times. It surfaces imbalances automatically before they become burnout. I'm not saying you need Yander specifically. But you need something that gives you real visibility into workload across your remote team. Gut feel and client counts aren't enough."
        },
        {
            "section_title": "The Retention Connection",
            "duration_minutes": 1.5,
            "script": "Here's what nobody tells you: unequal workload is the number one hidden cause of turnover in agencies. People don't quit because work is hard. They quit because work feels unfair. When your best performer realizes they're carrying twice the load for the same pay, resentment builds. They won't tell you. They'll just start interviewing. Fix the visibility problem and you fix a massive retention problem you didn't even know you had."
        }
    ],
    "call_to_action": {
        "duration_seconds": 25,
        "script": "If this hit home, drop a comment with how you currently measure workload in your agency. I'm genuinely curious what's working for people. If you want to check out Yander, link's in the description. And subscribe for more on running remote agencies without burning out your team. Thanks for watching."
    },
    "notes": {
        "total_duration_estimate": "15 minutes",
        "key_context": "Based on Jordan's experience losing employees to burnout despite 'equal' client loads. Introduces Yander naturally as solution he built.",
        "tone": "Problem-focused first, solution-focused second. Yander mention is casual, not salesy."
    }
}


def main():
    # Check character counts first
    print("Section character counts:")
    for section in WORKLOAD_DISTRIBUTION_SCRIPT["main_sections"]:
        char_count = len(section["script"])
        status = "OK" if char_count < 800 else "LONG" if char_count < 1000 else "TOO LONG"
        print(f"  - {section['section_title'][:40]:<40}: {char_count:>4} chars [{status}]")
    print()

    # Create complete video content package with images and talking points
    result = create_video_with_talking_points(
        script=WORKLOAD_DISTRIBUTION_SCRIPT,
        generate_images=True,  # Set to False to skip image generation
        print_progress=True
    )

    return result


if __name__ == "__main__":
    main()
