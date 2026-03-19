#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puppeteer WebGL Video Renderer Wrapper for Knowledge Explainer

调用 TypeScript Puppeteer 渲染器生成视频。
需要：Node.js >= 16, npm, puppeteer
"""

import subprocess
import sys
import os
from typing import List, Dict, Any


def compile_typescript():
    """编译 TypeScript 渲染器"""
    print("🔧 Compiling Puppeteer renderer...")
    
    try:
        # Check if dist folder exists and has the compiled JS
        dist_path = "generators/video_renderer_puppeteer.js"
        if not os.path.exists(dist_path):
            # Compile TypeScript
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd="generators",
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"⚠️ TypeScript compilation failed, trying direct tsc...")
                # Try direct tsc command
                subprocess.run(
                    ["tsc", "video_renderer_puppeteer.ts"],
                    cwd="generators",
                    capture_output=True
                )
        
        return True
    except Exception as e:
        print(f"❌ Failed to compile TypeScript: {e}")
        return False


def generate_video_with_puppeteer(
    scenes: List[Dict[str, Any]],
    output_path: str,
    width: int = 1920,
    height: int = 1080,
    fps: int = 30
):
    """
    使用 Puppeteer 渲染视频
    
    Args:
        scenes: 场景列表，每个场景包含 sceneId, text, subtitle, color, durationSec
        output_path: 输出视频路径
        width: 视频宽度
        height: 视频高度
        fps: 帧率
    """
    
    print(f"🎬 Starting Puppeteer WebGL rendering...")
    print(f"   Scenes: {len(scenes)}")
    print(f"   Resolution: {width}x{height}")
    print(f"   Output: {output_path}")
    
    try:
        # Create output directory
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Prepare scenes data for Node.js
        import json
        
        node_script = """
const fs = require('fs');
const path = require('path');

async function main() {
    const { renderVideo } = require('./video_renderer_puppeteer.js');
    
    const config = JSON.parse(fs.readFileSync('temp_render_config.json', 'utf-8'));
    
    try {
        const outputPath = await renderVideo(config);
        console.log('SUCCESS:', outputPath);
        process.exit(0);
    } catch (error) {
        console.error('ERROR:', error.message);
        process.exit(1);
    }
}

main();
"""
        
        # Write temporary config file
        config = {
            'scenes': scenes,
            'outputDir': os.path.dirname(output_path),
            'width': width,
            'height': height,
            'fps': fps
        }
        
        with open('temp_render_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False)
        
        # Write temporary Node.js script
        with open('temp_renderer_runner.js', 'w') as f:
            f.write(node_script)
        
        # Execute Node.js script
        result = subprocess.run(
            ['node', 'temp_renderer_runner.js'],
            cwd='generators',
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes timeout
        )
        
        # Cleanup temporary files
        try:
            os.remove('temp_render_config.json')
            os.remove('temp_renderer_runner.js')
        except:
            pass
        
        if result.returncode == 0:
            print(f"✅ Video generated successfully: {output_path}")
            return True
        else:
            print(f"❌ Puppeteer rendering failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Rendering timed out after 10 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running Puppeteer renderer: {e}")
        return False


if __name__ == "__main__":
    # Example usage
    test_scenes = [
        {
            'sceneId': 1,
            'text': '测试标题',
            'subtitle': '这是测试副标题',
            'color': '#1a1a2e',
            'durationSec': 5
        },
        {
            'sceneId': 2,
            'text': '第二个场景',
            'subtitle': '更多内容',
            'color': '#0f3460',
            'durationSec': 5
        }
    ]
    
    # Compile TypeScript first
    if not compile_typescript():
        print("❌ Failed to compile TypeScript, cannot continue")
        sys.exit(1)
    
    # Generate video
    success = generate_video_with_puppeteer(
        test_scenes,
        'output/puppeteer_test.mp4'
    )
    
    if success:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed")
        sys.exit(1)
