#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版 Remotion 视频生成演示器
无需复杂配置，直接展示原理和输出示例
"""

import json
from pathlib import Path
from datetime import datetime


def create_simple_demo(concept: str, key_points: list):
    """创建一个简单的 Remotion 项目演示"""
    
    output_dir = Path("/tmp/knowledge-remotion-demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 README 说明
    readme_content = f'''# 🎬 Remotion 知识视频生成示例

## 📚 概念：{concept}

## ✨ 核心要点 ({len(key_points)} 个)
'''
    for i, point in enumerate(key_points, 1):
        readme_content += f"\n{i}. {point}"
    
    readme_content += "\n\n## 🎯 视频结构规划\n"
    readme_content += "```\n"
    readme_content += "┌─────────────────────┐\n"
    readme_content += f"│ 0-10s: 开场动画     │ → 显示概念标题 {concept}\n"
    readme_content += "├─────────────────────┤\n"
    
    for i, point in enumerate(key_points[:3], 1):
        start = 10 + (i-1) * 15
        end = start + 15
        readme_content += f"│ {start:2d}-{end:2d}s: 要点{i}展示   │ → {point[:30]}...\n"
    
    readme_content += "├─────────────────────┤\n"
    readme_content += "│ 最后 10s: 总结记忆点 │ → 核心口诀\n"
    readme_content += "└─────────────────────┘\n"
    readme_content += f"```\n\n总时长：约 {(len(key_points)+2) * 15}秒\n"
    
    # 保存文件
    readme_path = output_dir / "VIDEO_DEMO.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return str(readme_path)


def generate_react_component(concept: str, points: list) -> str:
    """生成 React 组件代码示例"""
    
    component_code = '''// Remotion Knowledge Video Component
import React from "react";
import { AbsoluteFill, Sequence, Text, Opacity, ZoomIn } from "@remotion/react";

// 颜色主题
const COLORS = {
  background: "#1a1a2e",
  primary: "#e94560",
  secondary: "#0f3460",
  text: "#ffffff"
};

export const KnowledgeVideo = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      {/* 开场场景 */}
      <Sequence from={0}>
        <Opacity from={0} to={1}>
          <Text
            fontSize="80"
            fontWeight="bold"
            color={COLORS.text}
            origin="center"
            x="50%"
            y="30%"
          >
            📚 {CONCEPT}
          </Text>
        </Opacity>
      </Sequence>

      {/* 核心要点展示 */}
      <Sequence from={60}>
        {KEY_POINTS.map((point, index) => (
          <Sequence key={index} from={index * 80}>
            <Opacity from={0} to={1}>
              <Text
                fontSize="40"
                color={COLORS.secondary}
                origin="left"
                x="10%"
                y={(50 + index * 12) + "%"}
              >
                • {point}
              </Text>
            </Opacity>
          </Sequence>
        ))}
      </Sequence>

      {/* 总结场景 */}
      <Sequence from={480}>
        <ZoomIn from={1} to={1.2}>
          <Text
            fontSize="50"
            fontWeight="bold"
            color={COLORS.primary}
            origin="center"
            x="50%"
            y="70%"
          >
            💡 一句话记住这个概念！
          </Text>
        </ZoomIn>
      </Sequence>
    </AbsoluteFill>
  );
};
'''
    
    # 替换占位符
    component_code = component_code.replace("{CONCEPT}", concept[:20])
    component_code = component_code.replace("{KEY_POINTS}", json.dumps(points, ensure_ascii=False))
    
    return component_code


def demo_video_generation():
    """演示视频生成流程"""
    
    print("\n" + "="*70)
    print("🎬 Remotion 知识视频生成演示")
    print("="*70)
    
    # 示例数据
    concept = "Agent vs Skill"
    key_points = [
        "Agent 能独立决策",
        "Skill 需要被调用",
        "Agent 是 CEO，Skill 是工具",
        "一个 Agent 可以用多个 Skills",
        "Skills 可以被其他 Agent 复用"
    ]
    
    print(f"\n📚 概念：{concept}")
    print(f"✨ 核心要点：{len(key_points)}个\n")
    
    # 步骤 1: 生成项目文件
    print("📝 步骤 1: 生成 Remotion 组件...")
    component_code = generate_react_component(concept, key_points)
    
    component_path = Path("/tmp/knowledge-remotion-demo/AgentVideo.tsx")
    component_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(component_path, 'w', encoding='utf-8') as f:
        f.write(component_code)
    
    print(f"✅ 组件已保存：{component_path}")
    
    # 步骤 2: 生成演示文档
    print("\n📋 步骤 2: 生成视频结构说明...")
    readme_path = create_simple_demo(concept, key_points)
    print(f"✅ 说明文档已保存：{readme_path}")
    
    # 步骤 3: 显示生成的组件代码
    print("\n🎨 步骤 3: React 组件预览:")
    print("-" * 70)
    print(component_code[:800] + "...")
    print("-" * 70)
    
    # 步骤 4: 显示使用命令
    print("\n⚙️ 步骤 4: 运行 Remotion 生成视频的命令:")
    print("```bash")
    print("cd /tmp/knowledge-remotion-demo")
    print("npm init -y")
    print("npm install @remotion/react")
    print("npx remotion render AgentVideo -o agent_video.mp4")
    print("```")
    
    # 步骤 5: 显示输出预览
    print("\n📊 预期视频结构:")
    print(readme_path)
    print("")
    
    return {
        'concept': concept,
        'component': str(component_path),
        'readme': readme_path,
        'status': 'success'
    }


if __name__ == '__main__':
    result = demo_video_generation()
    
    print("\n" + "="*70)
    print("✅ Remotion 演示完成！")
    print("="*70)
    print(f"\n📁 生成的文件:")
    print(f"   • React 组件：{result['component']}")
    print(f"   • 结构说明：{result['readme']}")
    print(f"\n💡 下一步:")
    print(f"   1. 安装 Node.js (如果尚未安装)")
    print(f"   2. 运行 'npm install @remotion/react'")
    print(f"   3. 执行 'npx remotion render ...' 生成视频")
    print(f"\n🎥 视频将包含:")
    print(f"   • 开场动画 (10 秒)")
    print(f"   • {len([i for i in dir() if not i.startswith('_')])}个要点展示")
    print(f"   • 总结记忆点 (10 秒)")
    print(f"\n📚 更多 Remotion 文档：https://www.remotion.dev/")
