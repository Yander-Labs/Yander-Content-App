"""
Mindmap Generator Agent
Creates visual mindmaps using D3.js for professional, video-ready graphics.
"""

import json
import subprocess
import os
from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent
from datetime import datetime
from pathlib import Path


class MindmapAgent(BaseAgent):
    """Agent that generates professional D3.js mindmaps for visualizing content ideas."""

    # Available themes for mindmap rendering
    THEMES = ['modern', 'light', 'vibrant', 'minimal']

    def __init__(self):
        super().__init__(name="Mindmap Agent")
        self.renderer_path = Path(__file__).parent.parent / "mindmap-renderer"
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

    def _ensure_renderer_installed(self) -> bool:
        """
        Ensure the Node.js renderer dependencies are installed.

        Returns:
            True if dependencies are installed successfully
        """
        node_modules = self.renderer_path / "node_modules"
        if not node_modules.exists():
            self.logger.info("Installing mindmap renderer dependencies...")
            try:
                result = subprocess.run(
                    ["npm", "install"],
                    cwd=self.renderer_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    self.logger.error(f"npm install failed: {result.stderr}")
                    return False
                self.logger.info("Renderer dependencies installed successfully")
            except subprocess.TimeoutExpired:
                self.logger.error("npm install timed out")
                return False
            except FileNotFoundError:
                self.logger.error("npm not found. Please install Node.js")
                return False
        return True

    def render_with_d3(self,
                       structure: Dict[str, Any],
                       output_dir: str,
                       width: int = 1920,
                       height: int = 1080,
                       theme: str = "modern") -> Dict[str, str]:
        """
        Render mindmap using D3.js Node.js renderer.

        Args:
            structure: Mindmap structure dictionary
            output_dir: Directory to save output files
            width: Output width in pixels
            height: Output height in pixels
            theme: Visual theme ("modern", "light", "vibrant", "minimal")

        Returns:
            Dictionary with paths to generated files (svg, png)
        """
        self.logger.info(f"Rendering mindmap with D3.js: {structure.get('title', 'Untitled')}")

        # Ensure renderer is installed
        if not self._ensure_renderer_installed():
            raise RuntimeError("Failed to install mindmap renderer dependencies")

        # Create temp file for structure
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_structure_file = self.renderer_path / f"temp_structure_{timestamp}.json"

        try:
            # Write structure to temp file
            with open(temp_structure_file, 'w') as f:
                json.dump(structure, f, indent=2)

            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Run the renderer
            cmd = [
                "node",
                str(self.renderer_path / "render.js"),
                str(temp_structure_file),
                output_dir,
                f"--theme={theme}",
                f"--width={width}",
                f"--height={height}"
            ]

            self.logger.info(f"Running renderer: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                self.logger.error(f"Renderer failed: {result.stderr}")
                raise RuntimeError(f"Mindmap renderer failed: {result.stderr}")

            # Parse output to get file paths
            output_lines = result.stdout.strip().split('\n')
            files = {}

            for line in output_lines:
                if 'SVG saved:' in line:
                    files['svg'] = line.split('SVG saved:')[1].strip()
                elif 'PNG saved:' in line:
                    files['png'] = line.split('PNG saved:')[1].strip()

            self.logger.info(f"Renderer output: {files}")
            return files

        finally:
            # Cleanup temp file
            if temp_structure_file.exists():
                temp_structure_file.unlink()

    def create_svg_mindmap(self,
                          structure: Dict[str, Any],
                          width: int = 1920,
                          height: int = 1080,
                          style: str = "modern") -> str:
        """
        Create an SVG mindmap from structure (legacy method - now uses D3.js).

        Args:
            structure: Mindmap structure dictionary
            width: SVG width in pixels
            height: SVG height in pixels
            style: Visual style ("modern", "light", "vibrant", "minimal")

        Returns:
            SVG content as string
        """
        self.logger.info(f"Creating SVG mindmap: {structure.get('title', 'Untitled')}")

        # Use the D3.js renderer
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            files = self.render_with_d3(structure, temp_dir, width, height, style)
            if 'svg' in files:
                with open(files['svg'], 'r') as f:
                    return f.read()

        # Fallback to simple SVG if renderer fails
        self.logger.warning("D3.js renderer failed, using fallback")
        return self._create_fallback_svg(structure, width, height)

    def _create_fallback_svg(self, structure: Dict[str, Any], width: int, height: int) -> str:
        """
        Create a simple fallback SVG if D3.js renderer is unavailable.

        Args:
            structure: Mindmap structure dictionary
            width: SVG width in pixels
            height: SVG height in pixels

        Returns:
            SVG content as string
        """
        import svgwrite
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='#1a1a2e'))

        center_x, center_y = width // 2, height // 2
        title = structure.get('title', 'Mindmap')

        # Central gradient
        central_gradient = dwg.defs.add(dwg.linearGradient(id="central_grad"))
        central_gradient.add_stop_color(offset='0%', color='#667eea')
        central_gradient.add_stop_color(offset='100%', color='#764ba2')

        # Central box
        title_box_width = max(300, len(title) * 12)
        dwg.add(dwg.rect(
            insert=(center_x - title_box_width//2, center_y - 40),
            size=(title_box_width, 80), fill='url(#central_grad)',
            rx=10, ry=10, stroke='#ffffff', stroke_width=3
        ))
        dwg.add(dwg.text(title, insert=(center_x, center_y + 8),
            text_anchor='middle', font_size='28px', font_weight='bold',
            fill='#ffffff', font_family='Arial, sans-serif'))

        return dwg.tostring()

    def execute(self,
                content: Dict[str, Any],
                content_type: str = "video",
                width: int = 1920,
                height: int = 1080,
                style: str = "modern") -> Dict[str, Any]:
        """
        Execute mindmap generation with D3.js renderer.

        Args:
            content: Video script or post content
            content_type: Type of content ("video" or "post")
            width: Output width in pixels
            height: Output height in pixels
            style: Visual theme ("modern", "light", "vibrant", "minimal")

        Returns:
            Dictionary containing mindmap structure and file paths
        """
        # Generate structure using Claude
        structure = self.generate_mindmap_structure(content, content_type)

        if 'error' in structure:
            return structure

        # Save structure first
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        structure_filename = f"mindmap_structure_{timestamp}.json"
        structure_path = self.save_output(structure, structure_filename, "output/mindmaps")

        # Render with D3.js
        output_dir = str(Path(__file__).parent.parent / "output" / "mindmaps")

        try:
            files = self.render_with_d3(structure, output_dir, width, height, style)

            result = {
                "structure": structure,
                "svg_file": files.get('svg'),
                "png_file": files.get('png'),
                "structure_file": structure_path,
                "dimensions": {"width": width, "height": height},
                "theme": style,
                "renderer": "d3js"
            }

            self.logger.info(f"Mindmap generated with D3.js: {files.get('svg')}")

        except Exception as e:
            self.logger.warning(f"D3.js renderer failed: {e}, using fallback")

            # Use fallback SVG renderer
            svg_content = self._create_fallback_svg(structure, width, height)
            svg_filename = f"mindmap_{timestamp}.svg"
            svg_path = self.save_output(svg_content, svg_filename, "output/mindmaps")

            result = {
                "structure": structure,
                "svg_file": svg_path,
                "png_file": None,
                "structure_file": structure_path,
                "dimensions": {"width": width, "height": height},
                "theme": style,
                "renderer": "fallback"
            }

            self.logger.info(f"Mindmap generated with fallback: {svg_path}")

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
