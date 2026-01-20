#!/usr/bin/env python3
"""
Creates a script about why agencies need real-time financial tracking.
Based on Jordan's experience with Hayes Media's bookkeeper and financial systems.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import create_video_with_talking_points

FINANCIAL_TRACKING_SCRIPT = {
    "title": "Why Your Agency Is Bleeding Money: The Financial Tracking System Most Owners Ignore",
    "estimated_length_minutes": 14,
    "hook": {
        "duration_seconds": 15,
        "script": "Most agency owners have no idea how much money they're actually making until two weeks after the month is over. By then, it's too late. You've already overspent, missed the warning signs, and that software subscription you forgot about just renewed for another year. Here's how I track every dollar in real-time."
    },
    "early_cta": {
        "duration_seconds": 8,
        "script": "If you run an agency and want to actually understand your numbers, subscribe. I share what's working at Hayes Media every week. Let's get into this."
    },
    "intro": {
        "duration_seconds": 30,
        "script": "I'm Jordan. I run Hayes Media, and we did over $1M in 2025. For years, I treated financials as an afterthought. I'd get a P&L from my accountant weeks after the month ended and just hope the numbers looked okay. That approach almost killed my margins. Today I'm breaking down the financial tracking system we built and why waiting for your accountant is costing you money."
    },
    "main_sections": [
        {
            "section_title": "The Accountant Delay Problem",
            "duration_minutes": 2,
            "script": "Here's how most agencies handle finances. They have an accountant or bookkeeping service. At the end of each month, they send over bank statements and receipts. Two weeks later, they get a P&L. They glance at it, see if profit is positive, and move on. The problem: by the time you see that report, you're already halfway through the next month. That software trial you forgot to cancel? Already charged. That contractor who overbilled? Already paid. That client who's costing more to service than they're paying? You've already renewed their contract. Financial data that's two weeks old isn't information. It's history."
        },
        {
            "section_title": "The Real Cost of Flying Blind",
            "duration_minutes": 2,
            "script": "Let me tell you what flying blind cost me. In one quarter, I discovered we were paying for three different project management tools. Nobody remembered signing up for two of them. That was $400 a month for 8 months before I noticed. We had a contractor billing 25% more hours than agreed. Took me three months to catch it because I wasn't looking at the numbers until they were ancient history. Our biggest client was actually our least profitable when I finally did the math. We'd given them so many extras and scope additions that we were making 8% margin on a client I thought was our best. Total cost of not tracking in real-time: roughly $15K in one year. That's pure profit I lit on fire."
        },
        {
            "section_title": "Building Your Own Financial Tracker",
            "duration_minutes": 2,
            "script": "I stopped relying on monthly reports and built our own tracking system. Nothing fancy. A spreadsheet that gets updated multiple times per month. Every expense categorized: team costs, software, contractors, operations. Every revenue line tracked: which clients, which services, what margins. The key is frequency. We don't wait for month-end. We update weekly at minimum, sometimes more. When a new expense hits, it goes in the tracker that week. When a client pays, it's logged immediately. I can open this spreadsheet any day and know exactly where we stand. No surprises. No waiting two weeks to find out we overspent."
        },
        {
            "section_title": "The Bookkeeper Role",
            "duration_minutes": 2,
            "script": "I have a bookkeeper on my team. Not an external service that sends reports monthly. Someone internal who owns the numbers. Their job: update the financial tracker multiple times per month. Process payments to contractors and team members. Double-check every payment against our SOPs before it goes out. This catches errors before they happen. Last month, they caught a contractor invoice that was $800 higher than our agreement. The month before, they noticed a software subscription had increased without notification. These aren't things you catch with a monthly P&L. You catch them when someone is actively watching the money flow in real-time."
        },
        {
            "section_title": "The Software Audit",
            "duration_minutes": 2,
            "script": "Every quarter, I do a software audit using our tracker. I pull the list of every tool we're paying for. For each one, I ask: who uses this? When did they last use it? Can we consolidate or eliminate it? Agencies are notorious for software bloat. You sign up for a tool to solve one problem, then forget about it. Or you keep paying for the starter tier of something you upgraded away from. In my last audit, I cut $600 in monthly software costs. Tools we weren't using, redundant subscriptions, plans we could downgrade. That's $7,200 a year found in 30 minutes of looking at a spreadsheet. But only because the spreadsheet existed and was accurate."
        },
        {
            "section_title": "Real-Time Margin Tracking",
            "duration_minutes": 2,
            "script": "The most valuable part: real-time margin tracking by client. Every client has a target margin. We track hours spent, contractor costs, and any direct expenses. If a client starts trending below target margin, I know within weeks, not months. This changed how we handle scope creep. When the team logs extra hours on a client, it shows up in the margin calculation immediately. I can have a conversation with that client about scope before we've lost money, not after. We went from having a wide range of client profitability to having nearly every client within our target margin band. Not because we got lucky. Because we could see the numbers while there was still time to act."
        },
        {
            "section_title": "What to Track Weekly",
            "duration_minutes": 2,
            "script": "Here's what goes in our tracker, updated weekly. Revenue: cash received, invoices outstanding, projected revenue by client. Expenses: team payroll, contractor payments, software and tools, operational costs. Margins: gross margin overall, margin by client, margin by service line. Cash position: current bank balance, accounts receivable, upcoming major expenses. This takes my bookkeeper maybe two hours a week. The ROI on those two hours is probably 50x. Every dollar you don't track is a dollar that can leak out without you noticing. And in an agency, small leaks add up fast."
        }
    ],
    "call_to_action": {
        "duration_seconds": 25,
        "script": "If you're running an agency and only seeing your numbers monthly, you're operating with a blindfold. Start simple. Build a spreadsheet. Track expenses weekly. Know your margins by client. You'll find money you didn't know you were losing. Drop a comment with how often you currently look at your agency finances. I'm curious how many of you are in the same boat I was. Subscribe for more on running a profitable agency. Thanks for watching."
    },
    "notes": {
        "total_duration_estimate": "14 minutes",
        "key_context": "Based on Jordan's experience losing $15K in one year from not tracking finances closely. Built internal bookkeeper role to solve this.",
        "tone": "Practical, experience-based. Focus on the real costs of not tracking and the simple solution."
    }
}


def main():
    # Check character counts first
    print("Section character counts:")
    for section in FINANCIAL_TRACKING_SCRIPT["main_sections"]:
        char_count = len(section["script"])
        status = "OK" if char_count < 800 else "LONG" if char_count < 1000 else "TOO LONG"
        print(f"  - {section['section_title'][:40]:<40}: {char_count:>4} chars [{status}]")
    print()

    # Create complete video content package with images and talking points
    result = create_video_with_talking_points(
        script=FINANCIAL_TRACKING_SCRIPT,
        generate_images=True,
        print_progress=True
    )

    return result


if __name__ == "__main__":
    main()
