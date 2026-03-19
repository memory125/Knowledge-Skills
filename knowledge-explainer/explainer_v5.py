#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Explainer v5.0 - 知识通俗解释器（语音增强版）

核心特性：
1. 大白话翻译 - 专业术语 → 生活化语言
2. 视觉化解释 - ASCII/Mermaid 图表 + 概念图
3. 类比系统 - 多维度生活比喻
4. 视频生成 - 自动生成教学视频（Python+Pillow+FFmpeg）
5. 语音解说 ✨ NEW! - edgetts TTS 旁白（中文完美支持）
6. 字幕生成 ✨ NEW! - 自动同步字幕轨道
7. 分层学习 - 一句话/一分钟/深度解析

作者：OpenClaw AI Team
版本：5.0 (集成语音 + 字幕)
日期：2026-03-09
"""

import json
import os
import subprocess
import tempfile
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class VoiceConfig:
    """语音配置"""
    voice: str = "zh-CN-XiaoxiaoNeural"  # 默认女声 - 温暖专业
    rate: int = 0  # 语速 % (-100~+100)
    volume: int = 0  # 音量 % (-100~+100)
    pitch: int = 0  # 音调 Hz (-100~+100)


@dataclass
class ExplainerConfig:
    """解释器配置"""
    depth_level: int = 2  # 1=一句话，2=生活化，3=可视化，4=深度解析
    include_visuals: bool = True  # 是否包含可视化图表
    include_analogies: bool = True  # 是否包含生活类比
    output_format: str = "markdown"  # markdown, json, text
    generate_video: bool = False  # 是否生成教学视频
    voice_config: VoiceConfig = None  # 语音配置（v5.0 NEW）
    generate_audio: bool = True  # 是否生成音频轨道（v5.0 NEW）
    generate_subtitles: bool = True  # 是否生成字幕（v5.0 NEW）
    use_ollama: bool = False  # 是否使用 Ollama 生成解说词（v5.1 NEW）
    use_remotion: bool = False  # 是否使用 Remotion 渲染（v5.4, default=False）
    use_puppeteer: bool = False  # 是否使用 Puppeteer WebGL 渲染（v5.5, default=False）


class KnowledgeExplainerV5:
    """知识通俗解释器 v5.0"""

    def __init__(self, config: Optional[ExplainerConfig] = None):
        self.config = config or ExplainerConfig(voice_config=VoiceConfig())
        
    def explain(self, topic: str) -> str:
        """
        解释一个概念/术语/问题
        
        Args:
            topic: 要解释的主题
            
        Returns:
            通俗易懂的解释（markdown 格式）
        """
        # 生成大白话解释
        explanation = self._generate_explanation(topic)
        
        # 根据配置添加不同层级的内容
        if self.config.depth_level >= 2 and self.config.include_analogies:
            explanation += self._generate_analogies(topic)
            
        if self.config.depth_level >= 3 and self.config.include_visuals:
            explanation += self._generate_visuals(topic)
            
        if self.config.depth_level >= 4:
            explanation += self._generate_deep_dive(topic)
        
        # 生成教学视频 + 语音（v5.0 NEW）✨
        if self.config.generate_video:
            video_path = self._generate_video_with_audio(topic)
            if video_path:
                explanation += f"\n\n📹 **已生成教学视频**: `{video_path}`\n"
        
        # 仅生成音频（v5.0 NEW）✨
        if hasattr(self.config, 'audio_only') and self.config.audio_only:
            audio_path = self._generate_audio_only(topic)
            if audio_path:
                explanation += f"\n\n🎧 **已生成纯音频**: `{audio_path}`\n"
        
        return explanation
    
    def _generate_explanation(self, topic: str) -> str:
        """生成大白话解释"""
        # TODO: 集成 Ollama API 调用生成真实内容
        return f"""# 📚 {topic}（大白话版）

> **"一句话核心要点"**

## 🎯 核心概念

用通俗易懂的语言解释...

## 💡 关键理解

1. **第一点** - 说明
2. **第二点** - 说明  
3. **第三点** - 说明

"""
    
    def _generate_analogies(self, topic: str) -> str:
        """生成生活化类比"""
        return f"""
## 🎭 生活化比喻

### 就像...

[这里用生活场景类比]

### 对比表格

| 传统理解 | {topic} |
|---------|--------|
| ... | ... |

"""
    
    def _generate_visuals(self, topic: str) -> str:
        """生成可视化图表"""
        ascii_art = f"""
    ╔═══════════════════╗
    ║   {topic}         ║
    ╠═══════════════════╣
    ║   核心概念图       ║
    ╚═══════════════════╝
"""
        mermaid = """
```mermaid
graph TD
    A[起点] --> B{决策点}
    B -->|是 | C[结果 1]
    B -->|否 | D[结果 2]
```
"""
        return ascii_art + mermaid
    
    def _generate_deep_dive(self, topic: str) -> str:
        """生成深度解析"""
        return f"""
## 🧠 深度解析

### 技术原理

[这里提供技术细节]

### 实际应用场景

1. **场景一**
2. **场景二**

### 扩展学习

- 相关概念：...
- 推荐资源：...

"""

    def _generate_tts_script(self, topic: str) -> str:
        """
        ✨ v5.0 优化：根据主题动态生成解说词
        
        工作流程：
        1. 优先尝试 Ollama 生成（如果可用）
        2. 回退到预设知识库
        3. 最后使用通用模板
        
        Args:
            topic: 要解释的主题
            
        Returns:
            用于 TTS 的脚本文本
        """
        # 尝试 Ollama 生成（v5.1 新功能）✨
        if hasattr(self.config, 'use_ollama') and self.config.use_ollama:
            ollama_script = self._generate_tts_with_ollama(topic)
            if ollama_script:
                print(f"✅ 使用 Ollama 生成解说词")
                return ollama_script
        
        # 回退：预设的知识库（与视频画面精确匹配）
        scripts = {
            "费曼学习法": """费曼学习法，用教别人的方式学会知识。

第一步：选目标，确定要学习的概念或主题。

第二步：教别人，假装给初学者讲解。

第三步：查漏洞，卡住了就去查资料。

第四步：简化语言，去掉术语用大白话。

记住核心：真正懂的东西，一定能用大白话讲出来！""",
            
            "量子力学": """
量子力学是描述微观世界物理规律的学科，颠覆了我们对现实的传统认知。

首先，微观粒子具有波粒二象性，既像波又像粒子，取决于你如何观测它。

其次，海森堡不确定性原理告诉我们，无法同时精确知道粒子的位置和动量。

第三，薛定谔的猫这个思想实验展示了量子叠加态——猫可以同时处于生死两种状态。

第四，当进行观测时，波函数会坍缩，系统从多种可能变为确定的一种状态。

最后，量子纠缠现象表明，两个粒子可以瞬间相互影响，即使相隔光年之遥。

这些特性共同构成了我们理解微观世界的基础框架。
            """,
            
            "区块链": """
区块链是一种去中心化的公共账本技术，彻底改变了信任机制。

首先，传统方式中只有银行能记账，而区块链让每个人都能参与记账。

其次，账本不是存在保险柜里，而是在全网所有节点上复制存储。

第三，修改记录需要数学证明和大多数人同意，单个人无法篡改。

第四，每个区块都包含前一个区块的哈希值，形成不可断裂的链条。

最后，这种设计实现了去信任化，靠代码规则而不是人来保障安全。

这就是为什么区块链能用于数字货币、供应链追踪等重要场景。
            """,
            
            "机器学习": """
机器学习是让计算机从数据中学习规律的学科，是人工智能的核心。

首先，传统编程是告诉计算机规则，而机器学习是让它自己发现规律。

其次，监督学习需要标注好的训练数据，比如图片配标签来识别物体。

第三，无监督学习则让算法自己发现数据中的模式和聚类结构。

第四，深度学习使用多层神经网络，能处理图像、语音等复杂任务。

最后，模型通过不断调整参数来最小化预测误差，越训练越准确。

这就是现代 AI 能够人脸识别、自动翻译、智能推荐的技术基础。
            """,
            
            "相对论": """
相对论是爱因斯坦提出的革命性理论，改变了我们对时空的理解。

首先，狭义相对论指出时间和空间不是绝对的，而是相对的。

其次，光速是宇宙中的绝对速度极限，任何有质量的物体都无法超越。

第三，时间膨胀效应表明，高速运动的时钟会变慢，GPS 卫星必须修正这个效应。

第四，质能方程 E 等于 MC 平方告诉我们质量和能量可以相互转化。

最后，广义相对论进一步说明引力是时空弯曲的结果，而不是传统意义上的力。

这些理论已被无数实验验证，是现代物理学的基石。
            """,
        }
        
        # 如果 topic 在知识库中，返回对应脚本
        if topic in scripts:
            return scripts[topic].strip()
        
        # 默认通用模板（当 Ollama 失败且 topic 不在知识库中）
        return f"""{topic}是一个重要的概念或技术。

首先，我们需要理解它的基本定义和核心思想。

其次，它的关键特性和工作原理是学习的重点。

第三，这个概念在实际生活中有广泛应用场景。

第四，与其他相关概念对比可以更清晰把握其特点。

最后，掌握核心要点形成记忆口诀便于应用。""".strip()

    def _generate_tts_with_ollama(self, topic: str) -> Optional[str]:
        """
        ✨ v5.1 新功能：使用 Ollama 自动生成解说词
        
        Args:
            topic: 要解释的主题
            
        Returns:
            Ollama 生成的脚本，失败返回 None
        """
        try:
            # 导入本地 Ollama 生成器模块
            skill_dir = os.path.dirname(os.path.abspath(__file__))
            ollama_path = os.path.join(skill_dir, "ollama_generator.py")
            
            if not os.path.exists(ollama_path):
                print(f"⚠️ Ollama 生成器未找到：{ollama_path}")
                return None
            
            # 动态导入优化版模块（v2.0）
            import sys
            sys.path.insert(0, skill_dir)
            from ollama_generator_optimized import generate_tts_script_optimized as ollama_generate
            
            # 调用 Ollama 生成解说词
            script = ollama_generate(topic)
            
            if script:
                return script.strip()
            else:
                print("⚠️ Ollama 生成失败，回退到预设脚本")
                return None
                
        except Exception as e:
            print(f"⚠️ Ollama 集成异常：{e}")
            return None

    def _generate_tts_audio(self, text: str, output_path: str) -> bool:
        """
        ✨ v5.0 NEW! 使用 edge-tts 生成语音音频
        
        Args:
            text: 要合成语音的文本
            output_path: 输出文件路径
            
        Returns:
            成功返回 True，失败返回 False
        """
        cmd = [
            "edge-tts",
            "-t", text,
            "-v", self.config.voice_config.voice,
            "--write-media", output_path
        ]
        
        # 添加可选参数
        if self.config.voice_config.rate != 0:
            cmd.extend(["--rate", f"{self.config.voice_config.rate}%"])
        if self.config.voice_config.volume != 0:
            cmd.extend(["--volume", f"{self.config.voice_config.volume}%"])
        if self.config.voice_config.pitch != 0:
            cmd.extend(["--pitch", f"{self.config.voice_config.pitch}Hz"])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"⚠️ TTS 失败：{e}")
            return False

    def _generate_scene_subtitles(self, topic: str, output_path: str) -> bool:
        """
        ✨ v5.0 优化：精确到场景的 SRT 字幕生成
        
        视频结构（15 秒 = 450 帧 @30fps）：
        - Scene 1 (0-2.25s):   标题开场
        - Scene 2 (2.25-4.5s): 概念 1
        - Scene 3 (4.5-6.75s): 概念 2
        - Scene 4 (6.75-9s):   概念 3
        - Scene 5 (9-11.25s):  概念 4
        - Scene 6 (11.25-15s): 总结
        
        Returns:
            成功返回 True，失败返回 False
        """
        # 获取解说词分段
        full_script = self._generate_tts_script(topic)
        segments = self._split_script_by_scenes(full_script, topic)
        
        if not segments:
            print(f"⚠️ 无法分割字幕段落")
            return False
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, (start, end, text) in enumerate(segments, 1):
                    # 时间格式转换：秒 → SRT 格式
                    def sec_to_srt(seconds):
                        h = int(seconds // 3600)
                        m = int((seconds % 3600) // 60)
                        s = int(seconds % 60)
                        ms = int((seconds % 1) * 1000)
                        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
                    
                    f.write(f"{i}\n")
                    f.write(f"{sec_to_srt(start)} --> {sec_to_srt(end)}\n")
                    f.write(f"{text}\n\n")
            
            print(f"✅ 字幕生成成功：{output_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ 字幕生成失败：{e}")
            return False
    
    def _split_script_by_scenes(self, script: str, topic: str) -> List[tuple]:
        """
        根据场景分割解说词，返回 [(start_time, end_time, text), ...]
        
        视频时长：15 秒（450 帧 @30fps）
        每个场景：约 2.5 秒（标题 2.25s + 4×概念各 2.25s + 总结 3.75s）
        """
        lines = [line.strip() for line in script.strip().split('\n') if line.strip()]
        
        if not lines:
            return []
        
        # 视频总时长（秒）
        video_duration = 15.0
        
        # 计算每个段落的时长
        scene_duration = video_duration / len(lines)
        
        segments = []
        for i, line in enumerate(lines):
            start_time = i * scene_duration
            end_time = (i + 1) * scene_duration
            
            # 稍微缩短结束时间，避免字幕重叠（留 0.3 秒空白）
            if i < len(lines) - 1:
                end_time -= 0.3
            
            segments.append((start_time, end_time, line))
        
        return segments
    
    def _generate_subtitles(self, segments: List[Dict], output_path: str) -> bool:
        """
        ✨ v5.0 NEW! 生成字幕文件 (SRT 格式) - 保留原始接口
        
        Args:
            segments: [(start_time, end_time, text), ...]
            output_path: 输出文件路径
            
        Returns:
            成功返回 True，失败返回 False
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, (start, end, text) in enumerate(segments, 1):
                    # 时间格式转换：秒 → SRT 格式
                    def sec_to_srt(seconds):
                        h = int(seconds // 3600)
                        m = int((seconds % 3600) // 60)
                        s = int(seconds % 60)
                        ms = int((seconds % 1) * 1000)
                        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
                    
                    f.write(f"{i}\n")
                    f.write(f"{sec_to_srt(start)} --> {sec_to_srt(end)}\n")
                    f.write(f"{text}\n\n")
            return True
        except Exception as e:
            print(f"⚠️ 字幕生成失败：{e}")
            return False

    def _generate_video_with_puppeteer(self, topic: str, output_base: str) -> Optional[str]:
        """
        ✨ v5.5 NEW! 使用 Puppeteer WebGL 渲染引擎生成教学视频
        
        Puppeteer 优势：
        - HTML5 Canvas/WebGL渲染，更高质量视觉效果
        - 支持复杂动画和渐变效果
        - FFmpeg 合成，高兼容性 H.264+AAC 输出
        - 中文支持完善（Noto Sans CJK）
        
        Returns:
            视频文件路径，失败返回 None
        """
        print(f"🎬 Puppeteer WebGL 渲染引擎启动...")
        print(f"   Topic: {topic}")
        print(f"   Output Base: {output_base}")
        
        try:
            # Prepare scenes for video generation
            from knowledge_extractor import KnowledgeExtractor
            extractor = KnowledgeExtractor(self.config.depth, self.config.analogies)
            
            concept_info = extractor.extract_concept(
                self._concept, 
                self._definition, 
                topic, 
                False  # skip detailed text
            )
            
            # Build scenes from knowledge content
            scenes = [
                {
                    'sceneId': 1,
                    'text': f"{topic}",
                    'subtitle': "知识通俗解释",
                    'color': '#1a1a2e',
                    'durationSec': 3
                },
                {
                    'sceneId': 2,
                    'text': concept_info['concept_1']['title'],
                    'subtitle': concept_info['concept_1']['explanation'][:50] + "..." if len(concept_info['concept_1']['explanation']) > 50 else concept_info['concept_1']['explanation'],
                    'color': '#e94560',
                    'durationSec': 4
                },
                {
                    'sceneId': 3,
                    'text': concept_info['concept_2']['title'],
                    'subtitle': concept_info['concept_2']['explanation'][:50] + "..." if len(concept_info['concept_2']['explanation']) > 50 else concept_info['concept_2']['explanation'],
                    'color': '#0f3460',
                    'durationSec': 4
                },
                {
                    'sceneId': 4,
                    'text': "总结记忆口诀",
                    'subtitle': concept_info.get('memory_tip', "知识点已掌握"),
                    'color': '#16213e',
                    'durationSec': 3
                }
            ]
            
            # Generate video using Puppeteer wrapper
            from generators.run_puppeteer_renderer import generate_video_with_puppeteer
            
            video_path = os.path.join(output_base, f"{topic}_puppeteer.mp4")
            
            success = generate_video_with_puppeteer(
                scenes=scenes,
                output_path=video_path,
                width=1920,
                height=1080,
                fps=30
            )
            
            if success:
                print(f"✅ Puppeteer WebGL 视频生成成功：{video_path}")
                return video_path
            else:
                print("❌ Puppeteer WebGL 视频生成失败")
                return False
                
        except Exception as e:
            print(f"❌ Puppeteer 渲染错误：{str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _generate_video_with_remotion(self, topic: str, output_base: str) -> Optional[str]:
        """
        ✨ v5.4 NEW! 使用 Remotion 渲染引擎生成教学视频
        
        Remotion 优势：
        - React-based，更丰富的动效和转场
        - 更高的视觉质量（CSS/Canvas/WebGL）
        - 更好的字幕同步支持
        
        Args:
            topic: 主题名称
            output_base: 输出目录
            
        Returns:
            视频文件路径，失败则回退到 Python 方案
        """
        # 导入 Remotion Adapter
        try:
            import sys
            generators_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generators")
            if generators_dir not in sys.path:
                sys.path.insert(0, generators_dir)
            
            from video_generator_remotion_adapter import RemotionVideoAdapter
            
            # 准备输出路径
            safe_topic = topic.replace("/", "_").replace("\\", "_")
            video_path = os.path.join(output_base, f"{safe_topic}_remotion.mp4")
            
            # 创建适配器并生成视频
            adapter = RemotionVideoAdapter()
            
            if adapter.generate_video(topic, video_path):
                return video_path
            else:
                print("⚠️ Remotion 渲染失败，回退到 Python+Pillow 方案...")
                return None
                
        except ImportError as e:
            print(f"⚠️ Remotion Adapter 不可用：{e}")
            return None
        except Exception as e:
            print(f"⚠️ Remotion 渲染出错：{e}")
            import traceback
            traceback.print_exc()
            return None

    def _generate_video_with_audio(self, topic: str) -> Optional[str]:
        """
        ✨ v5.3 完整版：生成带语音解说的教学视频
        
        工作流程：
        1. 调用 v5.2 Enhanced 动态视频生成器（视觉升级）
        2. 为每个场景生成 TTS 语音（根据 topic，支持 Ollama）
        3. 合并音频轨道到视频
        4. 生成精确字幕（可选）
        
        Returns:
            视频文件路径，失败返回 None
        """
        # 统一目录结构中的路径
        skill_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 准备输出目录
        output_base = os.path.join(skill_dir, "output", topic.replace("/", "_").replace("\\", "_"))
        os.makedirs(output_base, exist_ok=True)
        
        # ✨ v5.4: Remotion 渲染方案（默认优先）
        if self.config.use_remotion:
            print("🎬 使用 Remotion (React-based) 渲染引擎...")
            return self._generate_video_with_remotion(topic, output_base)
        
        # ✨ v5.5: Puppeteer WebGL 渲染方案（高质量 HTML5 Canvas/WebGL）
        if self.config.use_puppeteer:
            print("🎬 使用 Puppeteer WebGL 渲染引擎（HTML5 Canvas/WebGL + FFmpeg）...")
            return self._generate_video_with_puppeteer(topic, output_base)
        
        # 备用：Python+Pillow 方案
        print("🎬 使用 Python+Pillow 渲染引擎（备用）...")
        video_script = os.path.join(skill_dir, "generators", "video_generator_enhanced.py")
        
        if not os.path.exists(video_script):
            print(f"⚠️ Enhanced 视频生成器未找到：{video_script}")
            # 回退到普通版本
            video_script = os.path.join(skill_dir, "generators", "video_generator_dynamic.py")
        
        # 生成对应主题的视频（v5.2 Enhanced）
        video_path = os.path.join(output_base, f"{topic}_v5.3_complete.mp4")
        
        try:
            result = subprocess.run(
                ["python3", video_script, topic, video_path],
                capture_output=True,
                text=True,
                timeout=180  # 增加超时时间（高质量渲染）
            )
            
            if result.returncode != 0 or not os.path.exists(video_path):
                print(f"⚠️ 视频生成失败：{result.stderr}")
                return None
                
            print(f"✅ v5.2 Enhanced 视频生成成功：{video_path}")
            
        except subprocess.TimeoutExpired:
            print("⚠️ 视频生成超时")
            return None
        except Exception as e:
            print(f"⚠️ 调用视频生成器失败：{e}")
            return None
        
        # ✨ v5.3: 生成 TTS 音频，根据 topic 动态调整解说词
        if self.config.generate_audio:
            audio_script = self._generate_tts_script(topic)
            audio_path = os.path.join(output_base, f"{topic}_audio.mp3")
            
            if self._generate_tts_audio(audio_script, audio_path):
                print(f"✅ 语音生成成功：{audio_path}")
                
                # ✨ v5.3: 生成精确到场景的 SRT 字幕
                subtitle_path = os.path.join(output_base, f"{topic}_subtitles.srt")
                if self.config.generate_subtitles:
                    self._generate_scene_subtitles(topic, subtitle_path)
                
                # 合并音频到视频（v5.3）✨
                final_video = os.path.join(output_base, f"{topic}_v5.3_with_voice.mp4")
                
                # 如果有字幕，一起嵌入
                if self.config.generate_subtitles and os.path.exists(subtitle_path):
                    cmd = [
                        "ffmpeg", "-y",
                        "-i", video_path,
                        "-i", audio_path,
                        "-i", subtitle_path,
                        "-c:v", "libx264",
                        "-c:a", "aac",
                        "-b:a", "128k",
                        "-c:s", "mov_text",  # 嵌入字幕轨道
                        "-map", "0:v:0",
                        "-map", "1:a:0",
                        "-map", "2:s:0",
                        "-shortest",
                        final_video
                    ]
                else:
                    cmd = [
                        "ffmpeg", "-y",
                        "-i", video_path,
                        "-i", audio_path,
                        "-c:v", "copy",  # 视频流不重新编码（快速）
                        "-c:a", "aac",   # 音频转为 AAC
                        "-b:a", "128k",  # 音频比特率
                        "-map", "0:v:0", # 选择视频流
                        "-map", "1:a:0", # 选择音频流
                        "-shortest",     # 以较短的流为准
                        final_video
                    ]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        size_mb = os.path.getsize(final_video) / (1024*1024)
                        print(f"✅ v5.3 Complete 视频 + 语音合并成功：{final_video}")
                        print(f"   • 大小：{size_mb:.2f} MB")
                        return final_video
                    else:
                        print(f"⚠️ FFmpeg 失败：{result.stderr}")
                except Exception as e:
                    print(f"⚠️ 合并音频失败：{e}")
        
        # 如果音频生成失败，返回原视频
        return video_path

    def _generate_audio_only(self, topic: str) -> Optional[str]:
        """
        ✨ v5.0 NEW! 仅生成纯音频（播客模式）
        
        Returns:
            音频文件路径
        """
        skill_dir = os.path.dirname(os.path.abspath(__file__))
        output_base = os.path.join(skill_dir, "output", topic.replace("/", "_"))
        os.makedirs(output_base, exist_ok=True)
        
        # TODO: 生成完整的解释文本
        script = f"{topic}的深度解析音频版..."
        
        audio_path = os.path.join(output_base, f"{topic}_audio.mp3")
        
        if self._generate_tts_audio(script, audio_path):
            return audio_path
        
        return None


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Knowledge Explainer v5.0 - 知识通俗解释器（语音增强版）")
    parser.add_argument("topic", type=str, help="要解释的概念/主题")
    parser.add_argument("--depth", type=int, default=2, choices=[1,2,3,4], 
                       help="深度等级：1=一句话，2=生活化，3=可视化，4=深度解析")
    parser.add_argument("--visuals", action="store_true", help="包含可视化图表")
    parser.add_argument("--analogies", action="store_true", help="包含生活类比")
    parser.add_argument("--video", action="store_true", help="生成教学视频")
    parser.add_argument("--audio", action="store_true", help="✨ v5.0: 启用语音解说")
    parser.add_argument("--subtitles", action="store_true", help="✨ v5.0: 生成字幕文件")
    parser.add_argument("--voice", type=str, default="zh-CN-XiaoxiaoNeural", 
                       help="✨ v5.0: TTS 语音（默认：zh-CN-XiaoxiaoNeural）")
    parser.add_argument("--rate", type=int, default=0, help="✨ v5.0: 语速调整 % (-100~+100)")
    parser.add_argument("--volume", type=int, default=0, help="✨ v5.0: 音量调整 %")
    parser.add_argument("--pitch", type=int, default=0, help="✨ v5.0: 音调调整 Hz")
    parser.add_argument("--ollama", action="store_true", help="✨ v5.1: 使用 Ollama 生成解说词")
    parser.add_argument("--remotion", action="store_true", default=False, 
                       help="✨ v5.4: 启用 Remotion 渲染引擎（React-based）")
    parser.add_argument("--no-remotion", dest="remotion", action="store_false",
                       help="禁用 Remotion，使用 Python+Pillow 方案")
    parser.add_argument("--puppeteer", action="store_true", default=False,
                       help="✨ v5.5: 启用 Puppeteer WebGL 渲染引擎（HTML5 Canvas/WebGL + FFmpeg）")
    parser.add_argument("--format", type=str, default="markdown", choices=["markdown", "json", "text"])
    
    args = parser.parse_args()
    
    # 创建配置
    voice_config = VoiceConfig(
        voice=args.voice,
        rate=args.rate,
        volume=args.volume,
        pitch=args.pitch
    )
    
    config = ExplainerConfig(
        depth_level=args.depth,
        include_visuals=args.visuals,
        include_analogies=args.analogies,
        generate_video=args.video,
        voice_config=voice_config,
        generate_audio=args.audio,
        generate_subtitles=args.subtitles,
        use_ollama=args.ollama,
        use_remotion=args.remotion,  # v5.4: Remotion 渲染开关
        use_puppeteer=args.puppeteer,  # v5.5: Puppeteer WebGL 渲染开关
        output_format=args.format
    )
    
    # 创建解释器并执行
    explainer = KnowledgeExplainerV5(config)
    result = explainer.explain(args.topic)
    
    print(result)


if __name__ == "__main__":
    main()
