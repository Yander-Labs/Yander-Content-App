"""
Mindmap Generator Agent
Creates visual mindmaps in SVG format for use in YouTube videos.
"""

import json
import svgwrite
from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent
from datetime import datetime


class MindmapAgent(BaseAgent):
    """Agent that generates SVG mindmaps for visualizing content ideas."""

    def __init__(self):
        super().__init__(name="Mindmap Agent")
        self.system_prompt = """You are an expert at creating structured mindmaps for educational content.

Your role is to:
1. Analyze video scripts or content ideas
2. Extract key concepts and their relationships
3. Create a hierarchical structure for visualization
4. Design mindmaps that are clear, educational, and visually appealing

Output mindmap structure in JSON format:
{
  "title": "Central topic",
  "branches": [
    {
      "label": "Main branch",
      "color": "#hexcolor",
      "subbranches": [
        {
          "label": "Sub-topic",
          "notes": ["detail1", "detail2"]
        }
      ]
    }
  ]
}

Guidelines:
- Keep labels concise (2-5 words)
- Use 3-7 main branches maximum
- Use colors to categorize topics
- Include actionable details in subbranches"""

    def generate_mindmap_structure(self,
                                   content: Dict[str, Any],
                                   content_type: str = "video") -> Dict[str, Any]:
        """
        Generate mindmap structure from content.

        Args:
            content: Video script or post content
            content_type: Type of content ("video" or "post")

        Returns:
            Mindmap structure dictionary
        """
        self.logger.info(f"Generating mindmap structure for: {content.get('title', 'Untitled')}")

        # Build the prompt based on content type
        if content_type == "video":
            content_summary = f"""TITLE: {content.get('title', '')}

MAIN SECTIONS:
{chr(10).join(f"- {section.get('section_title', '')}: {section.get('script', '')[:200]}..." for section in content.get('main_sections', []))}"""
        else:
            content_summary = f"""TITLE: {content.get('title', '')}

KEY TAKEAWAYS:
{chr(10).join(f"- {point}" for point in content.get('key_takeaways', []))}

BODY:
{content.get('body', '')[:500]}"""

        user_message = f"""Create a mindmap structure for the following content:

{content_summary}

Return a JSON structure that can be used to generate a visual mindmap.
Include 3-7 main branches with relevant subbranches.
Use appropriate colors to categorize topics."""

        response = self.call_claude(
            system_prompt=self.system_prompt,
            user_message=user_message,
            max_tokens=2048
        )

        # Parse response
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            structure = json.loads(json_str)
            return structure

        except Exception as e:
            self.logger.error(f"Error parsing mindmap structure: {str(e)}")
            return {
                "error": str(e),
                "raw_response": response
            }

    def create_svg_mindmap(self,
                          structure: Dict[str, Any],
                          width: int = 1920,
                          height: int = 1080,
                          style: str = "modern") -> str:
        """
        Create an SVG mindmap from structure.

        Args:
            structure: Mindmap structure dictionary
            width: SVG width in pixels
            height: SVG height in pixels
            style: Visual style ("modern", "minimal", "colorful")

        Returns:
            SVG content as string
        """
        self.logger.info(f"Creating SVG mindmap: {structure.get('title', 'Untitled')}")

        # Create SVG drawing
        dwg = svgwrite.Drawing(size=(width, height))

        # Add background
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='#1a1a2e'))

        # Center point
        center_x, center_y = width // 2, height // 2

        # Draw central topic
        title = structure.get('title', 'Mindmap')
        title_box_width = max(300, len(title) * 12)
        title_box_height = 80

        # Central box with gradient
        central_gradient = dwg.defs.add(dwg.linearGradient(id="central_grad"))
        central_gradient.add_stop_color(offset='0%', color='#667eea')
        central_gradient.add_stop_color(offset='100%', color='#764ba2')

        dwg.add(dwg.rect(
            insert=(center_x - title_box_width//2, center_y - title_box_height//2),
            size=(title_box_width, title_box_height),
            fill='url(#central_grad)',
            rx=10,
            ry=10,
            stroke='#ffffff',
            stroke_width=3
        ))

        # Central title text
        dwg.add(dwg.text(
            title,
            insert=(center_x, center_y + 8),
            text_anchor='middle',
            font_size='28px',
            font_weight='bold',
            fill='#ffffff',
            font_family='Arial, sans-serif'
        ))

        # Draw branches
        branches = structure.get('branches', [])
        num_branches = len(branches)

        for i, branch in enumerate(branches):
            # Calculate angle for this branch
            angle = (2 * 3.14159 * i / num_branches) - (3.14159 / 2)  # Start at top

            # Branch position
            branch_distance = 400
            branch_x = center_x + int(branch_distance * 0.7 * (1 if i % 2 == 0 else -1) * abs(angle / 3.14159))
            branch_y = center_y + int(branch_distance * 0.5 * (i - num_branches/2) / (num_branches/2))

            # Ensure branches stay within bounds
            branch_x = max(200, min(width - 200, branch_x))
            branch_y = max(150, min(height - 150, branch_y))

            # Draw connecting line
            dwg.add(dwg.line(
                start=(center_x, center_y),
                end=(branch_x, branch_y),
                stroke=branch.get('color', '#00d4ff'),
                stroke_width=3,
                opacity=0.6
            ))

            # Draw branch box
            branch_label = branch.get('label', f'Branch {i+1}')
            branch_width = max(180, len(branch_label) * 10)
            branch_height = 60

            dwg.add(dwg.rect(
                insert=(branch_x - branch_width//2, branch_y - branch_height//2),
                size=(branch_width, branch_height),
                fill=branch.get('color', '#00d4ff'),
                rx=8,
                ry=8,
                stroke='#ffffff',
                stroke_width=2
            ))

            dwg.add(dwg.text(
                branch_label,
                insert=(branch_x, branch_y + 6),
                text_anchor='middle',
                font_size='18px',
                font_weight='bold',
                fill='#ffffff',
                font_family='Arial, sans-serif'
            ))

            # Draw subbranches
            subbranches = branch.get('subbranches', [])
            for j, subbranch in enumerate(subbranches[:3]):  # Max 3 subbranches per branch
                # Subbranch position (stacked vertically near branch)
                sub_x = branch_x + 250
                sub_y = branch_y + (j - 1) * 80

                # Ensure subbranches stay within bounds
                sub_x = max(100, min(width - 100, sub_x))
                sub_y = max(100, min(height - 100, sub_y))

                # Draw connecting line
                dwg.add(dwg.line(
                    start=(branch_x + branch_width//2, branch_y),
                    end=(sub_x - 70, sub_y),
                    stroke=branch.get('color', '#00d4ff'),
                    stroke_width=2,
                    opacity=0.4,
                    stroke_dasharray='5,5'
                ))

                # Draw subbranch
                sub_label = subbranch.get('label', f'Sub {j+1}')
                sub_width = max(140, len(sub_label) * 9)
                sub_height = 45

                dwg.add(dwg.rect(
                    insert=(sub_x - sub_width//2, sub_y - sub_height//2),
                    size=(sub_width, sub_height),
                    fill='#2d2d44',
                    rx=6,
                    ry=6,
                    stroke=branch.get('color', '#00d4ff'),
                    stroke_width=2
                ))

                dwg.add(dwg.text(
                    sub_label,
                    insert=(sub_x, sub_y + 5),
                    text_anchor='middle',
                    font_size='14px',
                    fill='#ffffff',
                    font_family='Arial, sans-serif'
                ))

        return dwg.tostring()

    def execute(self,
                content: Dict[str, Any],
                content_type: str = "video",
                width: int = 1920,
                height: int = 1080,
                style: str = "modern") -> Dict[str, Any]:
        """
        Execute mindmap generation.

        Args:
            content: Video script or post content
            content_type: Type of content ("video" or "post")
            width: SVG width
            height: SVG height
            style: Visual style

        Returns:
            Dictionary containing mindmap structure and SVG file path
        """
        # Generate structure
        structure = self.generate_mindmap_structure(content, content_type)

        if 'error' in structure:
            return structure

        # Create SVG
        svg_content = self.create_svg_mindmap(structure, width, height, style)

        # Save SVG
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        svg_filename = f"mindmap_{timestamp}.svg"
        svg_path = self.save_output(svg_content, svg_filename, "output/mindmaps")

        # Save structure
        structure_filename = f"mindmap_structure_{timestamp}.json"
        structure_path = self.save_output(structure, structure_filename, "output/mindmaps")

        result = {
            "structure": structure,
            "svg_file": svg_path,
            "structure_file": structure_path,
            "dimensions": {"width": width, "height": height}
        }

        self.logger.info(f"Mindmap generated: {svg_path}")

        return result


if __name__ == "__main__":
    # Example usage
    agent = MindmapAgent()

    example_content = {
        "title": "5 Automation Workflows for Marketing Agencies",
        "main_sections": [
            {
                "section_title": "Client Onboarding",
                "script": "Automate your client onboarding process to save time..."
            },
            {
                "section_title": "Report Generation",
                "script": "Generate reports automatically every week..."
            }
        ]
    }

    result = agent.execute(content=example_content, content_type="video")
    print(json.dumps({k: v for k, v in result.items() if k != 'structure'}, indent=2))
