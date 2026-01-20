#!/usr/bin/env python3
"""
Add talking points with images to the existing Employee Quit Signs video page.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.notion_agent import NotionAgent
from agents.image_agent import ImageAgent

# The script content
EMPLOYEE_QUIT_SCRIPT = {
    "title": "The Hidden Signs Your Best Employees Are About to Quit (And You Don't Even Know It)",
    "estimated_length_minutes": 18,
    "hook": {
        "duration_seconds": 15,
        "script": "Your best employee is about to quit. They haven't said anything. Their work is still good. But in three weeks, they'll hand in their notice. I've seen this pattern play out dozens of times. And every time, the signs were there—we just didn't know how to read them. Here's how to spot the warning signs before it's too late."
    },
    "early_cta": {
        "duration_seconds": 8,
        "script": "If you're running a remote team and want to keep your A-players, subscribe. I share what I've learned scaling my agency and building tools to solve this exact problem. Now let's get into it."
    },
    "intro": {
        "duration_seconds": 30,
        "script": "I'm Jordan. I run a marketing agency that's done just over $1M in our best year. And I've lost employees I never saw coming. Not bad employees—my best ones. The ones I thought were happy. The ones doing great work. After enough painful surprises, I started studying this obsessively. I even built a software tool to help solve this problem. Today I'm sharing the hidden signs that predict resignation weeks before it happens."
    },
    "main_sections": [
        {
            "section_title": "Why You're Blind to the Signs",
            "duration_minutes": 2,
            "script": "In a remote environment, you lose the signals you'd naturally pick up in an office. You don't see someone's body language in meetings. You don't notice they stopped eating lunch with the team. You don't catch them scrolling LinkedIn at their desk. Remote work is incredible for productivity. But it creates a visibility gap around team sentiment that most founders don't even realize exists. Your best employees are professionals. They won't let their work slip while they're job hunting. That's what makes them A-players. Which means by the time performance drops, they've already accepted another offer."
        },
        {
            "section_title": "Sign 1: The Collaboration Cliff",
            "duration_minutes": 2.5,
            "script": "The first sign is what I call the Collaboration Cliff. Someone who used to jump into conversations, volunteer for projects, and offer ideas suddenly goes quiet. They're still doing their assigned work. But they've stopped contributing beyond their lane. This is huge. Your best employees over-contribute because they're invested. When they mentally check out, they pull back to just doing their job. Nothing more. I saw this with a senior account manager. Her work stayed solid. But she stopped proposing new processes, stopped mentoring juniors, stopped suggesting improvements. Three weeks later, she resigned. In retrospect, the cliff was obvious. At the time, I just thought she was focused."
        },
        {
            "section_title": "Sign 2: Communication Pattern Shifts",
            "duration_minutes": 2.5,
            "script": "The second sign is a change in communication patterns. This isn't about volume—it's about tone and timing. Someone who responded to Slack within minutes starts taking hours. Messages get shorter. The casual banter disappears. They're still responsive enough to do their job. But the energy is gone. I'm not talking about surveillance. I don't track keystrokes or screenshot people's screens. That's invasive and counterproductive. I'm talking about noticing patterns in how people naturally communicate in channels you already have access to. A team member who used to share wins in the channel stops celebrating. Someone who added context to their updates starts giving bare minimum answers. These shifts matter."
        },
        {
            "section_title": "Sign 3: Silent Disengagement",
            "duration_minutes": 2,
            "script": "The third sign is silent disengagement. This is the hardest to spot because nothing's visibly wrong. Work gets done. Deadlines are met. But in meetings, they're on mute more. Cameras off when they used to be on. They answer questions but don't ask any. They attend but don't participate. Silent disengagement is mental checkout before physical checkout. They've already decided to leave—they just haven't told you yet. In my experience, once someone hits this phase, you have maybe two to three weeks before the resignation email lands."
        },
        {
            "section_title": "Burnout vs. Resignation",
            "duration_minutes": 2,
            "script": "Here's what makes this tricky: burnout looks almost identical to resignation planning. Both show decreased engagement. Both show communication changes. Both show someone pulling back. The difference is the cause. Burnout comes from too much work, unclear priorities, or feeling unsupported. It's fixable. Resignation planning comes from a fundamental decision that their future isn't with you. That's much harder to reverse. How do you tell the difference? Ask directly. Not in a group setting. A genuine one-on-one: 'I've noticed you seem less energized lately. Is there something going on I can help with?' If it's burnout, they'll usually tell you. If it's resignation, they'll deflect. Either way, you learn something."
        },
        {
            "section_title": "The Weekly 15-Minute Review",
            "duration_minutes": 2,
            "script": "Here's the system I use now. Every Friday afternoon, I spend 15 minutes doing a team health review. I go through each team member and ask: Any change in communication patterns this week? Any withdrawal from collaboration? Any signals of disengagement in meetings? I keep a simple spreadsheet. Nothing fancy. Just tracking whether I'm seeing any of the three warning signs. If someone shows one sign for one week, I note it. If they show multiple signs, or one sign persists for two or more weeks, I have a direct conversation. This 15-minute habit has caught every potential resignation in the last year before it happened. Some I was able to save. Others I wasn't. But at least I wasn't blindsided."
        },
        {
            "section_title": "What to Do When You Spot the Signs",
            "duration_minutes": 2,
            "script": "When you see the signs, don't panic. Don't immediately offer a raise. Don't get defensive. Have a genuine conversation. Start with curiosity, not solutions. 'I've noticed you seem less engaged lately. What's going on?' Then listen. Really listen. Sometimes it's something you can fix: workload, unclear growth path, feeling undervalued. Sometimes it's not: they want to try a different industry, relocate, or start their own thing. If it's fixable, fix it fast. Don't make promises you won't keep. Take action within a week. If it's not fixable, part gracefully. Help them transition. Get a great reference. Your remaining team is watching how you handle departures."
        },
        {
            "section_title": "Prevention Is Better Than Detection",
            "duration_minutes": 2,
            "script": "The best strategy isn't catching resignation signs. It's creating an environment where people don't want to leave. For remote teams, this means: regular one-on-ones focused on their growth, not just task updates. Clear paths for advancement. Workload that's challenging but sustainable. Genuine recognition when they do great work. And the hardest one for founders—letting go of control and trusting them to own their domains. People don't quit jobs. They quit managers, quit cultures, quit feeling stuck. Build a place worth staying, and you'll spend less time watching for exit signs."
        }
    ],
    "call_to_action": {
        "duration_seconds": 25,
        "script": "If you found this helpful, drop a comment with how many of these signs you've seen in your team. I read every comment. And if you want a simple template for the weekly team health review I mentioned, I'll put a link in the description. Subscribe for more on running remote teams and scaling your agency. Thanks for watching."
    },
    "notes": {
        "total_duration_estimate": "18 minutes",
        "key_context": "Based on Jordan's experience with his marketing agency (peaked just over $1M/year) and building Yander for remote team management.",
        "tone": "Direct, practical, from experience. No fluff."
    }
}


def main():
    print("=" * 60)
    print("ADDING TALKING POINTS TO EMPLOYEE QUIT SIGNS VIDEO")
    print("=" * 60)

    notion_agent = NotionAgent()
    image_agent = ImageAgent()

    if not image_agent.client:
        print("Error: REPLICATE_API_TOKEN not found")
        return

    # Use the existing page ID from the URL
    # URL: https://www.notion.so/The-Hidden-Signs-Your-Best-Employees-Are-About-to-Quit-And-You-Don-t-Even-Know-It-2edf5ce31c4881d1a92cecef40327732
    page_id = "2edf5ce3-1c48-81d1-a92c-ecef40327732"

    print(f"\n[1/3] Using existing Notion page...")
    print(f"  Page ID: {page_id}")
    print(f"  URL: https://notion.so/{page_id.replace('-', '')}")

    # Generate images
    print(f"\n[2/3] Generating AI images ({len(EMPLOYEE_QUIT_SCRIPT['main_sections']) + 1} images)...")
    print("  This will take about 2 minutes due to rate limiting...")

    images = image_agent.generate_section_images(
        EMPLOYEE_QUIT_SCRIPT,
        include_hook=True,
        include_intro=False
    )

    print(f"\n  Generated {len(images)} images:")
    for img in images:
        print(f"    - {img['section']}")

    # Create talking points subpage
    print(f"\n[3/3] Creating Talking Points subpage...")

    subpage_id = notion_agent.create_talking_points_subpage(
        parent_page_id=page_id,
        script=EMPLOYEE_QUIT_SCRIPT,
        images=images
    )

    if subpage_id:
        subpage_url = f"https://notion.so/{subpage_id.replace('-', '')}"
        print(f"\n  SUCCESS!")
        print(f"  Talking Points: {subpage_url}")
    else:
        print("\n  Error creating talking points subpage")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
