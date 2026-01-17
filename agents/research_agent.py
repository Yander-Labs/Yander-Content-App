"""
Content Research Agent
Researches ideas for content using provided data, tool information, and online sources.
"""

import os
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from .base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent that researches content ideas for marketing agency topics."""

    def __init__(self):
        super().__init__(name="Research Agent")
        self.system_prompt = """You are an expert content researcher specializing in marketing agency operations, growth, and strategy.

Your role is to:
1. Analyze provided data about the user's marketing tool/agency
2. Research relevant trends and insights online
3. Generate compelling content ideas for:
   - Long-form YouTube videos (10-30 minutes)
   - Text-based posts (150+ words)
4. Focus on topics that help marketing agency owners with operations, marketing, and growth
5. Ensure ideas are educational, actionable, and hook the audience

Output your research in JSON format with:
{
  "video_ideas": [
    {
      "title": "string",
      "description": "string",
      "hook": "string",
      "key_points": ["string"],
      "target_length": "number (minutes)",
      "keywords": ["string"]
    }
  ],
  "post_ideas": [
    {
      "title": "string",
      "description": "string",
      "hook": "string",
      "key_points": ["string"],
      "target_length": "number (words)",
      "keywords": ["string"]
    }
  ],
  "research_sources": ["string"]
}"""

    def search_web(self, query: str) -> List[Dict[str, str]]:
        """
        Search the web for relevant information.

        Args:
            query: Search query

        Returns:
            List of search results with title, snippet, and URL
        """
        try:
            # Note: In production, use Google Custom Search API or similar
            # For now, this is a placeholder for web search functionality
            self.logger.info(f"Searching web for: {query}")

            # You can integrate with Google Custom Search API here
            # Example endpoint: https://www.googleapis.com/customsearch/v1

            return []
        except Exception as e:
            self.logger.error(f"Error searching web: {str(e)}")
            return []

    def scrape_url(self, url: str) -> str:
        """
        Scrape content from a URL.

        Args:
            url: URL to scrape

        Returns:
            Extracted text content
        """
        try:
            self.logger.info(f"Scraping URL: {url}")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return text[:5000]  # Limit to first 5000 characters

        except Exception as e:
            self.logger.error(f"Error scraping URL: {str(e)}")
            return ""

    def execute(self,
                tool_info: Optional[str] = None,
                user_data: Optional[str] = None,
                topics: Optional[List[str]] = None,
                num_video_ideas: int = 3,
                num_post_ideas: int = 5) -> Dict[str, Any]:
        """
        Execute content research.

        Args:
            tool_info: Information about the user's marketing tool
            user_data: Additional data provided by the user
            topics: Specific topics to research
            num_video_ideas: Number of video ideas to generate
            num_post_ideas: Number of post ideas to generate

        Returns:
            Dictionary containing research results
        """
        self.logger.info("Starting content research...")

        # Build research context
        context_parts = []

        if tool_info:
            context_parts.append(f"MARKETING TOOL INFORMATION:\n{tool_info}")

        if user_data:
            context_parts.append(f"USER PROVIDED DATA:\n{user_data}")

        if topics:
            context_parts.append(f"FOCUS TOPICS:\n" + "\n".join(f"- {topic}" for topic in topics))

        # Load content style references if available
        import json
        import os
        style_ref_path = "data/content_style_references.json"
        if os.path.exists(style_ref_path):
            try:
                with open(style_ref_path, 'r') as f:
                    style_refs = json.load(f)
                    # Add pattern analysis to context
                    if style_refs.get('pattern_analysis'):
                        patterns = style_refs['pattern_analysis']
                        pattern_summary = f"""SUCCESSFUL CONTENT PATTERNS (from top performers):

Common Hook Styles:
{chr(10).join(f"- {hook}" for hook in patterns.get('common_hooks', []))}

Proven Content Structures:
{chr(10).join(f"- {structure}" for structure in patterns.get('content_structures', []))}

Engagement Tactics:
{chr(10).join(f"- {tactic}" for tactic in patterns.get('engagement_tactics', []))}

Use these patterns as inspiration (don't copy directly, but apply the principles)."""
                        context_parts.append(pattern_summary)
                        self.logger.info("Loaded content style references")
            except Exception as e:
                self.logger.warning(f"Could not load content style references: {str(e)}")

        # Perform web research for trending topics
        research_queries = [
            "marketing agency operations best practices 2026",
            "marketing agency growth strategies",
            "marketing agency automation tools",
            "marketing agency client management"
        ]

        if topics:
            research_queries.extend(topics)

        # Note: Web search would be integrated here
        # For now, we'll rely on Claude's knowledge and user-provided data

        # Build the research prompt
        user_message = f"""Research and generate content ideas for a marketing agency focused on operations, marketing, and growth.

{chr(10).join(context_parts)}

Generate {num_video_ideas} video ideas and {num_post_ideas} post ideas.

Requirements:
- Video ideas should be 10-30 minutes long
- Post ideas should be 150+ words
- Each idea must have a compelling hook
- Focus on educating marketing agency owners
- Include actionable insights and strategies
- Base ideas on current trends and best practices

Return your response in the JSON format specified."""

        # Call Claude for research
        response = self.call_claude(
            system_prompt=self.system_prompt,
            user_message=user_message,
            max_tokens=4096
        )

        # Parse response
        try:
            import json
            # Extract JSON from response (Claude might wrap it in markdown)
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            research_results = json.loads(json_str)

            # Save results
            output_path = self.save_output(
                research_results,
                f"research_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "output"
            )

            research_results['output_file'] = output_path

            self.logger.info(f"Research complete. Generated {len(research_results.get('video_ideas', []))} video ideas and {len(research_results.get('post_ideas', []))} post ideas")

            return research_results

        except Exception as e:
            self.logger.error(f"Error parsing research results: {str(e)}")
            return {
                "error": str(e),
                "raw_response": response
            }


if __name__ == "__main__":
    # Example usage
    from datetime import datetime

    agent = ResearchAgent()
    results = agent.execute(
        tool_info="Marketing automation platform that helps agencies manage clients and campaigns",
        topics=["client retention", "agency scaling", "automation workflows"],
        num_video_ideas=2,
        num_post_ideas=3
    )

    print(json.dumps(results, indent=2))
