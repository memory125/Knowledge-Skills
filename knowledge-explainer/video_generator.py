#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Explainer Video Generator - 基于 Remotion 的视频生成模块
将文字解释自动转化为教学视频
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class RemotionVideoGenerator:
    """使用 Remotion 生成知识教学视频"""
    
    def __init__(self, output_dir: str = "/tmp/knowledge-videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Remotion 项目目录
        self.remotion_project = self.output_dir / "remotion-project"
        
    def setup_remotion_project(self):
        """初始化 Remotion 项目（首次运行需要）"""
        
        if (self.remotion_project / "package.json").exists():
            print("✓ Remotion 项目已存在")
            return True
        
        print("🚀 正在初始化 Remotion 项目...")
        
        try:
            # 创建项目目录
            self.remotion_project.mkdir(parents=True, exist_ok=True)
            
            # 初始化 npm 项目
            subprocess.run(
                ["npm", "init", "-y"],
                cwd=self.remotion_project,
                check=True,
                capture_output=True
            )
            
            # 安装 Remotion
            subprocess.run(
                ["npm", "install", "@remotion/cli", "@remotion/react"],
                cwd=self.remotion_project,
                check=True,
                capture_output=True
            )
            
            print("✅ Remotion 项目初始化完成")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Remotion 初始化失败：{e}")
            return False
    
    def generate_knowledge_video(self, concept: str, explanation_content: str) -> Optional[str]:
        """根据概念和解释内容生成教学视频"""
        
        # 1. 创建 React 组件
        component_path = self._create_remotion_component(concept, explanation_content)
        
        if not component_path:
            return None
        
        # 2. 导出视频
        video_path = self.remotion_project / f"output/{concept.replace(' ', '_')}_video.mp4"
        
        try:
            # 使用 Remotion CLI 导出
            result = subprocess.run(
                [
                    "npx", "remotion", "render",
                    "-o", str(video_path),
                    "KnowledgeVideo",
                    "--duration", "60",
                    "--fps", "30"
                ],
                cwd=self.remotion_project,
                check=True,
                capture_output=True,
                text=True
            )
            
            print(f"✅ 视频生成成功：{video_path}")
            return str(video_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 视频导出失败：{e.stderr}")
            return None
    
    def _create_remotion_component(self, concept: str, explanation_content: str) -> Optional[Path]:
        """创建 Remotion React 组件"""
        
        component_path = self.remotion_project / "KnowledgeVideo.tsx"
        
        # 提取关键信息
        one_line_summary = self._extract_one_liner(explanation_content)
        key_points = self._extract_key_points(explanation_content)
        
        # 生成 React 组件代码
        component_code = f'// Knowledge Video Generator - {concept}\nimport React from "react";\nimport {{ AbsoluteFill, Sequence, Text, Opacity, ZoomIn }} from "@remotion/react";\n\nconst CONCEPT_INFO = JSON.parse(\'{json.dumps({\n            "concept": concept,\n            "summary": one_line_summary,\n            "keyPoints": key_points\n        }, ensure_ascii=False)}\');\n'

// 颜色主题
const COLORS = {{
  background: "#1a1a2e",
  primary: "#e94560",
  secondary: "#0f3460",
  text: "#ffffff",
  accent: "#16213e"
}};

// 开场动画组件
const IntroScene = () => {{
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      <Sequence from={0} durationInFrames={60}>
        <Opacity from={0} to={1} durationInFrames={30}>
          <Text
            fontSize="80"
            fontWeight="bold"
            fontFamily="Arial, sans-serif"
            color={COLORS.text}
            origin="center"
            x="50%"
            y="40%"
          >
            📚 {concept}
          </Text>
        </Opacity>
        
        <Sequence from={60}>
          <Opacity from={0} to={1} durationInFrames={30}>
            <Text
              fontSize="40"
              fontFamily="Arial, sans-serif"
              color={COLORS.primary}
              origin="center"
              x="50%"
              y="60%"
            >
              大白话版解释
            </Text>
          </Opacity>
        </Sequence>
      </Sequence>
    </AbsoluteFill>
  );
}};

// 核心要点展示组件  
const KeyPointsScene = () => {{
  const {{ durationInFrames }} = useVideoConfig();
  
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      <Text
        fontSize="50"
        fontWeight="bold"
        fontFamily="Arial, sans-serif"
        color={COLORS.text}
        origin="center"
        x="50%"
        y="20%"
      >
        🔑 核心要点
      </Text>
      
      {CONCEPT_INFO.keyPoints.map((point, index) => (
        <Sequence 
          key={index} 
          from={120 + index * 80}
          durationInFrames={80}
        >
          <Opacity from={0} to={1}>
            <Text
              fontSize="35"
              fontFamily="Arial, sans-serif"
              color={COLORS.secondary}
              origin="left"
              x="10%"
              y={40 + index * 12 + "%"}
            >
              • {point}
            </Text>
          </Opacity>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
}};

// 总结场景
const SummaryScene = () => {{
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.primary }}>
      <Sequence from={0}>
        <ZoomIn from={1} to={1.2} durationInFrames={60}>
          <Text
            fontSize="45"
            fontWeight="bold"
            fontFamily="Arial, sans-serif"
            color={COLORS.text}
            origin="center"
            x="50%"
            y="50%"
          >
            💡 {one_line_summary}
          </Text>
        </ZoomIn>
      </Sequence>
    </AbsoluteFill>
  );
}};

// 主视频组件
export const KnowledgeVideo: React.FC = () => {{
  return (
    <>
      <Sequence from={0}>
        <IntroScene />
      </Sequence>
      
      <Sequence from={180}>
        <KeyPointsScene />
      </Sequence>
      
      <Sequence from={600}>
        <SummaryScene />
      </Sequence>
    </>
  );
}};
'''
        
        try:
            with open(component_path, 'w', encoding='utf-8') as f:
                f.write(component_code)
            
            print(f"✓ React 组件已创建：{component_path}")
            return component_path
            
        except Exception as e:
            print(f"❌ 创建组件失败：{e}")
            return None
    
    def _extract_one_liner(self, content: str) -> str:
        """从内容中提取一句话总结"""
        
        import re
        
        # 寻找 "一句话总结" 或类似标记
        patterns = [
            r'💡\s*一句话总结[::：]\s*(.+?)(?:\n|-{3,})',
            r'**💡\s*一句话总结**:\s*(.+?)(?:\n|-{3,})',
            r'summary.*[:：]\s*(.+?)(?:\n|-{3,})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:100]  # 限制长度
        
        return "这个概念的核心要点是简单易懂"
    
    def _extract_key_points(self, content: str) -> List[str]:
        """提取核心要点（最多 5 个）"""
        
        import re
        
        points = []
        
        # 寻找要点列表
        patterns = [
            r'[•✦●]\s*(.+?)(?:\n|$)',
            r'\d+\.\s*(.+?)(?:\n|$)',
            r'**([^*]+)**:\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches[:5]:
                if isinstance(match, tuple):
                    point = f"{match[0]}: {match[1]}"
                else:
                    point = match
                
                point = point.strip()
                if point and len(point) > 5 and len(point) < 200:
                    points.append(point)
            
            if len(points) >= 5:
                break
        
        return points if points else ["要点 1", "要点 2", "要点 3"]


# 集成到 Knowledge Explainer
def integrate_video_generation(explainer_class):
    """将视频生成功能集成到 KnowledgeExplainer"""
    
    original_init = explainer_class.__init__
    
    def new_init(self, query: str, enable_extensions: List[str] = None):
        original_init(self, query, enable_extensions)
        self.video_generator = RemotionVideoGenerator()
    
    explainer_class.__init__ = new_init
    
    def generate_knowledge_video(self, concept: str, explanation: str, output_file: str = None) -> Optional[str]:
        """生成知识教学视频"""
        
        if 'video' not in (self.enabled_extensions or []):
            print("⚠️ 视频生成功能未启用")
            return None
        
        # 检查 Node.js 环境
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Node.js 未安装，无法生成视频")
                print("请运行：curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs")
                return None
        except FileNotFoundError:
            print("❌ Node.js 未找到")
            return None
        
        # 初始化 Remotion 项目
        if not self.video_generator.setup_remotion_project():
            return None
        
        # 生成视频
        video_path = self.video_generator.generate_knowledge_video(concept, explanation)
        
        if video_path and output_file:
            import shutil
            shutil.copy(video_path, output_file)
            return output_file
        
        return video_path
    
    explainer_class.generate_knowledge_video = generate_knowledge_video


# 示例使用
if __name__ == '__main__':
    print("=== Knowledge Video Generator Demo ===\n")
    
    generator = RemotionVideoGenerator()
    
    # 测试数据
    test_concept = "区块链"
    test_content = """
    # 📚 区块链（大白话版）
    
    > 💡 **一句话总结**: 全班同学共同记账，没人能改别人的账
    
    ## 🔑 核心要点
    1. 公开透明 - 所有人能看到所有交易
    2. 不可篡改 - 一旦写入就改不了
    3. 共同维护 - 靠数学而不是人治
    """
    
    # 测试组件生成
    component = generator._create_remotion_component(test_concept, test_content)
    
    if component:
        print(f"✅ React 组件已创建")
        print(f"📁 位置：{component}")
        print("\n💡 下一步:")
        print("1. 安装 Node.js 和 npm")
        print("2. 运行：npm install")
        print("3. 生成视频：npx remotion render KnowledgeVideo -o output.mp4")
    else:
        print("❌ 组件创建失败")
