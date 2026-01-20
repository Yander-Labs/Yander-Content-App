#!/usr/bin/env python3
"""
Creates a script about why agencies should build personal brands instead of running paid ads.
Based on Jordan's experience with Hayes Media.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import create_video_with_talking_points

PERSONAL_BRAND_SCRIPT = {
    "title": "Stop Running Paid Ads for Your Agency: Why Personal Brand Beats Performance Marketing",
    "estimated_length_minutes": 16,
    "hook": {
        "duration_seconds": 15,
        "script": "We were spending $3,000 to acquire a single client through paid ads. Twelve months later, after building a personal brand on YouTube, that number dropped to $500. But the cost savings aren't even the real story. The quality of clients completely transformed. Here's what nobody tells you about agency client acquisition."
    },
    "early_cta": {
        "duration_seconds": 8,
        "script": "If you're an agency owner tired of chasing leads, subscribe. I share what's actually working to grow Hayes Media. Let's get into this."
    },
    "intro": {
        "duration_seconds": 35,
        "script": "I'm Jordan. I run Hayes Media, a marketing agency that did over $1M in 2025. For years, I believed what everyone told me: run paid ads, build funnels, scale with predictable acquisition costs. It worked, kind of. We got clients. But something was off. Today I'm breaking down why I stopped running paid ads for my agency and started building a personal brand instead. And why the numbers prove this is the smarter play for most agency owners."
    },
    "main_sections": [
        {
            "section_title": "The Paid Ads Trap",
            "duration_minutes": 2,
            "script": "Here's what our paid ads looked like. We ran Facebook and Google ads targeting business owners who needed marketing help. Cost per lead was around $150. We'd get maybe 20 leads a month. Of those, 3-4 would book calls. We'd close one. Total cost to acquire that client: $3,000. On paper, the math worked. Average client was worth $15K-$20K over their lifetime. But here's what the spreadsheet didn't show: the clients we acquired through paid ads were fundamentally different from other clients."
        },
        {
            "section_title": "The Hidden Problem with Paid Ad Clients",
            "duration_minutes": 2,
            "script": "Clients from paid ads had three problems. First, they were price shoppers. They clicked on our ad, then clicked on five competitors. They were comparing quotes, not seeking expertise. Second, they were smaller brands. Bigger companies don't hire agencies from Facebook ads. They hire through referrals and reputation. Third, they churned faster. Average retention for paid ad clients was 6 months. For referral clients, it was 14 months. We were paying $3,000 to acquire clients who stayed half as long and paid less. The real CAC when you factor in churn was catastrophic."
        },
        {
            "section_title": "The Cold Email and Referral Baseline",
            "duration_minutes": 2,
            "script": "Meanwhile, our best clients came from two sources: cold email and referrals. Cold email cost us time but almost no money. Maybe $200 in tools. Referrals cost nothing. These clients were different. They came in already trusting us. They weren't comparing five options. They wanted to work with us specifically. Average deal size was 40% higher. Retention was more than double. But cold email doesn't scale infinitely. Referrals are unpredictable. I needed a third channel that combined the trust of referrals with some level of predictability."
        },
        {
            "section_title": "The Personal Brand Experiment",
            "duration_minutes": 2,
            "script": "I started posting on YouTube. Not because I wanted to be an influencer. Because I realized something: the best agencies I knew didn't run ads. Their founders had personal brands. They spoke at conferences. They had podcasts. They were known. My hypothesis: if I could become known for something specific, clients would come to me pre-sold. No price shopping. No comparison calls. Just people who already trusted my expertise and wanted to hire Hayes Media specifically."
        },
        {
            "section_title": "12 Months of Consistent Content",
            "duration_minutes": 2,
            "script": "For 12 months, I posted consistently. Weekly YouTube videos about running and scaling agencies. No viral moments. No overnight success. Just steady, valuable content for agency owners and the business owners who hire agencies. Months 1-3: basically nothing. A few hundred views per video. Zero inbound leads. Months 4-6: starting to see comments, some DMs asking questions. Still no clients. Months 7-9: first inbound lead from YouTube. Then another. Two closed. Months 10-12: consistent inbound. 3-4 qualified leads per month just from content."
        },
        {
            "section_title": "The New Economics",
            "duration_minutes": 2,
            "script": "Let's compare the numbers. Paid ads: $3,000 CAC, 6-month average retention, price-sensitive clients. Personal brand: $500 CAC when you factor in equipment, editing, and my time. 14-month average retention. Clients who come in already trusting us. But here's the real difference: paid ad leads required 3-4 calls to close. YouTube leads often closed on the first call. They'd watched hours of my content. They knew my philosophy. They'd already decided they wanted to work with us. We just needed to confirm fit and discuss scope."
        },
        {
            "section_title": "Why This Works for Agencies Specifically",
            "duration_minutes": 2,
            "script": "This isn't just generic advice. Personal brand works especially well for agencies because of what you're selling. You're selling expertise and trust. Clients need to believe you understand their problems and can solve them. A 15-minute YouTube video demonstrates expertise in a way no ad ever could. Plus, agencies have a content advantage. You're already creating strategies, solving problems, seeing what works. You have endless content ideas from your actual work. You're not making things up. You're sharing real experience."
        },
        {
            "section_title": "The Compounding Effect",
            "duration_minutes": 2,
            "script": "Here's what paid ads can never do: compound. Every dollar you spend on ads disappears once the campaign ends. Turn off the budget, leads stop. Personal brand compounds. A video I made 8 months ago still brings leads today. My content library grows. My authority grows. My audience grows. And it feeds itself. Better clients lead to better case studies lead to better content lead to better clients. Paid ads are a treadmill. Personal brand is an asset that appreciates."
        }
    ],
    "call_to_action": {
        "duration_seconds": 25,
        "script": "If you're running an agency and spending money on ads to acquire clients, I'm not saying stop tomorrow. But start building alongside it. One video a week. One post a day. In 12 months, you might not need those ads at all. Drop a comment with how you're currently acquiring clients. I read every one. And subscribe if you want more on growing agencies without burning cash on ads. Thanks for watching."
    },
    "notes": {
        "total_duration_estimate": "16 minutes",
        "key_context": "Based on Jordan's actual experience with Hayes Media. $3K CAC from ads dropped to $500 after 12 months of YouTube.",
        "tone": "Data-driven, experience-based. Not anti-ads dogma, just showing what worked better."
    }
}


def main():
    # Check character counts first
    print("Section character counts:")
    for section in PERSONAL_BRAND_SCRIPT["main_sections"]:
        char_count = len(section["script"])
        status = "OK" if char_count < 800 else "LONG" if char_count < 1000 else "TOO LONG"
        print(f"  - {section['section_title'][:40]:<40}: {char_count:>4} chars [{status}]")
    print()

    # Create complete video content package with images and talking points
    result = create_video_with_talking_points(
        script=PERSONAL_BRAND_SCRIPT,
        generate_images=True,
        print_progress=True
    )

    return result


if __name__ == "__main__":
    main()
