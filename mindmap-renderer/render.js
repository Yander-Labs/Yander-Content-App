#!/usr/bin/env node
/**
 * D3.js Mindmap Renderer
 * Creates beautiful force-directed mindmaps from JSON structure
 */

import * as d3 from 'd3';
import { JSDOM } from 'jsdom';
import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

// Configuration
const CONFIG = {
  width: 1920,
  height: 1080,
  backgroundColor: '#0f0f1a',
  centerNode: {
    radius: 80,
    fontSize: 22,
    fontWeight: 'bold',
    gradient: ['#667eea', '#764ba2']
  },
  branchNode: {
    radius: 55,
    fontSize: 14,
    fontWeight: '600'
  },
  subbranchNode: {
    radius: 45,
    fontSize: 12,
    fontWeight: '500'
  },
  link: {
    strokeWidth: 3,
    opacity: 0.7
  },
  animation: {
    duration: 1000
  }
};

// Color palettes for different themes
const THEMES = {
  modern: {
    background: '#0f0f1a',
    centerGradient: ['#667eea', '#764ba2'],
    branchColors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8'],
    textColor: '#ffffff',
    linkOpacity: 0.6
  },
  light: {
    background: '#f8f9fa',
    centerGradient: ['#6366f1', '#8b5cf6'],
    branchColors: ['#ef4444', '#06b6d4', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#14b8a6'],
    textColor: '#1f2937',
    linkOpacity: 0.5
  },
  vibrant: {
    background: '#1a1a2e',
    centerGradient: ['#00d4ff', '#090979'],
    branchColors: ['#ff006e', '#fb5607', '#ffbe0b', '#8338ec', '#3a86ff', '#06ffa5', '#ff595e'],
    textColor: '#ffffff',
    linkOpacity: 0.7
  },
  minimal: {
    background: '#ffffff',
    centerGradient: ['#374151', '#111827'],
    branchColors: ['#6b7280', '#9ca3af', '#4b5563', '#374151', '#d1d5db', '#6b7280', '#9ca3af'],
    textColor: '#111827',
    linkOpacity: 0.3
  }
};

/**
 * Convert mindmap structure to hierarchical data for D3
 */
function convertToHierarchy(structure) {
  const root = {
    name: structure.title,
    type: 'center',
    children: []
  };

  structure.branches.forEach((branch, i) => {
    const branchNode = {
      name: branch.label,
      type: 'branch',
      color: branch.color,
      index: i,
      children: []
    };

    if (branch.subbranches) {
      branch.subbranches.forEach((sub, j) => {
        branchNode.children.push({
          name: sub.label,
          type: 'subbranch',
          notes: sub.notes || [],
          parentColor: branch.color,
          index: j
        });
      });
    }

    root.children.push(branchNode);
  });

  return root;
}

/**
 * Estimate node dimensions based on text
 */
function getNodeDimensions(name, type) {
  const textLength = name.length;
  if (type === 'center') {
    return { width: Math.max(200, textLength * 11 + 60), height: 80 };
  } else if (type === 'branch') {
    return { width: Math.max(120, textLength * 9 + 40), height: 50 };
  } else {
    return { width: Math.max(100, textLength * 8 + 30), height: 40 };
  }
}

/**
 * Check if two rectangles overlap
 */
function rectsOverlap(r1, r2, padding = 20) {
  return !(r1.x + r1.width / 2 + padding < r2.x - r2.width / 2 - padding ||
           r1.x - r1.width / 2 - padding > r2.x + r2.width / 2 + padding ||
           r1.y + r1.height / 2 + padding < r2.y - r2.height / 2 - padding ||
           r1.y - r1.height / 2 - padding > r2.y + r2.height / 2 + padding);
}

/**
 * Create radial tree layout with collision avoidance
 */
function createRadialLayout(hierarchy, width, height) {
  const centerX = width / 2;
  const centerY = height / 2;
  const padding = 55; // Minimum padding between nodes

  // Position center node
  hierarchy.x = centerX;
  hierarchy.y = centerY;
  const centerDims = getNodeDimensions(hierarchy.name, 'center');
  hierarchy.width = centerDims.width;
  hierarchy.height = centerDims.height;

  const branches = hierarchy.children || [];
  const numBranches = branches.length;

  // Calculate branch positions in a radial pattern
  const branchRadius = Math.min(width, height) * 0.35;

  // Collect all nodes for collision detection
  const allNodes = [hierarchy];

  branches.forEach((branch, i) => {
    // Distribute branches evenly around the center, starting from top
    const angle = (2 * Math.PI * i / numBranches) - Math.PI / 2;
    branch.x = centerX + branchRadius * Math.cos(angle);
    branch.y = centerY + branchRadius * Math.sin(angle);
    branch.angle = angle;

    const branchDims = getNodeDimensions(branch.name, 'branch');
    branch.width = branchDims.width;
    branch.height = branchDims.height;
    allNodes.push(branch);

    // Position subbranches - extend outward from center
    const subbranches = branch.children || [];
    const subCount = subbranches.length;

    if (subCount === 0) return;

    // Calculate direction outward from center
    const outwardAngle = angle;

    // Position subbranches in a stacked column extending outward
    const subRadius = 220; // Distance to first subbranch
    const subSpacing = 70; // Spacing between stacked subbranches

    subbranches.forEach((sub, j) => {
      // Position along the outward direction, then stack perpendicular
      const baseX = branch.x + subRadius * Math.cos(outwardAngle);
      const baseY = branch.y + subRadius * Math.sin(outwardAngle);

      // Stack subbranches perpendicular to the outward direction
      const perpAngle = outwardAngle + Math.PI / 2;
      const stackOffset = (j - (subCount - 1) / 2) * subSpacing;

      sub.x = baseX + stackOffset * Math.cos(perpAngle);
      sub.y = baseY + stackOffset * Math.sin(perpAngle);
      sub.angle = outwardAngle;

      const subDims = getNodeDimensions(sub.name, 'subbranch');
      sub.width = subDims.width;
      sub.height = subDims.height;
      allNodes.push(sub);
    });
  });

  // Collision resolution - push overlapping nodes apart
  const maxIterations = 100; // More iterations for better resolution
  for (let iter = 0; iter < maxIterations; iter++) {
    let hasOverlap = false;

    for (let i = 0; i < allNodes.length; i++) {
      for (let j = i + 1; j < allNodes.length; j++) {
        const n1 = allNodes[i];
        const n2 = allNodes[j];

        // Skip center node - it stays fixed
        if (n1.type === 'center' || n2.type === 'center') continue;

        if (rectsOverlap(n1, n2, padding)) {
          hasOverlap = true;

          // Calculate push direction
          const dx = n2.x - n1.x;
          const dy = n2.y - n1.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;

          // Push nodes apart - stronger force
          const pushForce = 35;
          const nx = dx / dist;
          const ny = dy / dist;

          // Move the node that's further from center (subbranches move more)
          if (n2.type === 'subbranch' && n1.type !== 'subbranch') {
            n2.x += nx * pushForce;
            n2.y += ny * pushForce;
          } else if (n1.type === 'subbranch' && n2.type !== 'subbranch') {
            n1.x -= nx * pushForce;
            n1.y -= ny * pushForce;
          } else {
            // Both same type - push both
            n1.x -= nx * pushForce * 0.5;
            n1.y -= ny * pushForce * 0.5;
            n2.x += nx * pushForce * 0.5;
            n2.y += ny * pushForce * 0.5;
          }
        }
      }
    }

    if (!hasOverlap) break;
  }

  // Ensure all nodes stay within bounds
  const margin = 60;
  allNodes.forEach(node => {
    if (node.type === 'center') return;
    node.x = Math.max(margin + node.width / 2, Math.min(width - margin - node.width / 2, node.x));
    node.y = Math.max(margin + node.height / 2, Math.min(height - margin - node.height / 2, node.y));
  });

  return hierarchy;
}

/**
 * Generate curved path between two points (organic mindmap style)
 */
function generateCurvedPath(source, target, type = 'branch') {
  const dx = target.x - source.x;
  const dy = target.y - source.y;
  const dr = Math.sqrt(dx * dx + dy * dy);

  // Control point offset for bezier curve
  const curvature = type === 'branch' ? 0.3 : 0.4;

  // Calculate perpendicular offset for control points
  const mx = (source.x + target.x) / 2;
  const my = (source.y + target.y) / 2;

  // Add slight curve by offsetting the midpoint
  const offsetX = -dy * curvature * 0.3;
  const offsetY = dx * curvature * 0.3;

  const cx = mx + offsetX;
  const cy = my + offsetY;

  return `M ${source.x},${source.y} Q ${cx},${cy} ${target.x},${target.y}`;
}

/**
 * Create SVG mindmap using D3.js
 */
function createMindmapSVG(structure, options = {}) {
  const {
    width = CONFIG.width,
    height = CONFIG.height,
    theme = 'modern'
  } = options;

  const themeConfig = THEMES[theme] || THEMES.modern;

  // Create virtual DOM
  const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
  const document = dom.window.document;

  // Create SVG
  const svg = d3.select(document.body)
    .append('svg')
    .attr('xmlns', 'http://www.w3.org/2000/svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`);

  // Add definitions for gradients and filters
  const defs = svg.append('defs');

  // Background gradient
  const bgGradient = defs.append('linearGradient')
    .attr('id', 'bg-gradient')
    .attr('x1', '0%')
    .attr('y1', '0%')
    .attr('x2', '100%')
    .attr('y2', '100%');

  bgGradient.append('stop')
    .attr('offset', '0%')
    .attr('stop-color', themeConfig.background);
  bgGradient.append('stop')
    .attr('offset', '100%')
    .attr('stop-color', d3.color(themeConfig.background).darker(0.3));

  // Center node gradient
  const centerGradient = defs.append('linearGradient')
    .attr('id', 'center-gradient')
    .attr('x1', '0%')
    .attr('y1', '0%')
    .attr('x2', '100%')
    .attr('y2', '100%');

  centerGradient.append('stop')
    .attr('offset', '0%')
    .attr('stop-color', themeConfig.centerGradient[0]);
  centerGradient.append('stop')
    .attr('offset', '100%')
    .attr('stop-color', themeConfig.centerGradient[1]);

  // Drop shadow filter
  const shadow = defs.append('filter')
    .attr('id', 'drop-shadow')
    .attr('x', '-50%')
    .attr('y', '-50%')
    .attr('width', '200%')
    .attr('height', '200%');

  shadow.append('feDropShadow')
    .attr('dx', '0')
    .attr('dy', '4')
    .attr('stdDeviation', '8')
    .attr('flood-color', 'rgba(0,0,0,0.3)');

  // Glow filter for nodes
  const glow = defs.append('filter')
    .attr('id', 'glow')
    .attr('x', '-50%')
    .attr('y', '-50%')
    .attr('width', '200%')
    .attr('height', '200%');

  glow.append('feGaussianBlur')
    .attr('stdDeviation', '3')
    .attr('result', 'coloredBlur');

  const glowMerge = glow.append('feMerge');
  glowMerge.append('feMergeNode').attr('in', 'coloredBlur');
  glowMerge.append('feMergeNode').attr('in', 'SourceGraphic');

  // Background
  svg.append('rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'url(#bg-gradient)');

  // Add subtle grid pattern
  const gridPattern = defs.append('pattern')
    .attr('id', 'grid')
    .attr('width', 40)
    .attr('height', 40)
    .attr('patternUnits', 'userSpaceOnUse');

  gridPattern.append('circle')
    .attr('cx', 20)
    .attr('cy', 20)
    .attr('r', 1)
    .attr('fill', themeConfig.textColor)
    .attr('opacity', 0.05);

  svg.append('rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'url(#grid)');

  // Convert and layout data
  const hierarchy = convertToHierarchy(structure);
  createRadialLayout(hierarchy, width, height);

  // Create main group
  const g = svg.append('g').attr('class', 'mindmap');

  // Collect all links
  const links = [];
  const branches = hierarchy.children || [];

  branches.forEach((branch, i) => {
    // Link from center to branch
    links.push({
      source: hierarchy,
      target: branch,
      type: 'branch',
      color: branch.color || themeConfig.branchColors[i % themeConfig.branchColors.length]
    });

    // Links from branch to subbranches
    (branch.children || []).forEach(sub => {
      links.push({
        source: branch,
        target: sub,
        type: 'subbranch',
        color: branch.color || themeConfig.branchColors[i % themeConfig.branchColors.length]
      });
    });
  });

  // Draw links (curved paths)
  g.selectAll('.link')
    .data(links)
    .enter()
    .append('path')
    .attr('class', 'link')
    .attr('d', d => generateCurvedPath(d.source, d.target, d.type))
    .attr('fill', 'none')
    .attr('stroke', d => d.color)
    .attr('stroke-width', d => d.type === 'branch' ? 4 : 2.5)
    .attr('opacity', themeConfig.linkOpacity)
    .attr('stroke-linecap', 'round');

  // Draw subbranch nodes
  branches.forEach((branch, i) => {
    const color = branch.color || themeConfig.branchColors[i % themeConfig.branchColors.length];

    (branch.children || []).forEach(sub => {
      const subGroup = g.append('g')
        .attr('class', 'subbranch-node')
        .attr('transform', `translate(${sub.x}, ${sub.y})`);

      // Node background (rounded rectangle)
      const textLength = sub.name.length;
      const nodeWidth = Math.max(100, textLength * 8 + 30);
      const nodeHeight = 40;

      subGroup.append('rect')
        .attr('x', -nodeWidth / 2)
        .attr('y', -nodeHeight / 2)
        .attr('width', nodeWidth)
        .attr('height', nodeHeight)
        .attr('rx', 20)
        .attr('ry', 20)
        .attr('fill', d3.color(color).darker(0.8))
        .attr('stroke', color)
        .attr('stroke-width', 2)
        .attr('filter', 'url(#drop-shadow)');

      // Node text
      subGroup.append('text')
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .attr('fill', themeConfig.textColor)
        .attr('font-family', 'Inter, system-ui, -apple-system, sans-serif')
        .attr('font-size', CONFIG.subbranchNode.fontSize)
        .attr('font-weight', CONFIG.subbranchNode.fontWeight)
        .text(sub.name);
    });
  });

  // Draw branch nodes
  branches.forEach((branch, i) => {
    const color = branch.color || themeConfig.branchColors[i % themeConfig.branchColors.length];

    const branchGroup = g.append('g')
      .attr('class', 'branch-node')
      .attr('transform', `translate(${branch.x}, ${branch.y})`);

    // Create gradient for this branch
    const branchGradient = defs.append('linearGradient')
      .attr('id', `branch-gradient-${i}`)
      .attr('x1', '0%')
      .attr('y1', '0%')
      .attr('x2', '100%')
      .attr('y2', '100%');

    branchGradient.append('stop')
      .attr('offset', '0%')
      .attr('stop-color', color);
    branchGradient.append('stop')
      .attr('offset', '100%')
      .attr('stop-color', d3.color(color).darker(0.5));

    // Node background (rounded rectangle)
    const textLength = branch.name.length;
    const nodeWidth = Math.max(120, textLength * 9 + 40);
    const nodeHeight = 50;

    branchGroup.append('rect')
      .attr('x', -nodeWidth / 2)
      .attr('y', -nodeHeight / 2)
      .attr('width', nodeWidth)
      .attr('height', nodeHeight)
      .attr('rx', 25)
      .attr('ry', 25)
      .attr('fill', `url(#branch-gradient-${i})`)
      .attr('stroke', '#ffffff')
      .attr('stroke-width', 2)
      .attr('filter', 'url(#drop-shadow)');

    // Node text
    branchGroup.append('text')
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('fill', themeConfig.textColor)
      .attr('font-family', 'Inter, system-ui, -apple-system, sans-serif')
      .attr('font-size', CONFIG.branchNode.fontSize)
      .attr('font-weight', CONFIG.branchNode.fontWeight)
      .text(branch.name);
  });

  // Draw center node (on top)
  const centerGroup = g.append('g')
    .attr('class', 'center-node')
    .attr('transform', `translate(${hierarchy.x}, ${hierarchy.y})`);

  // Center node shadow/glow
  centerGroup.append('ellipse')
    .attr('rx', CONFIG.centerNode.radius + 10)
    .attr('ry', CONFIG.centerNode.radius * 0.6 + 10)
    .attr('fill', themeConfig.centerGradient[0])
    .attr('opacity', 0.2)
    .attr('filter', 'url(#glow)');

  // Center node background
  const titleLength = hierarchy.name.length;
  const centerWidth = Math.max(200, titleLength * 11 + 60);
  const centerHeight = 80;

  centerGroup.append('rect')
    .attr('x', -centerWidth / 2)
    .attr('y', -centerHeight / 2)
    .attr('width', centerWidth)
    .attr('height', centerHeight)
    .attr('rx', 40)
    .attr('ry', 40)
    .attr('fill', 'url(#center-gradient)')
    .attr('stroke', '#ffffff')
    .attr('stroke-width', 3)
    .attr('filter', 'url(#drop-shadow)');

  // Center node text (with word wrap for long titles)
  const words = hierarchy.name.split(' ');
  const maxCharsPerLine = 25;
  const lines = [];
  let currentLine = '';

  words.forEach(word => {
    if ((currentLine + ' ' + word).trim().length <= maxCharsPerLine) {
      currentLine = (currentLine + ' ' + word).trim();
    } else {
      if (currentLine) lines.push(currentLine);
      currentLine = word;
    }
  });
  if (currentLine) lines.push(currentLine);

  const lineHeight = 26;
  const startY = -((lines.length - 1) * lineHeight) / 2;

  lines.forEach((line, i) => {
    centerGroup.append('text')
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('y', startY + i * lineHeight)
      .attr('fill', themeConfig.textColor)
      .attr('font-family', 'Inter, system-ui, -apple-system, sans-serif')
      .attr('font-size', CONFIG.centerNode.fontSize)
      .attr('font-weight', CONFIG.centerNode.fontWeight)
      .text(line);
  });

  return svg.node().outerHTML;
}

/**
 * Render SVG to PNG using Puppeteer
 */
async function renderToPNG(svgContent, outputPath, width, height) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height });

  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          * { margin: 0; padding: 0; }
          body { width: ${width}px; height: ${height}px; overflow: hidden; }
          svg { display: block; }
        </style>
      </head>
      <body>${svgContent}</body>
    </html>
  `;

  await page.setContent(html);
  await page.screenshot({ path: outputPath, type: 'png' });
  await browser.close();
}

/**
 * Main render function
 */
async function renderMindmap(inputPath, outputDir, options = {}) {
  const {
    theme = 'modern',
    width = CONFIG.width,
    height = CONFIG.height,
    formats = ['svg', 'png']
  } = options;

  // Read input structure
  const structure = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));

  // Generate SVG
  const svgContent = createMindmapSVG(structure, { width, height, theme });

  // Create output directory if needed
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const baseName = path.basename(inputPath, '.json');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const outputBaseName = `${baseName}_${timestamp}`;

  const results = {};

  // Save SVG
  if (formats.includes('svg')) {
    const svgPath = path.join(outputDir, `${outputBaseName}.svg`);
    fs.writeFileSync(svgPath, svgContent);
    results.svg = svgPath;
    console.log(`SVG saved: ${svgPath}`);
  }

  // Render PNG
  if (formats.includes('png')) {
    const pngPath = path.join(outputDir, `${outputBaseName}.png`);
    await renderToPNG(svgContent, pngPath, width, height);
    results.png = pngPath;
    console.log(`PNG saved: ${pngPath}`);
  }

  return results;
}

// CLI interface
async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log('Usage: node render.js <input.json> [output_dir] [--theme=modern|light|vibrant|minimal] [--width=1920] [--height=1080]');
    console.log('\nExample: node render.js mindmap_structure.json ./output --theme=vibrant');
    process.exit(1);
  }

  const inputPath = args[0];
  const outputDir = args[1] || './output';

  // Parse options
  const options = {
    theme: 'modern',
    width: 1920,
    height: 1080,
    formats: ['svg', 'png']
  };

  args.slice(2).forEach(arg => {
    if (arg.startsWith('--theme=')) {
      options.theme = arg.split('=')[1];
    } else if (arg.startsWith('--width=')) {
      options.width = parseInt(arg.split('=')[1]);
    } else if (arg.startsWith('--height=')) {
      options.height = parseInt(arg.split('=')[1]);
    } else if (arg.startsWith('--format=')) {
      options.formats = arg.split('=')[1].split(',');
    }
  });

  try {
    const results = await renderMindmap(inputPath, outputDir, options);
    console.log('\nRender complete!');
    console.log(JSON.stringify(results, null, 2));
  } catch (error) {
    console.error('Error rendering mindmap:', error);
    process.exit(1);
  }
}

// Export for use as module
export { createMindmapSVG, renderMindmap, renderToPNG, THEMES };

// Run if called directly
main();
