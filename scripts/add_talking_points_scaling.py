#!/usr/bin/env python3
"""
Add talking points with images to the existing Scaling video page.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.notion_agent import NotionAgent
from agents.image_agent import ImageAgent

# The concise scaling script
SCALING_SCRIPT = {
    "title": "The Brutal Truth About Scaling to $1M: What Nobody Tells You About the 7-Figure Transition",
    "estimated_length_minutes": 22,
    "hook": {
        "duration_seconds": 15,
        "script": "Getting to $500K in agency revenue is hard. But the transition from $500K to $1M is exponentially harder. Most agencies plateau between $500K and $750K forever. I almost became one of those statistics. Here's what I learned scaling to just over $1M in our best year."
    },
    "early_cta": {
        "duration_seconds": 8,
        "script": "If you're an agency owner trying to scale to seven figures, subscribe now. I break down operational and financial realities of scaling agencies every week. Let's get into this."
    },
    "intro": {
        "duration_seconds": 35,
        "script": "I'm Jordan. My agency has done just over $1M in our best year. But a couple years ago, we were stuck at $550K. I was working 70-hour weeks, personally managing accounts, watching profit margins shrink. I thought I was doing everything right. Today I'm sharing the uncomfortable truths about scaling to $1M. We're covering the leadership paradox, when to fire yourself from delivery, team restructuring, margin compression, and the three financial decisions that determine if you break through."
    },
    "main_sections": [
        {
            "section_title": "The Leadership Paradox",
            "duration_minutes": 2.5,
            "script": "At $500K, I realized I was the bottleneck. All the skills that got me there were preventing me from scaling. Being a great operator is your superpower early on. You're close to clients, you understand the work, you can save projects. But at $500K, this becomes your prison. I was still lead strategist on top accounts. I was reviewing every piece of creative. I was on every important call. I was operationally excellent but strategically bankrupt. The transition to $1M isn't about doing more of what works. It's about becoming a different type of leader. You shift from operator to architect. From doer to designer of systems. I resisted this for eight months. We stayed flat at $550K while I burned out. The paradox: you have to let go of being the best operator to become the CEO your business needs."
        },
        {
            "section_title": "When to Fire Yourself from Delivery",
            "duration_minutes": 3,
            "script": "When do you fire yourself from client delivery? Probably six months before you think you should. My breaking point: I calculated my effective hourly rate. At $550K revenue, working 60-hour weeks on client work, I was paying myself less than my senior account managers. I was the most expensive delivery person in my agency. Fire yourself when your time doing work prevents you from building systems that scale the work. This happens around $400K-$500K. At that point, spend 70% of your time on: building processes, recruiting leaders, and strategic business development. My 90-day transition: Month one, document everything. Month two, train and shadow. Month three, full handoff with weekly check-ins. Within six months of removing myself from delivery, revenue jumped from $550K to $800K. I was finally working on growth instead of fulfillment."
        },
        {
            "section_title": "The Team Restructure",
            "duration_minutes": 3,
            "script": "Hard truth: the team that got you to $500K probably isn't the team that gets you to $1M. At $500K, we had five generalists. Everyone wore multiple hats. It was scrappy and flexible until it wasn't. You can't systematize chaos. You can't create repeatable processes when everyone's role is fluid. We moved from generalist to specialized pod structure. Each pod had clear roles: client lead, project manager, and specialists. Some high performers in the generalist model didn't fit the specialized model. I had difficult conversations. One person left voluntarily. Another I had to transition out. It felt like betrayal. But loyalty to people can't come at the expense of the business. We also hired differently. At sub-$500K, I hired for hustle. At $500K+, I hired for specialized expertise. Average salary jumped from $45K to $58K. We added an $85K director role. Within six months, they built systems that let us take 40% more clients without adding delivery staff."
        },
        {
            "section_title": "Margin Compression",
            "duration_minutes": 2.5,
            "script": "This almost made me quit: margin compression. At $500K, we ran 28% net margin. That's $140K profit. At $700K, eighteen months later, we were at 19% margin. That's $133K profit. We grew revenue 40% and made less money. I was furious. But margin compression during the $500K to $1M phase is normal. It's the cost of building infrastructure to scale. Where the money went: team costs jumped from 42% to 51% of revenue. Systems and tools added $15K. Training added $10K. Plus opportunity cost from being less efficient during transition. You have to sacrifice short-term profitability for long-term scalability. At $1M, we're back to 26% margin. That's $260K profit, nearly double what we made at $500K. Plan for this. Keep six months of operating expenses in reserve before scaling aggressively."
        },
        {
            "section_title": "Decision 1: Reinvest vs Extract",
            "duration_minutes": 2,
            "script": "Three financial decisions determine if you break through. First: reinvest profits or extract them? At $500K, you're finally making money. Temptation is to upgrade your lifestyle. Agencies that break through reinvest 60-70% of profits during transition. Agencies that plateau extract most profits. I kept my salary flat at $80K for 18 months and reinvested about $80K back into hiring, systems, and growth. That funded our leadership hire, new project management system, and first real marketing budget. Without it, we'd still be at $500K."
        },
        {
            "section_title": "Decision 2: Specialize vs Diversify",
            "duration_minutes": 2,
            "script": "Second decision: diversify services or go deeper in one? At $500K, clients want you to do everything. SEO, paid ads, email, social, web design. Temptation is to say yes because it's revenue. This is a trap. We said no to 60% of service requests and doubled down on paid acquisition and conversion optimization. We turned away SEO, social media management, and branding. Probably said no to $100K in revenue that year. But by specializing, we could systematize delivery, become known for one thing, charge premium rates, and scale without proportional headcount. We went from 12 clients across six services to 18 clients in two services. Tighter delivery, better margins, stronger reputation."
        },
        {
            "section_title": "Decision 3: Personal Brand vs Hiding",
            "duration_minutes": 2,
            "script": "Third decision: build a personal brand or hide behind the agency? At $500K, you're comfortable behind the scenes. But to break through, someone needs to be the face of the business. I resisted. I didn't want to post on LinkedIn or do videos. Then I calculated our CAC. At $500K, we spent $5K to acquire a client through paid ads. Average lifetime value was $24K. Decent but not great. I started posting content three times a week on LinkedIn. Within six months, we got 2-3 inbound leads monthly from my content. These closed at 45% versus 18% from paid channels. CAC was essentially zero. Over 12 months, my personal brand generated $200K in revenue at basically no cost. That's the difference between plateau and growth."
        },
        {
            "section_title": "The Identity Shift",
            "duration_minutes": 2.5,
            "script": "The hardest part: identity shift. For years, my identity was tied to doing great work. I was the strategist who saved campaigns. The one clients asked for by name. Becoming a CEO meant letting go of that. The CEO role at this phase isn't big strategic decisions. It's building systems, recruiting, difficult conversations, spreadsheets, cash flow forecasting, one-on-ones, documenting processes. For six months, I hated it. I felt disconnected from work I loved. But my value was no longer in doing the work. My value was in building the machine that does the work. I created a new scorecard: processes documented, leadership meetings held, strategic decisions made, hours on business development versus delivery. The breakthrough: my team didn't need me to be the best operator. They needed me to be the clearest leader. Vision, direction, support, resources. That's the CEO job."
        },
        {
            "section_title": "Fewer Clients, Higher Value",
            "duration_minutes": 2,
            "script": "Counterintuitive truth: to scale from $500K to $1M, you need fewer clients, not more. At $500K, we had 20 clients averaging $25K annually. Constant sales pressure, lots of small accounts, high complexity. At $1M, we have 15 clients averaging $65K. Fewer clients, less chaos, higher profitability. Small clients are operationally expensive. Same onboarding, reporting, and communication as large clients, but fraction of the revenue. They churn faster and are more price-sensitive. We raised minimums from $2K to $5K monthly. Lost 30% of clients, the bottom tier. Filled the gap with higher-value clients. Changed our ideal customer from solopreneurs to established companies with $2M-$20M revenue. Clients who value expertise, pay on time, and stick around for years."
        }
    ],
    "call_to_action": {
        "duration_seconds": 30,
        "script": "If you made it this far, you're serious about scaling. Assess where you are honestly. Are you still the operator or have you transitioned to CEO? Are you reinvesting or extracting profits? Are you specializing or trying to do everything? If you're between $400K and $750K, I've created a free 7-Figure Scale Audit. It tells you exactly where your bottlenecks are. Link in description. Drop a comment with where you're at in your journey. I read every comment. Thanks for watching."
    }
}


def main():
    print("=" * 60)
    print("ADDING TALKING POINTS TO SCALING VIDEO")
    print("=" * 60)

    notion_agent = NotionAgent()
    image_agent = ImageAgent()

    if not image_agent.client:
        print("Error: REPLICATE_API_TOKEN not found")
        return

    # Search for existing page
    print("\n[1/3] Searching for existing Notion page...")
    page = notion_agent.search_page_by_title("Brutal Truth About Scaling")

    if page:
        page_id = page["page_id"]
        print(f"  Found page: {page['title']}")
        print(f"  URL: {page['url']}")
    else:
        print("  Page not found. Creating new one...")
        idea = {
            "title": SCALING_SCRIPT["title"],
            "hook": SCALING_SCRIPT["hook"]["script"],
            "key_points": [s["section_title"] for s in SCALING_SCRIPT["main_sections"]]
        }
        page_id = notion_agent.create_video_entry(idea, SCALING_SCRIPT)
        if not page_id:
            print("  Error creating page")
            return
        print(f"  Created: https://notion.so/{page_id.replace('-', '')}")

    # Generate images
    print(f"\n[2/3] Generating AI images ({len(SCALING_SCRIPT['main_sections']) + 1} images)...")
    print("  This will take about 2 minutes due to rate limiting...")

    images = image_agent.generate_section_images(
        SCALING_SCRIPT,
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
        script=SCALING_SCRIPT,
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
