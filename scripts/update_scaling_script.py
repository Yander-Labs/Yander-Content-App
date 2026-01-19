#!/usr/bin/env python3
"""
Script to update the scaling video content with corrected revenue figures.
Changes from $1M-$2M narrative to $500K-$1M narrative.
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.notion_agent import NotionAgent

# Updated script with corrected figures
UPDATED_SCRIPT = {
    "title": "The Brutal Truth About Scaling to $1M: What Nobody Tells You About the 7-Figure Transition",
    "estimated_length_minutes": 28,
    "hook": {
        "duration_seconds": 20,
        "script": "Getting to $500K in agency revenue is hard. I'll be honest—it took me years of grinding. But here's what actually broke me: the transition from $500K to $1M is exponentially harder. And most agencies never make it. In fact, a huge percentage of agencies plateau between $500K and $750K and stay there forever. I almost became one of those statistics. Here's why this transition nearly destroyed my business—and what I learned that took us from $500K to just over $1M in our best year."
    },
    "early_cta": {
        "duration_seconds": 10,
        "script": "Real quick—if you're an agency owner trying to scale to seven figures, hit that subscribe button right now. I break down the operational and financial realities of scaling agencies every week, and you'll want to catch the next one. Now, let's get into this."
    },
    "intro": {
        "duration_seconds": 45,
        "script": "I'm Jordan, and I run a marketing agency that's done just over $1M in our best year. But a couple years ago, we were stuck at around $550K, and I was working 70-hour weeks, personally managing client accounts, and watching our profit margins shrink every quarter. I thought I was doing everything right. I had clients, I had revenue, I had a team. But I was trapped. Today, I'm going to share the brutal, uncomfortable truths about scaling to $1M that nobody talks about. We're covering the leadership paradox that keeps you stuck, the exact moment you need to fire yourself from delivery, the team restructure that feels like starting over, why your margins will compress before they expand, and the three financial decisions that literally determine if you break through or plateau forever. This isn't theory—this is what actually happened, with real numbers and real consequences."
    },
    "main_sections": [
        {
            "section_title": "The Leadership Paradox: Why What Got You Here Keeps You Stuck",
            "duration_minutes": 3.5,
            "script": "Let's start with the most painful realization I had at $500K: I was the bottleneck. And here's the paradox—all the skills that got me to $500K were the exact things preventing me from getting to $1M. At the sub-$500K stage, being a great operator is your superpower. You're close to clients, you understand the work deeply, you can jump in and save projects, you're the best salesperson because you know the service inside and out. This is what gets you to mid-six figures. But at $500K, this becomes your prison. I was still the lead strategist on our top three accounts. I was reviewing every piece of creative. I was on sales calls, onboarding calls, and crisis calls. I was operationally excellent—and strategically bankrupt. Here's what nobody tells you: the transition from $500K to $1M isn't about doing more of what works. It's about becoming a completely different type of leader. You have to shift from operator to architect. From doer to designer of systems. From being in the business to working on the business. And this shift is terrifying because it feels like you're abandoning the very things that made you successful. I resisted this for eight months. And in those eight months, we stayed flat at around $550K while I burned out. The leadership paradox is this: you have to let go of being the best operator to become the CEO your business needs. And that means accepting that others will do the work differently than you—and that's okay.",
            "visual_notes": "Show comparison graphic: 'Skills That Got You to $500K' vs 'Skills Needed for $1M' - on-screen text highlighting the paradox"
        },
        {
            "section_title": "When to Fire Yourself from Delivery (The $500K Threshold)",
            "duration_minutes": 4,
            "script": "So when exactly do you fire yourself from client delivery? Here's the uncomfortable answer: probably six months before you think you should. For me, the breaking point came when I calculated my effective hourly rate. I was making $550K in revenue, but I was personally working 60-hour weeks on client work. When I divided my salary by my actual hours worked, I was paying myself less than I was paying my senior account managers. I was the most expensive delivery person in my agency. Here's the framework I wish I'd had: You should fire yourself from delivery when your time doing the work prevents you from building the systems that would scale the work. Practically, this happens around $400K to $500K for most agencies. At this point, you should be spending 70% of your time on three things: one, building and optimizing processes so your team can deliver without you; two, recruiting and developing leaders who can run departments; and three, strategic business development—not just sales calls, but partnerships, positioning, and product development. Here's how I actually did it. First, I made a list of every client-facing responsibility I had. Then I rated each one: What only I can do versus what others can learn. The 'only I can do' list was way shorter than I thought. It was basically strategic positioning and key client relationships. Everything else—campaign execution, creative review, reporting, even most strategy—could be systematized and delegated. Then I created a 90-day transition plan. Month one: Document everything. I recorded my process for every major task. Month two: Train and shadow. I had team members shadow me, then I shadowed them. Month three: Full handoff with weekly check-ins. The hardest part? Watching someone do it differently than I would. Not wrong—just different. I had to bite my tongue a hundred times. But here's what happened: within six months of removing myself from delivery, our revenue jumped from $550K to $800K. Why? Because I was finally working on growth instead of just fulfillment.",
            "visual_notes": "Show the 90-day transition timeline as an animated graphic; display the revenue jump chart showing $550K to $800K"
        },
        {
            "section_title": "The Team Restructure: Why It Feels Like Starting Over",
            "duration_minutes": 4.5,
            "script": "Here's a harsh truth: the team that got you to $500K is probably not the team that gets you to $1M. And restructuring feels like you're blowing up everything you built. At $500K, we had five people. Everyone wore multiple hats. We had account managers who also did some project management and some strategy. We had designers who also did client communication. It was scrappy, flexible, and it worked—until it didn't. The problem with a generalist team at scale is that you can't systematize chaos. You can't create repeatable processes when everyone's role is fluid. And you definitely can't scale when every team member is a single point of failure. Here's the restructure we had to do, and why it was painful. We moved from a generalist model to a specialized pod structure. Each pod had clear roles: a client lead who owns relationships and strategy, a project manager who owns delivery and timelines, and specialists who own execution in their domain. This meant some people who were high performers in the generalist model didn't fit in the specialized model. I had to have some very difficult conversations. One person left voluntarily because they didn't want to specialize. Another person I had to transition out because they couldn't operate at the level required for their new specialized role. These were people who helped build the agency. It felt like betrayal. But here's what I learned: loyalty to people can't come at the expense of the business. And honestly, keeping them in roles they weren't suited for wasn't fair to them either. The restructure also meant hiring differently. At sub-$500K, I hired for hustle and attitude. At $500K+, I had to hire for specialized expertise and experience. This meant higher salaries. Our average team member salary jumped from $45K to $58K. That hurt in the short term. We also added a director-level role at $85K—our first true leadership hire. I'll be honest, I resented that salary for the first three months. It felt like a luxury we couldn't afford. But within six months, they built the operational systems that allowed us to take on 40% more clients without adding more delivery staff. The restructure took about nine months fully. And during those nine months, it felt like we were moving backward. Some clients noticed the transitions. We had a few bumpy handoffs. But on the other side, we had a team that could actually scale. Here's my advice: start the restructure at $400K, not at $600K when you're already drowning. And be honest with your team about what's happening and why.",
            "visual_notes": "Show before/after org charts - 'Generalist Model at $500K' vs 'Specialized Pod Structure at $750K+'; display salary comparison graphics"
        },
        {
            "section_title": "Margin Compression: The Profitability Paradox",
            "duration_minutes": 3.5,
            "script": "Let's talk about something that almost made me quit: margin compression. Here's what happened to our profitability during the scale from $500K to $1M. At $500K in revenue, we were running at about 28% net profit margin. That's $140K in profit. Healthy. At $700K, about eighteen months later, we were at 19% net margin. That's $133K in profit. We grew revenue by 40% and made less money. I was furious. I thought we were doing something wrong. But here's the brutal truth: margin compression during the $500K to $1M phase is normal. It's the cost of building the infrastructure to scale. Let me break down where the money went. First, team restructure costs. We hired more expensive specialists and added leadership. Our team costs went from 42% of revenue to 51% of revenue. Second, systems and tools. We invested in a real project management system, a CRM, automation tools, and better reporting infrastructure. This added about $15K annually. Third, training and development. We brought in consultants, paid for courses, and invested in leadership coaching. Another $10K. Fourth, the biggest one—opportunity cost. During the transition, we were less efficient. Projects took longer. Some clients churned during team transitions. We had to turn down new business because we were at capacity while restructuring. Here's what nobody tells you: you have to be willing to sacrifice short-term profitability for long-term scalability. I had to make peace with making less money for about 12 to 18 months while we built the foundation. But here's the payoff: Once the systems were in place and the team was fully trained, our margins started expanding again. At $1M, we're at 26% net margin. That's $260K in profit—nearly double what we made at $500K. The key is knowing this is coming and planning for it. I wish I'd kept six months of operating expenses in reserve before starting the transition. I didn't, and there were some scary months where I wasn't sure we'd make payroll. Don't make that mistake.",
            "visual_notes": "Show profitability graph over time - the 'valley' of margin compression; display expense breakdown pie charts at different revenue stages"
        },
        {
            "section_title": "The 3 Financial Decisions That Determine If You Break Through",
            "duration_minutes": 5,
            "script": "Okay, this is the most important section. There are three major financial decisions you'll face between $500K and $1M. How you handle these literally determines if you plateau or break through. Decision number one: Do you reinvest profits or extract them? At $500K, you're finally making decent money. The temptation is to pay yourself a bigger salary, upgrade your lifestyle, maybe buy that car you've been wanting. I get it. I almost did this. But here's what I learned: agencies that break through to $1M+ reinvest 60-70% of profits back into the business during the transition phase. Agencies that plateau extract most of their profits. I made a deal with myself: for 18 months, I would keep my salary flat at $80K—which was comfortable but not extravagant—and reinvest everything else. That meant about $80K went back into hiring, systems, and growth initiatives. This was hard. I watched other agency owners buying Teslas and taking luxury vacations while I was flying economy and driving my paid-off Honda. But that reinvestment is what funded our leadership hire, our new project management system, and our first real marketing budget. Without it, we'd still be at $500K. Decision number two: Do you diversify services or go deeper in one? At $500K, you're getting requests for all kinds of adjacent services. SEO, paid ads, email, social, web design—clients want you to do everything. The temptation is to say yes to all of it because it's revenue. This is a trap. Here's what we did: we said no to 60% of service requests and doubled down on the 40% that represented our highest margin, most scalable offering. For us, that was paid acquisition and conversion optimization. We turned away SEO projects, social media management, and branding work. In the short term, this felt like leaving money on the table. We probably said no to $100K in revenue that year. But by specializing, we could systematize our delivery, become known for one thing, charge premium rates, and scale without adding proportional headcount. This decision took us from 12 clients across six service lines to 18 clients in two service lines. Our delivery got tighter, our margins improved, and our reputation strengthened. Decision number three: Do you build a personal brand or hide behind the agency? This one's controversial. At $500K, you're comfortable staying behind the scenes. The agency has a reputation, you've got referrals, you don't need to be visible. But to break through to $1M+, someone needs to be the face of the business. For most agencies, that's the founder. I resisted this hard. I didn't want to post on LinkedIn, I didn't want to do videos, I didn't want to put myself out there. But here's what changed my mind: I calculated our customer acquisition cost. At $500K, we were spending $5K to acquire a client through paid ads and outbound. Our average client lifetime value was $24K. That's a decent return—acceptable but not great. Then I started posting content three times a week on LinkedIn. Within six months, we were getting two to three inbound leads per month from my personal content. These leads closed at 45% versus 18% from paid channels. And the CAC was essentially zero except for my time. Over 12 months, my personal brand generated about $200K in new revenue at basically no cost. That's the difference between plateau and growth. These three decisions—reinvest versus extract, specialize versus diversify, personal brand versus hiding—are the ones that determined our trajectory. Get them right and you break through. Get them wrong and you plateau.",
            "visual_notes": "Show the 3 decisions as bold on-screen graphics; display ROI comparison between paid acquisition vs personal brand leads; show revenue attribution from each decision"
        },
        {
            "section_title": "From Operator to CEO: The Identity Shift",
            "duration_minutes": 3.5,
            "script": "Let's talk about the hardest part of this entire transition: the identity shift. For the first few years of my agency, I was an operator. My identity was tied to doing great work. I was the strategist who saved campaigns. I was the one clients asked for by name. I was really good at the work. Becoming a CEO meant letting go of that identity. And that was terrifying. Here's what the CEO role actually looks like at the $500K to $1M phase—and it's not what you think. You're not sitting in a corner office making big strategic decisions. You're building systems. You're recruiting. You're having difficult conversations. You're looking at spreadsheets and forecasting cash flow. You're in weekly one-on-ones with your leadership team. You're documenting processes. Honestly, for the first six months, I hated it. I felt disconnected from the work I loved. I felt like I wasn't adding value. I missed the dopamine hit of launching a great campaign. But here's what I had to accept: my value was no longer in doing the work. My value was in building the machine that does the work. This required a complete mindset shift. I had to stop measuring my day by tasks completed and start measuring it by systems built. I had to stop getting validation from client wins and start getting it from team development. I had to stop being the hero and start being the architect. Practically, here's how I made this shift. I created a new scorecard for myself with different metrics. Instead of campaigns launched, I tracked: number of processes documented, leadership team meetings held, strategic decisions made, and hours spent on business development versus delivery. I also got a business coach. This was a $10K investment that felt insane at the time. But they helped me navigate the identity crisis and held me accountable to staying in my CEO role instead of slipping back into operator mode. The biggest breakthrough came when I realized that my team didn't need me to be the best operator. They needed me to be the clearest leader. They needed vision, direction, support, and resources. That's the CEO job. If you're in this transition right now, give yourself grace. It takes 12 to 18 months to fully make this shift. You'll slip back into operator mode. You'll second-guess yourself. You'll wonder if you're still valuable. That's all normal. Just keep focusing on building the systems and developing the leaders. That's how you scale.",
            "visual_notes": "Show comparison: 'Operator Scorecard' vs 'CEO Scorecard'; display the identity shift journey as a visual timeline"
        },
        {
            "section_title": "The Client Mix Shift: Fewer Clients, Higher Value",
            "duration_minutes": 2.5,
            "script": "Here's a counterintuitive truth: to scale from $500K to $1M, you probably need fewer clients, not more. At $500K, we had 20 active clients. Average client value was about $25K annually. This meant constant sales pressure, lots of small accounts, and high operational complexity. At $1M, we have about 15 clients. Average client value is $65K annually. We have fewer clients, less chaos, and higher profitability. Here's why this shift matters. Small clients are operationally expensive. They require the same onboarding, reporting, and communication as large clients, but generate a fraction of the revenue. They also churn faster and are more price-sensitive. The shift from many small clients to fewer large clients requires two things. First, you need to increase your prices significantly. We went from $2K monthly retainers to $5K minimum. This scared me. I thought we'd lose everyone. We lost about 30% of clients—the bottom tier who were never going to scale with us anyway. But the remaining 70% stayed, and we filled the gap with higher-value clients. Second, you need to change your ideal customer profile. We stopped targeting solopreneurs and tiny startups. We started targeting established companies with $2M to $20M in revenue who had real marketing budgets. This meant different marketing, different sales conversations, and different service delivery. But it also meant clients who valued our expertise, paid on time, and stuck around for years instead of months. The client mix shift is uncomfortable because it feels like you're shrinking your potential market. But you're actually focusing on the market that can afford to pay what you're worth. This is how you scale profitably.",
            "visual_notes": "Show client portfolio comparison: '20 clients at $500K' vs '15 clients at $1M' with average values; display the ideal customer profile shift"
        },
        {
            "section_title": "Real Financial Breakdown: Where the Money Goes",
            "duration_minutes": 3,
            "script": "Let's get into the actual numbers. I'm going to show you exactly where the money goes at different revenue stages, because understanding this is critical for planning your transition. At $500K in revenue, here's how our finances broke down. Team costs: $210K or 42%. This included four full-time employees and one contractor. Tools and software: $14K or 2.8%. We were pretty lean here. Office and overhead: $18K or 3.6%. We had a small office space. Marketing and sales: $12K or 2.4%. Mostly just paid ads. Owner salary: $60K or 12%. My take-home. Net profit: $140K or 28%. This went into savings and some reinvestment. At $750K, during the transition phase, here's how it changed. Team costs: $382K or 51%. We added specialists and a director. Tools and software: $26K or 3.5%. We upgraded to better systems. Office and overhead: $24K or 3.2%. Training and development: $16K or 2.1%. This was new. Marketing and sales: $22K or 3%. We started investing in content. Owner salary: $60K or 8%. I kept this flat intentionally. Net profit: $142K or 19%. Lower margin, similar absolute profit. Notice the margin compression. Now at $1M, here's where we are. Team costs: $490K or 49%. More efficient with better systems. Tools and software: $32K or 3.2%. Marketing and sales: $44K or 4.4%. This drives our growth now. Training and development: $21K or 2.1%. Office and overhead: $29K or 2.9%. Owner salary: $90K or 9%. I finally gave myself a raise. Net profit: $260K or 26%. Back to healthy margins with nearly double the absolute profit from $500K. The key insight: during the transition, your costs increase before your revenue catches up. You need to plan for this. If I could do it over, I would have saved more cash before starting the transition. I'd recommend having at least six months of operating expenses in reserve before you start scaling aggressively. This gives you runway to make the investments without panicking.",
            "visual_notes": "Show detailed financial breakdown tables for each revenue stage; use animated graphics to show how percentages shift; highlight the margin compression and recovery"
        },
        {
            "section_title": "The Biggest Mindset Shift Required",
            "duration_minutes": 2.5,
            "script": "We've covered a lot of tactical and financial stuff, but let me end with the biggest mindset shift required to scale to seven figures. It's this: you have to stop thinking like a freelancer and start thinking like a business owner. What's the difference? A freelancer mindset says: I need to be involved in everything. My expertise is the product. If I'm not doing the work, we're not delivering value. Growth means working more hours. A business owner mindset says: My job is to build systems that deliver value without me. The team's expertise is the product. If I'm doing the work, I'm the bottleneck. Growth means building leverage. This shift sounds simple, but it's profound. It affects every decision you make. Freelancer mindset hires people to help them do more work. Business owner mindset hires people to replace them in the work. Freelancer mindset sees team members as assistants. Business owner mindset sees team members as the scalable asset. Freelancer mindset measures success by how busy they are. Business owner mindset measures success by how much the business runs without them. I'll be honest—I still struggle with this sometimes. There are days when I want to jump back into a campaign strategy because it's familiar and comfortable. But every time I do that, I'm stealing time from building the business. The mindset shift isn't a one-time thing. It's a daily practice of choosing to work on the business instead of in it. Of choosing to develop others instead of doing it yourself. Of choosing to build systems instead of being the system. This is what separates agencies that plateau at $500K from those that break through to $1M and beyond. If you can make this shift, everything else becomes possible."
        }
    ],
    "call_to_action": {
        "duration_seconds": 45,
        "script": "Alright, if you made it this far, you're serious about scaling. Here's what I want you to do next. First, assess where you are honestly. Are you still the operator, or have you transitioned to CEO? Are you reinvesting profits or extracting them? Are you specializing or trying to do everything? Second, if you're between $400K and $750K right now, I've created a free resource called the 7-Figure Scale Audit. It's a 15-minute assessment that'll tell you exactly where your bottlenecks are and what to focus on first. Link is in the description. Third, if you want to see how we actually built the systems that took us from $500K to $1M, I break down our entire operational playbook in next week's video. Hit subscribe so you don't miss it. And if this video helped you, drop a comment below with where you're at in your journey. Are you pre-$500K grinding to get there, or are you in the messy middle of the transition? I read every comment and I'll respond with specific advice for your situation. Thanks for watching, and I'll see you in the next one."
    },
    "notes": {
        "total_duration_estimate": "28 minutes (excluding intro/outro animations)",
        "b_roll_suggestions": [
            "Screenshots of financial dashboards and spreadsheets",
            "Org chart graphics showing team evolution",
            "Time-lapse of Jordan working at desk/in office",
            "Stock footage of team meetings and collaboration",
            "Screen recordings of project management tools",
            "Graphs and charts showing revenue growth",
            "Photos of the team at different stages of growth",
            "Jordan walking through office space",
            "Close-ups of writing/sketching strategy notes"
        ],
        "on_screen_text_suggestions": [
            "Most agencies plateau between $500K-$750K",
            "The Leadership Paradox: What got you here keeps you stuck",
            "Fire yourself from delivery at $400K-$500K",
            "90-Day Transition Plan",
            "Margin compression is NORMAL during scale",
            "3 Financial Decisions That Determine Your Success",
            "Reinvest 60-70% of profits during transition",
            "Specialize, don't diversify",
            "Personal brand = zero CAC leads",
            "Fewer clients, higher value",
            "At $500K: 20 clients averaging $25K",
            "At $1M: 15 clients averaging $65K",
            "Stop thinking like a freelancer, start thinking like a business owner"
        ]
    }
}


def main():
    print("=" * 60)
    print("UPDATING SCALING VIDEO SCRIPT")
    print("=" * 60)

    # Initialize Notion agent
    notion_agent = NotionAgent()

    # Search for existing page
    search_title = "Brutal Truth About Scaling Past $1M"
    print(f"\n[1/4] Searching for existing Notion page: '{search_title}'")

    existing_page = notion_agent.search_page_by_title(search_title)

    if existing_page:
        print(f"  Found page: {existing_page['title']}")
        print(f"  Page ID: {existing_page['page_id']}")

        # Archive the existing page
        print(f"\n[2/4] Archiving existing page...")
        archived = notion_agent.archive_page(existing_page['page_id'])
        if archived:
            print("  Page archived successfully")
        else:
            print("  Warning: Could not archive page")
    else:
        print("  No existing page found")

    # Save updated script locally
    print(f"\n[3/4] Saving updated script locally...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    script_path = f"output/scripts/script_scaling_updated_{timestamp}.json"

    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    with open(script_path, 'w', encoding='utf-8') as f:
        json.dump(UPDATED_SCRIPT, f, indent=2)
    print(f"  Saved to: {script_path}")

    # Create new Notion entry
    print(f"\n[4/4] Creating new Notion entry...")

    # Prepare idea dictionary for Notion
    idea = {
        "title": UPDATED_SCRIPT["title"],
        "hook": UPDATED_SCRIPT["hook"]["script"],
        "key_points": [section["section_title"] for section in UPDATED_SCRIPT["main_sections"]]
    }

    page_id = notion_agent.create_video_entry(idea, UPDATED_SCRIPT)

    if page_id:
        page_url = f"https://notion.so/{page_id.replace('-', '')}"
        print(f"  Created new Notion page!")
        print(f"  Page ID: {page_id}")
        print(f"  URL: {page_url}")
    else:
        print("  Error: Could not create Notion page")

    print("\n" + "=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)

    print(f"\nSummary:")
    print(f"  - Old page archived: {'Yes' if existing_page else 'N/A'}")
    print(f"  - New script saved: {script_path}")
    print(f"  - New Notion page: {'Created' if page_id else 'Failed'}")
    print(f"\nTitle: {UPDATED_SCRIPT['title']}")


if __name__ == "__main__":
    main()
