#!/usr/bin/env python3
"""
Script to generate mindmaps for all video scripts using the elevated theme.
"""

import sys
import os
import json
import re
import subprocess
from pathlib import Path
from glob import glob

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.mindmap_agent import MindmapAgent


def sanitize_filename(name: str) -> str:
    """Convert title to safe filename."""
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', name)
    clean = re.sub(r'\s+', '_', clean)
    clean = re.sub(r'_+', '_', clean)
    return clean[:80].lower()


def main():
    """Generate mindmaps for all video scripts."""
    print("=" * 60)
    print("Generating Mindmaps for All Videos")
    print("=" * 60)

    # Find all video scripts (exclude post scripts)
    scripts_dir = Path(__file__).parent.parent / "output" / "scripts"
    video_scripts = sorted(glob(str(scripts_dir / "script_*.json")))

    print(f"\nFound {len(video_scripts)} video scripts")

    # Initialize mindmap agent
    agent = MindmapAgent()
    renderer_path = Path(__file__).parent.parent / "mindmap-renderer"
    output_dir = Path(__file__).parent.parent / "output" / "mindmaps"

    print(f"Output directory: {output_dir}")
    print(f"Renderer path: {renderer_path}\n")

    results = []
    skipped = []

    for script_path in video_scripts:
        full_path = Path(script_path)

        # Load script
        with open(full_path, 'r') as f:
            script = json.load(f)

        title = script.get('title', 'Untitled')
        safe_name = sanitize_filename(title)

        # Check if mindmap already exists with new naming
        existing_png = output_dir / f"{safe_name}.png"
        if existing_png.exists():
            print(f"SKIP (exists): {title[:50]}...")
            skipped.append(title)
            continue

        print(f"\nProcessing: {title[:60]}...")
        print("-" * 50)

        # Generate mindmap structure using Claude
        print("  Generating mindmap structure...")
        structure = agent.generate_mindmap_structure(script, content_type="video")

        if 'error' in structure:
            print(f"  ERROR: {structure.get('error')}")
            continue

        # Save structure with proper filename
        structure_file = output_dir / f"{safe_name}_structure.json"

        with open(structure_file, 'w') as f:
            json.dump(structure, f, indent=2)
        print(f"  Structure saved: {structure_file.name}")

        # Render using Node.js renderer with elevated theme
        print("  Rendering mindmap...")

        cmd = [
            "node",
            str(renderer_path / "render.js"),
            str(structure_file),
            str(output_dir),
            "--theme=elevated"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"  RENDER ERROR: {result.stderr}")
            continue

        # Parse output
        svg_path = None
        png_path = None
        for line in result.stdout.strip().split('\n'):
            if 'SVG saved:' in line:
                svg_path = line.split('SVG saved:')[1].strip()
            elif 'PNG saved:' in line:
                png_path = line.split('PNG saved:')[1].strip()

        print(f"  SVG: {os.path.basename(svg_path) if svg_path else 'N/A'}")
        print(f"  PNG: {os.path.basename(png_path) if png_path else 'N/A'}")

        results.append({
            "title": title,
            "safe_name": safe_name,
            "structure_file": str(structure_file),
            "svg_file": svg_path,
            "png_file": png_path
        })

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTotal scripts found: {len(video_scripts)}")
    print(f"Newly generated: {len(results)}")
    print(f"Skipped (already exist): {len(skipped)}")

    if results:
        print("\nNewly generated mindmaps:")
        for r in results:
            print(f"  - {r['title'][:50]}...")
            print(f"    -> {r['safe_name']}.png")

    print("\nDone!")


if __name__ == "__main__":
    main()
