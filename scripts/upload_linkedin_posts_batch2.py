#!/usr/bin/env python3
"""
Script to create and upload batch 2 of LinkedIn posts for marketing agency owners to Notion.
Following content guidelines: no client bashing, no negative hiring stories, no emojis, no hashtags.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.notion_agent import NotionAgent

# 5 Long-form LinkedIn posts for marketing agency owners - Batch 2
LINKEDIN_POSTS = [
    {
        "idea": {
            "title": "Why Your Best People Keep Leaving"
        },
        "post": {
            "hook": "Your best employees aren't leaving for more money. They're leaving because they don't feel safe.",
            "full_post": """Your best employees aren't leaving for more money.

They're leaving because they don't feel safe.

I learned this the hard way when I noticed a pattern at my agency. Our top performers would hit their stride, deliver incredible work for 12-18 months, then quietly start job hunting.

Exit interviews told me nothing useful. "Found a better opportunity" was the standard answer.

Then one former team member was honest with me over coffee.

"I never felt like I could make a mistake," she said. "Every client call felt like a test. Every project felt like my job was on the line."

That conversation forced me to look in the mirror.

I thought I was building a high-performance culture. I was actually building a culture of fear.

There's a difference between high standards and high anxiety.

High standards mean clear expectations, honest feedback, and room to grow.

High anxiety means people hide problems instead of solving them. They play it safe instead of innovating. They protect themselves instead of protecting the work.

The agencies that retain their best people understand something crucial:

Psychological safety isn't soft. It's strategic.

When people feel safe to speak up, you catch problems early. When they feel safe to experiment, you get better ideas. When they feel safe to admit mistakes, you build a learning organization.

I started making changes. Weekly check-ins focused on support, not surveillance. Public recognition of calculated risks, even when they didn't work. Zero tolerance for blame culture in post-mortems.

The result wasn't just better retention. It was better work.

Your culture isn't what you say in all-hands meetings. It's how people feel on a random Tuesday afternoon.

What would your team say about your culture if they knew you'd never find out?""",
            "key_takeaways": [
                "Fear-based cultures drive away top performers",
                "Psychological safety enables innovation and problem-solving",
                "High standards and high anxiety are not the same thing",
                "Culture is defined by daily experiences, not mission statements"
            ],
            "hashtags": []
        }
    },
    {
        "idea": {
            "title": "The Global Talent Advantage Most Agencies Ignore"
        },
        "post": {
            "hook": "I used to think the best talent lived within 50 miles of my office. That belief was costing me hundreds of thousands of dollars.",
            "full_post": """I used to think the best talent lived within 50 miles of my office.

That belief was costing me hundreds of thousands of dollars.

When I finally embraced remote hiring, I started with one role. A project manager position I'd been struggling to fill locally for months.

I expanded the search globally. Within two weeks, I found someone in Eastern Europe who had more relevant experience than any local candidate. They were hungry, professional, and brought a work ethic that elevated our entire team.

That one hire changed how I think about building agencies.

Here's what I've learned hiring globally:

Talent is everywhere. Opportunity is not.

There are brilliant marketers, designers, and strategists in countries where the cost of living is a fraction of major US cities. They have the same skills, the same education, often better English than you'd expect.

What they don't have is access to the opportunities you can provide.

This isn't about finding "cheap labor." That mindset leads to bad hires and worse relationships.

It's about finding exceptional people who are genuinely grateful for the opportunity and motivated to prove themselves. People who see your agency as a career, not a stepping stone.

The practical benefits are real. You can build a stronger team at a lower cost. You can offer competitive salaries that transform someone's life while staying profitable. You get coverage across time zones.

But the unexpected benefit was better.

My global team members brought perspectives I never would have found locally. They challenged assumptions. They introduced processes from companies I'd never heard of. They made us better.

Most agencies limit their talent pool to their zip code.

The world has never been more connected. The question is whether you'll take advantage of it.

Where have you found your best remote hires?""",
            "key_takeaways": [
                "Global talent pools offer exceptional candidates",
                "Cost-effectiveness and quality are not mutually exclusive",
                "Remote hiring provides access to motivated, hungry professionals",
                "Diverse perspectives strengthen agency capabilities"
            ],
            "hashtags": []
        }
    },
    {
        "idea": {
            "title": "The Problem With Waiting Until It's Obvious"
        },
        "post": {
            "hook": "By the time you notice a team member is burned out, they've already been drowning for months.",
            "full_post": """By the time you notice a team member is burned out, they've already been drowning for months.

By the time a client complains, they've been frustrated for weeks.

By the time your best performer resigns, they mentally checked out long ago.

This is the trap most agency owners fall into. We manage reactively instead of proactively.

I used to pride myself on having an "open door policy." Anyone could come to me with problems. What I didn't realize was that by the time problems walked through my door, they'd already done their damage.

The best leaders I've studied don't wait for problems to announce themselves.

They build systems to detect signals early.

Think about it. A team member's workload creeping up week over week is a signal. A usually responsive client going quiet is a signal. A top performer declining optional projects is a signal.

None of these are problems yet. But they're all warnings.

The shift for me came when I stopped asking "what problems do we have?" and started asking "what problems are we about to have?"

I started tracking leading indicators, not just lagging ones. Regular check-ins focused on capacity, not just status. Client health scores based on engagement patterns, not just renewal dates.

The ROI was immediate.

We caught workload imbalances before burnout. We addressed client concerns before they escalated. We had retention conversations before resignation letters.

Reactive management feels productive because you're always solving problems.

Proactive management feels slower because you're preventing problems nobody sees.

But prevented problems have infinite ROI.

What early warning signs do you wish you'd caught sooner?""",
            "key_takeaways": [
                "Problems are visible long before they become crises",
                "Leading indicators matter more than lagging indicators",
                "Proactive management prevents rather than solves problems",
                "Early intervention has the highest ROI"
            ],
            "hashtags": []
        }
    },
    {
        "idea": {
            "title": "What Losing One Person Actually Costs"
        },
        "post": {
            "hook": "Replacing a team member costs 50-200% of their annual salary. But that's not the real expense.",
            "full_post": """Replacing a team member costs 50-200% of their annual salary.

But that's not the real expense.

Last year I did a full accounting of what one departure actually cost our agency. Not just the obvious costs. Everything.

The recruiting fees and job posting costs were easy to calculate. So were the hours spent interviewing, the training time, the slower productivity during ramp-up.

But the hidden costs were staggering.

The institutional knowledge that walked out the door. That person knew our clients' preferences, our internal shortcuts, the context behind past decisions. That knowledge took two years to build and disappeared in two weeks.

The impact on the team left behind. Redistributed workload. Lowered morale. The quiet conversations wondering "should I be looking too?"

The client relationships that weakened. Clients build trust with people, not logos. Transitions always carry risk, no matter how smooth.

The management time spent on damage control instead of growth.

When I added it all up, that one departure cost us roughly 4x their salary in real and opportunity costs.

That math changed how I think about retention.

Every dollar spent keeping good people is worth four dollars in replacement costs avoided. Every hour invested in someone's growth is an hour not spent searching for their replacement.

The agencies that win long-term don't just hire well. They create environments where leaving feels like losing something valuable.

Retention isn't an HR initiative. It's a business strategy.

What's your actual cost when someone leaves?""",
            "key_takeaways": [
                "True turnover costs far exceed salary replacement",
                "Institutional knowledge loss is often the biggest hidden cost",
                "Retention investment has 4x or better ROI",
                "Turnover impacts team morale and client relationships"
            ],
            "hashtags": []
        }
    },
    {
        "idea": {
            "title": "The Hardest Skill Nobody Teaches Agency Owners"
        },
        "post": {
            "hook": "The thing that got you here won't get you there. And for most agency owners, that thing is doing the work yourself.",
            "full_post": """The thing that got you here won't get you there.

And for most agency owners, that thing is doing the work yourself.

I built my agency on my ability to deliver great work. Clients hired us because of my skills, my relationships, my attention to detail.

That same identity almost killed the business.

At $500K in revenue, I was still reviewing every deliverable. Still on every client call. Still the bottleneck for every decision.

I told myself it was about quality. The truth was I didn't trust anyone else to care as much as I did.

A mentor asked me a question I couldn't answer:

"Are you building an agency or a high-paying job with employees?"

The difference is delegation. Real delegation. Not "do this task" delegation, but "own this outcome" delegation.

This meant accepting that others would do things differently than I would. Sometimes worse. Sometimes better. Always differently.

It meant letting small mistakes happen so people could learn, instead of preventing every error through micromanagement.

It meant measuring results, not methods.

The first time a client meeting happened without me was terrifying. The first time a campaign launched without my review felt wrong. The first time I took a week off and nothing broke felt like a miracle.

That's when I realized I wasn't the asset anymore. The team was.

Scaling an agency requires one core skill that nobody teaches:

Learning to let go of the very things that made you successful.

Your ability to do great work got you here. Your ability to build others who do great work gets you there.

What are you still holding onto that you need to release?""",
            "key_takeaways": [
                "Founder skills can become founder limitations",
                "True delegation means transferring ownership, not just tasks",
                "Micromanagement prevents team development",
                "Scale requires building capability in others"
            ],
            "hashtags": []
        }
    }
]


def main():
    """Create and upload all LinkedIn posts to Notion."""
    print("=" * 60)
    print("LinkedIn Posts Upload to Notion - Batch 2")
    print("=" * 60)

    # Initialize Notion agent
    notion_agent = NotionAgent()

    if not notion_agent.notion_client:
        print("ERROR: Notion client not initialized. Check your NOTION_API_KEY.")
        return

    if not notion_agent.database_id:
        print("ERROR: No NOTION_DATABASE_ID configured.")
        return

    print(f"\nUploading {len(LINKEDIN_POSTS)} posts to Notion...\n")

    results = []

    for i, post_data in enumerate(LINKEDIN_POSTS, 1):
        title = post_data["idea"]["title"]
        print(f"[{i}/5] Uploading: {title}")

        result = notion_agent.execute(
            content_type="post",
            idea=post_data["idea"],
            content=post_data["post"]
        )

        if result["success"]:
            print(f"       SUCCESS - Page ID: {result['page_id']}")
            print(f"       URL: {result['page_url']}")
            results.append({
                "title": title,
                "success": True,
                "page_id": result["page_id"],
                "url": result["page_url"]
            })
        else:
            print(f"       FAILED - {result.get('error', 'Unknown error')}")
            results.append({
                "title": title,
                "success": False,
                "error": result.get("error")
            })

        print()

    # Summary
    print("=" * 60)
    print("UPLOAD SUMMARY")
    print("=" * 60)

    successful = sum(1 for r in results if r["success"])
    print(f"\nTotal posts: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")

    if successful > 0:
        print("\nUploaded posts:")
        for r in results:
            if r["success"]:
                print(f"  - {r['title']}")
                print(f"    {r['url']}")

    print("\nDone!")


if __name__ == "__main__":
    main()
