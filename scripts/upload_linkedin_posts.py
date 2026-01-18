#!/usr/bin/env python3
"""
Script to create and upload 5 LinkedIn posts for marketing agency owners to Notion.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.notion_agent import NotionAgent

# 5 Long-form LinkedIn posts for marketing agency owners
LINKEDIN_POSTS = [
    {
        "idea": {
            "title": "The Decision That Transformed My Agency"
        },
        "post": {
            "hook": "One client represented 40% of our revenue. Then I made the hardest strategic decision of my career.",
            "full_post": """One client represented 40% of our revenue.

Then I made the hardest strategic decision of my career.

We had built an incredible partnership. They were our anchor account, the one that gave us stability when we were growing. I'm grateful for what that relationship taught us.

But I started noticing something.

We had become so focused on one account that our other clients weren't getting our best work. My team was stretched thin. We were building our entire business around a single relationship.

That's when I realized: I wasn't building a sustainable agency. I was building a dependency.

So we made a deliberate choice.

We started investing more in business development. We focused on building deeper relationships with our other accounts. We created capacity to take on new partnerships.

Over the next year, we diversified. We grew our client base thoughtfully. We built a portfolio where no single client represented more than 15% of revenue.

The result?

When market conditions shifted and that original client reduced their budget, we didn't panic. We adapted. Our diversified base kept us stable while we adjusted.

Here's what I learned:

Your best clients deserve your best work. But your business deserves a foundation that can weather any storm.

Diversification isn't about loyalty. It's about building something that lasts.

The agencies that thrive long-term spread their risk without spreading themselves thin.

What percentage of revenue would make you uncomfortable if it came from one client?

#MarketingAgency #AgencyLife #ClientManagement #BusinessGrowth #Leadership""",
            "key_takeaways": [
                "Revenue concentration creates strategic risk",
                "Diversification enables long-term stability",
                "Strong client relationships and smart business strategy coexist",
                "Building sustainably requires deliberate choices"
            ],
            "hashtags": ["#MarketingAgency", "#AgencyLife", "#ClientManagement", "#BusinessGrowth", "#Leadership"]
        }
    },
    {
        "idea": {
            "title": "Why I Stopped Working 80-Hour Weeks"
        },
        "post": {
            "hook": "I used to brag about working 80-hour weeks. Then my body gave me a wake-up call I couldn't ignore.",
            "full_post": """I used to brag about working 80-hour weeks.

Then my body gave me a wake-up call I couldn't ignore.

Three years into running my agency, I ended up in the ER. Chest pains. Shortness of breath. I thought it was a heart attack at 34.

It wasn't. But the doctor's words hit harder than any diagnosis:

"You're not having a heart attack. You're having a lifestyle."

I built an agency that couldn't function without me. Every decision ran through me. Every client wanted to talk to "the founder." I wore it like a badge of honor.

But I wasn't building a business. I was building a prison.

The turning point came when I asked myself one question:

"What would happen to my clients if I got hit by a bus tomorrow?"

The answer terrified me. Everything would collapse.

So I made changes. Painful ones.

I hired people smarter than me and actually let them make decisions. I documented every process in my head. I told clients they'd get better results working with my team than with me alone.

Some clients left. Most stayed. And something magical happened.

Revenue grew 40% the year I started working less.

Not because I'm special. Because I finally got out of my own way.

Your agency doesn't need you to be a hero.

It needs you to be a builder.

What's one thing only you do that someone else could learn?

#AgencyOwner #Entrepreneurship #WorkLifeBalance #Burnout #ScalingBusiness""",
            "key_takeaways": [
                "Hustle culture can destroy your health",
                "Building systems beats being indispensable",
                "Delegation often accelerates growth",
                "Sustainable pace creates sustainable businesses"
            ],
            "hashtags": ["#AgencyOwner", "#Entrepreneurship", "#WorkLifeBalance", "#Burnout", "#ScalingBusiness"]
        }
    },
    {
        "idea": {
            "title": "The Pricing Mistake That Cost Me $200K"
        },
        "post": {
            "hook": "A prospect told me my prices were too high. So I dropped them. That single decision cost me over $200,000.",
            "full_post": """A prospect told me my prices were too high.

So I dropped them.

That single decision cost me over $200,000.

Here's what happened:

Early in my agency, a dream client said our proposal was "out of budget." Without hesitating, I offered a 30% discount. They signed immediately.

I thought I'd won.

I hadn't.

That discounted rate became our anchor. When they referred us to three other companies, they all expected the same pricing. When it came time to renew, they expected another discount.

Eighteen months later, I had four clients paying rates that barely covered our costs. My team was overworked. Profits were nonexistent.

But here's what really hurt:

The original prospect later told me they had budget for our full rate. They just wanted to see if we'd negotiate.

The lesson changed everything about how I run my agency:

Price is a signal of value.

When you discount easily, you tell clients your work isn't worth what you quoted. You attract price-sensitive clients who will always push for more.

The agencies that thrive don't compete on price. They compete on outcomes, expertise, and the problems they solve.

Now when someone says we're too expensive, I say: "We might not be the right fit, and that's okay."

Most of them sign anyway. The ones who don't were never going to be good clients.

Your price isn't just a number. It's a filter.

Have you ever regretted a discount you gave?

#PricingStrategy #AgencyGrowth #ValueBasedPricing #MarketingAgency #SalesStrategy""",
            "key_takeaways": [
                "Discounting signals low confidence in your value",
                "Price anchoring affects all future negotiations",
                "Premium pricing attracts premium clients",
                "Walking away protects your business"
            ],
            "hashtags": ["#PricingStrategy", "#AgencyGrowth", "#ValueBasedPricing", "#MarketingAgency", "#SalesStrategy"]
        }
    },
    {
        "idea": {
            "title": "The Leadership Lesson That Changed How I Build Teams"
        },
        "post": {
            "hook": "I used to think hiring great people was the hard part. Then I learned what actually makes teams thrive.",
            "full_post": """I used to think hiring great people was the hard part.

Then I learned what actually makes teams thrive.

Early in my agency, I brought on a talented team member. Smart, motivated, eager to contribute. I was excited about their potential.

But I made a classic founder mistake.

I was so focused on client work that I didn't invest in their onboarding. No structured plan. No clear milestones. I assumed talent would figure it out.

A few weeks in, they shared honest feedback: "I want to do great work, but I'm not sure what great looks like here."

That conversation changed everything for me.

I realized I wasn't failing at hiring. I was failing at leading.

So I built the onboarding experience I wished I'd had:

A 30-day roadmap with clear expectations for each week. Weekly one-on-ones focused on removing obstacles. Documented processes so nobody had to guess how we do things.

The transformation was immediate.

New team members hit their stride faster. They felt confident instead of confused. They stayed longer because they could see a path to growth.

One of our early hires after this shift became our operations director. Another now leads our largest accounts. They didn't succeed because they were different. They succeeded because I learned to set them up for success.

Here's what I tell every agency owner now:

Your team's performance is a mirror of your leadership.

Invest in onboarding like it's your most important client deliverable. Because in many ways, it is.

What's one thing that helped you ramp up quickly in a new role?

#Hiring #TeamBuilding #Leadership #AgencyLife #EmployeeRetention""",
            "key_takeaways": [
                "Onboarding investment drives retention",
                "Clear expectations enable high performance",
                "Leadership skills are developed, not innate",
                "Great environments bring out the best in people"
            ],
            "hashtags": ["#Hiring", "#TeamBuilding", "#Leadership", "#AgencyLife", "#EmployeeRetention"]
        }
    },
    {
        "idea": {
            "title": "The System That Saved My Agency"
        },
        "post": {
            "hook": "My agency almost died because I kept everything in my head. One sick day proved how fragile we really were.",
            "full_post": """My agency almost died because I kept everything in my head.

One sick day proved how fragile we really were.

I came down with the flu. Nothing serious, but I was out for a week. When I came back, I found:

Three missed client deadlines. Two angry emails from accounts I thought were happy. One team member who almost quit from the stress.

All because nobody knew how I did things.

The client reporting process? In my head. The campaign launch checklist? In my head. The escalation protocol when things went wrong? You guessed it.

My "efficient" way of running things was actually a ticking time bomb.

That week forced me to ask an uncomfortable question:

Am I running an agency or a one-person show with expensive helpers?

I spent the next three months documenting everything. Every process. Every template. Every "obvious" thing that wasn't obvious to anyone but me.

It was tedious. It felt like it was slowing me down. My ego hated it.

But here's what happened after:

New hires got productive in weeks instead of months. Client delivery became consistent, regardless of who was working on it. I took my first real vacation in four years.

The unsexy truth about scaling an agency:

Systems are freedom.

Without them, you're not the owner. You're the bottleneck.

The best time to document a process is before you desperately need someone else to do it.

What process do you keep meaning to document but haven't yet?

#AgencyOperations #SystemsThinking #ProcessImprovement #ScalingBusiness #MarketingAgency""",
            "key_takeaways": [
                "Undocumented knowledge is a liability",
                "Systems create freedom, not bureaucracy",
                "Consistency requires documented processes",
                "Delegation is impossible without clarity"
            ],
            "hashtags": ["#AgencyOperations", "#SystemsThinking", "#ProcessImprovement", "#ScalingBusiness", "#MarketingAgency"]
        }
    }
]


def main():
    """Create and upload all LinkedIn posts to Notion."""
    print("=" * 60)
    print("LinkedIn Posts Upload to Notion")
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
