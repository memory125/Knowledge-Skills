/**
 * Puppeteer WebGL Video Renderer for Knowledge Explainer
 * 
 * 使用 Puppeteer + HTML5 Canvas/WebGL渲染高质量教学视频帧，
 * 然后通过 FFmpeg 合成最终视频。
 */

import puppeteer, { Page } from 'puppeteer';
import fs from 'fs-extra';
import path from 'path';

export interface VideoScene {
  sceneId: number;
  text: string;
  subtitle?: string;
  color: string;
  durationSec: number;
}

export interface RenderConfig {
  scenes: VideoScene[];
  outputDir: string;
  width: number;
  height: number;
  fps: number;
}

/**
 * Generate a single frame using Puppeteer + Canvas
 */
async function generateFrame(
  scene: VideoScene,
  progress: number,
  width: number,
  height: number,
  outputPath: string,
  page: Page
): Promise<void> {
  // Create HTML with Canvas for rendering
  const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { margin: 0; padding: 0; overflow: hidden; }
    canvas { display: block; }
  </style>
</head>
<body>
  <canvas id="canvas" width="${width}" height="${height}"></canvas>
  <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    
    // Scene data
    const scene = ${JSON.stringify(scene)};
    const progress = ${progress};
    
    // Create gradient background
    const gradient = ctx.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, scene.color);
    gradient.addColorStop(1, adjustBrightness(scene.color, -30));
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
    
    // Add animated geometric shapes based on progress
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.3 * (0.5 + progress * 0.5);
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.fill();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Add text
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Title text
    ctx.font = 'bold ${Math.floor(height * 0.12)}px "Noto Sans CJK", sans-serif';
    const textLines = wrapText(ctx, scene.text, width * 0.8);
    textLines.forEach((line, index) => {
      ctx.fillText(line, centerX, centerY - (textLines.length - 1) * height * 0.06 / 2 + index * height * 0.06);
    });
    
    // Subtitle if exists
    if (scene.subtitle) {
      ctx.font = '${Math.floor(height * 0.07)}px "Noto Sans CJK", sans-serif';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.fillText(scene.subtitle, centerX, centerY + height * 0.15);
    }
    
    // Helper functions
    function adjustBrightness(hex, percent) {
      const num = parseInt(hex.replace('#', ''), 16);
      const amt = Math.round(2.55 * percent);
      const R = Math.min(255, Math.max(0, (num >> 16) + amt));
      const G = Math.min(255, Math.max(0, ((num >> 8) & 0x00FF) + amt));
      const B = Math.min(255, Math.max(0, (num & 0x0000FF) + amt));
      return '#' + (0x1000000 + (R << 16) + (G << 8) + B).toString(16).slice(1);
    }
    
    function wrapText(ctx, text, maxWidth) {
      const words = text.split(' ');
      const lines = [];
      let currentLine = words[0];
      
      for (let i = 1; i < words.length; i++) {
        const word = words[i];
        const width = ctx.measureText(currentLine + ' ' + word).width;
        
        if (width > maxWidth && lines.length > 0) {
          lines.push(currentLine);
          currentLine = word;
        } else {
          currentLine += ' ' + word;
        }
      }
      
      lines.push(currentLine);
      return lines;
    }
  </script>
</body>
</html>
  `;

  await page.setContent(html, { waitUntil: 'networkidle0' });
  
  // Wait for canvas to render
  await page.waitForFunction(() => {
    const canvas = document.getElementById('canvas') as HTMLCanvasElement;
    return canvas.width > 0 && canvas.height > 0;
  });
  
  // Capture screenshot
  await page.screenshot({ path: outputPath, fullPage: false });
}

/**
 * Generate all frames for the video
 */
export async function renderVideo(config: RenderConfig): Promise<string> {
  const { scenes, outputDir, width = 1920, height = 1080, fps = 30 } = config;
  
  await fs.ensureDir(outputDir);
  const framesDir = path.join(outputDir, 'frames');
  await fs.ensureDir(framesDir);
  
  console.log(`🎬 Puppeteer WebGL Rendering Started`);
  console.log(`   Resolution: ${width}x${height}`);
  console.log(`   Scenes: ${scenes.length}`);
  console.log(`   FPS: ${fps}`);
  
  // Launch browser with optimized settings
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu-sandbox',
      '--disable-webgl-draft-extensions'
    ]
  });
  
  const page = await browser.newPage();
  
  // Set viewport size
  await page.setViewport({ width, height, deviceScaleFactor: 2 });
  
  try {
    let frameIndex = 0;
    
    for (const scene of scenes) {
      const totalFrames = Math.floor(scene.durationSec * fps);
      
      console.log(`\n📝 Scene ${scene.sceneId}: "${scene.text.substring(0, 40)}..."`);
      console.log(`   Duration: ${scene.durationSec}s (${totalFrames} frames)`);
      
      for (let i = 0; i < totalFrames; i++) {
        const progress = i / totalFrames;
        const outputPath = path.join(framesDir, `frame_${String(frameIndex).padStart(6, '0')}.png`);
        
        await generateFrame(scene, progress, width, height, outputPath, page);
        
        frameIndex++;
        
        if (frameIndex % 100 === 0) {
          console.log(`   Generated ${frameIndex} frames...`);
        }
      }
    }
    
    console.log(`\n✅ Generated ${frameIndex} frames total`);
    
    // Stitch frames into video using FFmpeg
    const outputPath = path.join(outputDir, 'output.mp4');
    
    await stitchVideo(framesDir, outputPath, fps);
    
    console.log(`✅ Video rendered: ${outputPath}`);
    
    // Cleanup frames
    console.log(`🧹 Cleaning up frames...`);
    await fs.remove(framesDir);
    
    return outputPath;
    
  } finally {
    await browser.close();
  }
}

/**
 * Stitch frames into video using FFmpeg
 */
async function stitchVideo(framesDir: string, outputPath: string, fps: number): Promise<void> {
  return new Promise((resolve, reject) => {
    const { exec } = require('child_process');
    
    const framePattern = path.resolve(framesDir, 'frame_%06d.png');
    const ffmpegCmd = `ffmpeg -y -framerate ${fps} -i "${framePattern}" -c:v libx264 -pix_fmt yuv420p -crf 23 -preset medium "${outputPath}"`;
    
    console.log('🎥 Stitching video with FFmpeg...');
    
    const process = exec(ffmpegCmd);
    
    process.stderr?.on('data', (data: any) => {
      // Progress output
      const progressMatch = data.toString().match(/time=(\d+):(\d+):(\d+)/);
      if (progressMatch) {
        console.log(`   FFmpeg progress: ${progressMatch[1]}:${progressMatch[2]}:${progressMatch[3]}`);
      }
    });
    
    process.on('close', (code: number) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`FFmpeg failed with code ${code}`));
      }
    });
    
    process.on('error', reject);
  });
}

export default { renderVideo };
