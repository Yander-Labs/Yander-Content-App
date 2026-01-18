#!/usr/bin/env python3
"""
Script to create and upload batch 3 of LinkedIn posts - background/origin stories.
Following content guidelines: no client bashing, no negative hiring stories, no emojis, no hashtags.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.notion_agent import NotionAgent

# 5 Long-form LinkedIn posts - Background and Growth Stories
LINKEDIN_POSTS = [
    {
        "idea": {
            "title": "The Moment I Knew I Had to Build Something Different"
        },
        "post": {
            "hook": "I was sitting in my car after losing a client I'd worked 80-hour weeks to keep. That's when I realized I wasn't building a business. I was building my own cage.",
            "full_post": """I was sitting in my car after losing a client I'd worked 80-hour weeks to keep.

That's when I realized I wasn't building a business. I was building my own cage.

I started my agency the way most people do. I was good at marketing, needed income, and figured I could figure out the business part later.

For the first two years, I was the salesperson, the strategist, the account manager, the bookkeeper, and the janitor. I wore every hat because I thought that's what "hustle" meant.

My revenue grew. My calendar filled up. But something was broken.

I'd land a client, deliver great work, and still lose them six months later. I'd hire someone, train them for weeks, and watch them leave. Every win felt temporary.

That night in my car, I asked myself a question I'd been avoiding:

"Am I building an agency or just buying myself a demanding job?"

The honest answer changed everything.

I stopped optimizing for revenue and started optimizing for sustainability. I built systems instead of heroics. I hired for culture fit, not just skill. I said no to clients who needed a vendor instead of a partner.

It took another two years to rebuild the right way.

But that rebuild took the agency from barely $500K to over $2.8M in revenue. More importantly, it gave me my life back.

The turning point wasn't a strategy or a tactic.

It was admitting that the way I was doing things wasn't working, even though the numbers looked fine on paper.

If you're grinding right now and wondering why success still feels like a trap, maybe the problem isn't working harder.

Maybe it's time to rebuild.

What's one thing in your business you know isn't working but haven't addressed yet?""",
            "key_takeaways": [
                "Revenue growth doesn't equal business health",
                "Hustle without systems leads to burnout",
                "Sometimes you need to rebuild, not just optimize",
                "Sustainable growth requires honest self-assessment"
            ],
            "hashtags": []
        }
    },
    {
        "idea": {
            "title": "From $500K to $2.8M: What Actually Changed"
        },
        "post": {
            "hook": "People ask me what changed to grow my agency from $500K to $2.8M. They expect a marketing secret or sales hack. The real answer disappoints them.",
            "full_post": """People ask me what changed to grow my agency from $500K to $2.8M.

They expect a marketing secret or sales hack.

The real answer disappoints them.

I stopped doing the things I was good at.

At $500K, I was the best marketer in my agency. The best salesperson. The best client manager. That was the problem.

Every hour I spent doing those things was an hour I couldn't spend building the machine that would do them without me.

Here's the unsexy truth about what actually changed:

I documented everything I did. Every process. Every decision framework. Every client communication template. It took months and felt like it was slowing me down.

I hired people to replace me in roles, not just assist me. There's a difference. Assistants need you. Replacements free you.

I stopped saying yes to every opportunity. We turned away clients who weren't right fits. We raised prices and lost some people. We got specific about who we served best.

I invested in infrastructure before we needed it. CRM systems. Project management. Financial tracking. It felt premature at $500K. It was essential by $1.5M.

I spent more time thinking than doing. Calendar blocks for strategy. No meetings on certain days. Time to actually lead instead of just produce.

None of this is exciting.

There's no viral growth hack in documenting your client onboarding process. No dopamine hit from building a training system for new hires.

But that boring work is the difference between an agency that depends on you and an agency that grows beyond you.

The $500K version of my agency needed me every day.

The $2.8M version runs when I'm not there.

That's not a marketing win. It's an operations win.

What boring work have you been avoiding that could unlock your next level of growth?""",
            "key_takeaways": [
                "Growth often requires doing less of what you're good at",
                "Documentation and systems beat talent and hustle",
                "Saying no creates space for better opportunities",
                "Operations wins compound more than marketing wins"
            ],
            "hashtags": []
        }
    },
    {
        "idea": {
            "title": "Why I Started Building Software After Running an Agency"
        },
        "post": {
            "hook": "After scaling my agency to $2.8M, I started building software to solve a problem that almost cost me everything: I had no idea what was really happening with my remote team.",
            "full_post": """After scaling my agency to $2.8M, I started building software to solve a problem that almost cost me everything.

I had no idea what was really happening with my remote team.

We were fully remote. On paper, things looked great. Projects delivered. Clients happy. Revenue growing.

Then three things happened in the same month:

My best account manager resigned. Said she'd been overwhelmed for months. I had no idea.

A key client churned. Turns out there had been communication issues for weeks. Nobody told me until it was too late.

Two team members were quietly job hunting. I found out from LinkedIn notifications.

I wasn't a bad leader. I just had no visibility.

The tools we used showed me activity, not reality. Screenshots and time tracking told me people were working. They didn't tell me if someone was drowning, disengaging, or about to walk out the door.

I started obsessing over a question:

How do I see problems before they become crises without turning into a surveillance manager?

That obsession became a product. Software that integrates with the tools teams already use and surfaces behavioral signals, not screenshots. Workload patterns, not keystrokes. Early warnings, not invasive monitoring.

Because here's what I learned running my agency:

The information that matters most is the information people don't tell you.

Not because they're hiding it. Because they don't think it's important, or they're too busy, or they assume you already know.

Leaders need signal, not surveillance.

If you manage a remote team, you've probably felt this gap. You know something's off, but you can't quite see it until it's too late.

That's the problem I'm trying to solve.

What's the last team issue you wish you'd seen coming earlier?""",
            "key_takeaways": [
                "Activity metrics don't reveal team health",
                "Problems often surface too late in remote teams",
                "Leaders need behavioral signals, not surveillance",
                "The most important information is what people don't tell you"
            ],
            "hashtags": []
        }
    },
    {
        "idea": {
            "title": "The Question That Changed How I Lead"
        },
        "post": {
            "hook": "Early in my agency, I asked my team: 'Does anyone need anything?' Nobody spoke up. Two weeks later, someone quit. I was asking the wrong question.",
            "full_post": """Early in my agency, I asked my team: "Does anyone need anything?"

Nobody spoke up.

Two weeks later, someone quit.

I was asking the wrong question.

"Does anyone need anything?" puts the burden on your team. They have to self-diagnose their problem, decide it's worth mentioning, and feel comfortable speaking up in a group setting.

That's three barriers before you hear anything useful.

I changed my approach after that wake-up call.

Instead of open-ended group questions, I started asking specific, individual questions:

"What's one thing on your plate right now that's taking longer than it should?"

"If you could change one thing about how we work, what would it be?"

"What's something you've been dealing with that I probably don't know about?"

These questions do three things differently:

They're specific enough to prompt real answers, not just "I'm good."

They assume there IS something, making it safer to share.

They signal that you actually want to know the truth.

But questions alone weren't enough.

I also had to change when and how I asked. One-on-ones instead of team meetings. Async check-ins for people who process better in writing. Creating space where honesty felt safe.

The shift wasn't dramatic or instant.

But over time, I started hearing things earlier. Small frustrations before they became resignations. Workload issues before burnout. Concerns about clients before they churned.

Leadership isn't about having the answers.

It's about asking questions that surface the truth before it's too late.

What question do you wish someone had asked you earlier in your career?""",
            "key_takeaways": [
                "Open-ended questions often get empty answers",
                "Specific questions make honesty easier",
                "How you ask matters as much as what you ask",
                "Early signals require intentional discovery"
            ],
            "hashtags": []
        }
    },
    {
        "idea": {
            "title": "What Nobody Told Me Before I Started My Agency"
        },
        "post": {
            "hook": "When I started my agency, everyone gave me advice about getting clients. Nobody warned me about what happens after you get them.",
            "full_post": """When I started my agency, everyone gave me advice about getting clients.

Nobody warned me about what happens after you get them.

The first year of my agency, I was great at sales. I could close. I could pitch. I could promise the moon and deliver good work.

What I couldn't do was keep clients happy while doing that good work. Manage a team while selling and delivering. Build systems while fighting fires daily.

Here's what I wish someone had told me:

Client acquisition is a skill. Client retention is a system. You can hustle your way to new clients. You can't hustle your way to keeping them.

The work you do is less important than how the client feels about the work. I delivered great results for clients who still left. I delivered mediocre results for clients who stayed for years. The difference was communication, not performance.

Your first hires will probably be wrong. Not because they're bad people, but because you don't know how to hire yet. Budget for learning this lesson, because you will pay for it.

Revenue is vanity. Profit is sanity. Cash flow is reality. I had months where revenue looked amazing and I couldn't make payroll. Understanding the difference between these three numbers is survival.

The hardest part isn't any single skill. It's doing many skills at 70% while you build toward not needing to do them at all.

I made every mistake in the book. Hired wrong, priced wrong, promised wrong, prioritized wrong.

But each mistake taught me something I couldn't have learned any other way.

If you're in year one or two of your agency, it's supposed to be hard. The chaos isn't a sign you're failing. It's the tuition for the education you're getting.

Keep going.

What's something you wish someone had told you before you started your business?""",
            "key_takeaways": [
                "Client retention requires systems, not just hustle",
                "How clients feel matters more than results delivered",
                "Early hiring mistakes are part of the learning curve",
                "Understand the difference between revenue, profit, and cash flow"
            ],
            "hashtags": []
        }
    }
]


def main():
    """Create and upload all LinkedIn posts to Notion."""
    print("=" * 60)
    print("LinkedIn Posts Upload to Notion - Batch 3 (Background/Origin)")
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
