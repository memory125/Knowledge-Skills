#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Explainer v2.0 - 知识通俗解释器（全功能版）
新增：漫画生成、语音解说、互动问答、领域模板、视频推荐
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import re
import base64
import io

# 扩展功能依赖（可选）
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import yt_dlp
    HAS_YT_DLP = True
except ImportError:
    HAS_YT_DLP = False


class KnowledgeExplainerV2:
    """知识通俗解释器 v2.0 - 全功能版"""
    
    # ==== 配置区域 ====
    CONFIG = {
        'comedyai_api_key': os.environ.get('COMFYUI_API_KEY', ''),
        'dalle_api_key': os.environ.get('DALL_E_API_KEY', ''),
        'stable_diffusion_url': os.environ.get('STABLE_DIFFUSION_URL', 'http://localhost:7860'),
        'tts_provider': 'edge-tts',  # edge-tts, google-tts, azure-tts
        'video_search_engines': ['youtube', 'bilibili', 'youku'],
    }
    
    # 领域专用模板库
    DOMAIN_TEMPLATES = {
        'general': {
            'style': '通俗易懂的科普风格',
            'analogies': ['日常生活', '工作场景', '游戏世界'],
            'visual_style': '清晰的卡通风格图示',
            'disclaimer': ''
        },
        'medical': {
            'style': '通俗易懂 + 医学科普风格',
            'analogies': ['人体工厂', '细胞小镇', '免疫系统卫队'],
            'visual_style': '医学插图风格，清晰标注',
            'disclaimer': '⚠️ 本解释仅供参考，具体医疗问题请咨询专业医生'
        },
        'legal': {
            'style': '严谨但易理解的普法风格',
            'analogies': ['社会规则', '游戏规则', '合同契约'],
            'visual_style': '流程图 + 法律条文对照',
            'disclaimer': '⚠️ 本解释不构成法律建议，具体问题请咨询律师'
        },
        'tech': {
            'style': '技术科普风格，适度专业术语',
            'analogies': ['电脑系统', '互联网世界', '编程逻辑'],
            'visual_style': '架构图 + 数据流图',
            'disclaimer': ''
        },
        'finance': {
            'style': '投资理财通俗讲解',
            'analogies': ['种树存钱', '开店经营', '游戏经济'],
            'visual_style': '趋势图 + 对比表',
            'disclaimer': '⚠️ 投资有风险，本解释不构成投资建议'
        },
        'science': {
            'style': '科学探索风格',
            'analogies': ['宇宙探险', '微观世界', '自然现象'],
            'visual_style': '科学示意图 + 实验演示',
            'disclaimer': ''
        }
    }
    
    def __init__(self, query: str, enable_extensions: List[str] = None):
        self.query = query
        self.concept = ""
        self.difficulty_level = "beginner"
        self.domain = "general"
        self.output_dir = Path("/tmp/knowledge-explainer-v2")
        self.output_dir.mkdir(exist_ok=True)
        
        # 启用的扩展功能
        self.enabled_extensions = enable_extensions or []
        
    def analyze_query(self) -> Dict:
        """分析用户问题，判断概念、难度和领域"""
        
        # 关键词检测（更完善）
        keywords = {
            "medical": ["疾病", "治疗", "药物", "症状", "诊断", "医学"],
            "legal": ["法律", "合同", "权利", "诉讼", "法规", "判决"],
            "tech": ["人工智能", "AI", "区块链", "量子", "云计算", "大数据", "编程"],
            "finance": ["投资", "股票", "比特币", "通货膨胀", "经济", "理财"],
            "science": ["物理", "化学", "生物", "宇宙", "基因", "细胞", "科学"],
        }
        
        detected_domains = []
        for domain, words in keywords.items():
            if any(word in self.query for word in words):
                detected_domains.append(domain)
        
        # 判断难度级别
        difficulty_patterns = {
            "beginner": ["是什么", "啥是", "怎么理解", "通俗解释", "简单说", "能讲讲"],
            "intermediate": ["原理", "机制", "如何工作", "为什么", "深入一点"],
            "advanced": ["数学表达", "理论推导", "深层分析", "专业角度", "学术"]
        }
        
        for level, patterns in difficulty_patterns.items():
            if any(p in self.query for p in patterns):
                self.difficulty_level = level
                break
        
        return {
            "query": self.query,
            "domains": detected_domains or ["general"],
            "difficulty": self.difficulty_level,
            "timestamp": datetime.now().isoformat()
        }
    
    def extract_concept(self) -> str:
        """从问题中提取核心概念"""
        patterns = [
            r'(?:什么是 | 啥是|解释一下|通俗讲|简单说)\s*([^\？]+)\??',
            r'([^\s]+\s*(?:和|与)[^\s]+)(?:的什么区别|有啥不同)',
            r'([^\s]+)(?:怎么工作 | 如何运作|原理是什么)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.query)
            if match:
                self.concept = match.group(1).strip()
                return self.concept
        
        self.concept = self.query
        return self.concept
    
    # ==== 扩展功能 1: 真实漫画生成 ====
    def generate_comic_image(self, concept: str, style: str = "cartoon") -> Optional[str]:
        """使用 ComfyUI/Stable Diffusion 生成漫画风格图片"""
        
        if not self._check_api_config():
            print("⚠️  未配置 AI 绘图 API，跳过图片生成")
            return None
        
        # 构建提示词
        prompt = self._build_image_prompt(concept, style)
        
        try:
            # 使用 ComfyUI 生成（示例）
            import requests
            
            response = requests.post(
                f"{self.CONFIG['stable_diffusion_url']}/api/text2img",
                json={
                    "prompt": prompt,
                    "negative_prompt": "blurry, low quality, distorted",
                    "steps": 20,
                    "width": 512,
                    "height": 512,
                },
                timeout=60
            )
            
            if response.status_code == 200:
                image_data = response.json()['images'][0]
                filepath = self.output_dir / f"comic_{concept[:10]}.png"
                
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(image_data))
                
                return str(filepath)
        except Exception as e:
            print(f"图片生成失败：{e}")
        
        return None
    
    def _build_image_prompt(self, concept: str, style: str) -> str:
        """构建 AI 绘图提示词"""
        
        style_prompts = {
            "cartoon": "educational cartoon style, simple illustration, clear lines",
            "comic": "comic book style, colorful, expressive characters",
            "infographic": "infographic style, clean design, icons and labels",
            "anime": "anime style, Japanese animation, bright colors"
        }
        
        base_prompt = f"""
        Educational illustration about {concept}, 
        {style_prompts.get(style, 'cartoon')},
        teaching diagram, easy to understand,
        white background, professional quality
        """
        
        return base_prompt.strip()
    
    # ==== 扩展功能 2: 语音解说 ====
    def generate_audio_explanation(self, text: str) -> Optional[str]:
        """使用 TTS 生成语音文件"""
        
        if not HAS_REQUESTS:
            print("⚠️  requests 库未安装，无法生成音频")
            return None
        
        try:
            # 方法 1: Edge TTS (免费)
            import edge_tts
            
            filepath = self.output_dir / f"explanation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            
            communicate = edge_tts.Communicate(
                text[:5000],  # 限制长度
                "zh-CN-XiaoxiaoNeural",  # 中文语音
                rate="+10%"
            )
            
            with open(filepath, "wb") as f:
                async def amain():
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            f.write(chunk["data"])
                
            import asyncio
            asyncio.run(amain())
            
            return str(filepath)
            
        except ImportError:
            print("⚠️  edge-tts 未安装，请运行：pip install edge-tts")
            return None
        except Exception as e:
            print(f"语音生成失败：{e}")
            return None
    
    # ==== 扩展功能 3: 互动问答系统 ====
    def interactive_mode(self, max_rounds: int = 5):
        """进入多轮互动问答模式"""
        
        print("\n🤖 进入互动问答模式\n")
        print(f"最多 {max_rounds} 轮对话，输入 'quit' 退出\n")
        
        context = {
            "concept": self.extract_concept(),
            "difficulty": self.difficulty_level,
            "history": []
        }
        
        for round_num in range(max_rounds):
            try:
                user_input = input(f"[第{round_num+1}轮] 你的问题：").strip()
                
                if user_input.lower() in ['quit', '退出', '结束']:
                    print("👋 感谢使用！再见~")
                    break
                
                if not user_input:
                    continue
                
                # 生成回答
                response = self._generate_interactive_response(user_input, context)
                
                print(f"\n💡 {response}\n")
                
                context["history"].append({
                    "question": user_input,
                    "answer": response,
                    "round": round_num + 1
                })
                
            except KeyboardInterrupt:
                print("\n\n👋 感谢使用！再见~")
                break
    
    def _generate_interactive_response(self, question: str, context: Dict) -> str:
        """生成互动问答的回答"""
        
        # 根据上下文调整回答深度
        if len(context["history"]) == 1:
            prefix = "📚 首先让我们了解基础："
        elif len(context["history"]) <= 3:
            prefix = "💡 进一步来说："
        else:
            prefix = "🎯 深入理解："
        
        # 构建提示词
        prompt = f"""基于之前的讨论（概念：{context['concept']}），用户现在问："{question}"

请用大白话回答，结合之前的对话历史。

回答要求：
1. 延续之前的解释风格
2. 用生活化的比喻
3. 给出具体例子

回答：
""" + prefix
        
        # 调用 Ollama（简化版）
        try:
            import subprocess
            result = subprocess.run(
                ['ollama', 'run', 'qwen2.5', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        #  fallback 回答
        return f"关于'{question}'，可以理解为：这是{context['concept']}的一个延伸问题。用简单的比喻来说，就像..."
    
    # ==== 扩展功能 4: 领域专用模板 ====
    def get_domain_template(self, domain: str) -> Dict:
        """获取特定领域的解释模板"""
        
        return self.DOMAIN_TEMPLATES.get(domain, self.DOMAIN_TEMPLATES["general"])
    
    def apply_domain_style(self, explanation: str, domain: str) -> str:
        """根据领域风格调整解释内容"""
        
        template = self.get_domain_template(domain)
        
        # 添加免责声明
        if template.get('disclaimer'):
            explanation += f"\n\n{template['disclaimer']}"
        
        return explanation
    
    # ==== 扩展功能 5: 视频推荐 ====
    def find_relevant_videos(self, concept: str, max_results: int = 3) -> List[Dict]:
        """搜索相关的科普视频"""
        
        videos = []
        
        # 方法 1: 使用 YouTube Data API（需要 API Key）
        if self.CONFIG.get('youtube_api_key'):
            try:
                import googleapiclient.discovery
                
                youtube = googleapiclient.discovery.build(
                    'youtube', 'v3',
                    developerKey=self.CONFIG['youtube_api_key']
                )
                
                search = youtube.search().list(
                    q=f"{concept} 科普 通俗解释",
                    part='snippet,id',
                    type='video',
                    maxResults=max_results,
                    regionCode='CN'
                )
                
                for item in search['items']:
                    if item['id']['kind'] == 'youtube#video':
                        videos.append({
                            "platform": "YouTube",
                            "title": item['snippet']['title'],
                            "url": f"https://youtube.com/watch?v={item['id']['videoId']}",
                            "channel": item['snippet']['channelTitle']
                        })
                        
            except Exception as e:
                print(f"YouTube 搜索失败：{e}")
        
        # 方法 2: Bilibili（使用关键词构建 URL）
        bilibili_search_url = f"https://search.bilibili.com/all?keyword={concept}科普"
        videos.append({
            "platform": "Bilibili",
            "title": f"搜索'{concept}科普'",
            "url": bilibili_search_url,
            "note": "在 Bilibili 查看相关视频"
        })
        
        # 方法 3: 通用推荐（无需 API）
        general_recommendations = [
            {
                "platform": "Bilibili",
                "title": f"{concept} 入门教程合集",
                "url": f"https://search.bilibili.com/all?keyword={concept}",
                "note": "适合初学者的视频"
            },
            {
                "platform": "YouTube",
                "title": f"What is {concept}? (Explanation)",
                "url": f"https://www.youtube.com/results?search_query=what+is+{concept.replace(' ', '+')}",
                "note": "英文科普视频"
            }
        ]
        
        videos.extend(general_recommendations[:max_results])
        
        return videos
    
    def format_video_links(self, videos: List[Dict]) -> str:
        """格式化视频链接输出"""
        
        if not videos:
            return "\n⚠️ 未找到相关视频\n"
        
        output = ["\n## 📹 推荐学习视频"]
        
        for i, video in enumerate(videos, 1):
            output.append(f"\n{i}. **{video['platform']}**: [{video['title']}]({video['url']})")
            
            if video.get('note'):
                output.append(f"   - 💡 {video['note']}")
        
        return "\n".join(output)
    
    # ==== 主解释流程（v2.0） ====
    def explain_with_ollama_v2(self, model: str = "qwen2.5", 
                             enable_comic: bool = False,
                             enable_audio: bool = False,
                             enable_interactive: bool = False,
                             enable_video: bool = False) -> Dict:
        """v2.0 版本完整解释流程"""
        
        # 1. 分析问题
        analysis = self.analyze_query()
        concept = self.extract_concept()
        domains = analysis['domains']
        
        print(f"\n🧠 v2.0 智能分析:")
        print(f"   ✓ 概念：{concept}")
        print(f"   ✓ 难度：{analysis['difficulty']}")
        print(f"   ✓ 领域：{', '.join(domains)}")
        
        # 2. 应用领域模板
        if domains and len(domains) > 0:
            domain = domains[0]
            template = self.get_domain_template(domain)
            print(f"   ✓ 风格：{template['style']}")
        
        # 3. 调用 AI 生成解释
        prompt = self._build_v2_prompt(concept, analysis)
        
        try:
            import subprocess
            result = subprocess.run(
                ['ollama', 'run', model, prompt],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                return {'success': False, 'error': result.stderr}
            
            explanation = result.stdout
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        # 4. 应用领域风格
        if domains and len(domains) > 0:
            explanation = self.apply_domain_style(explanation, domains[0])
        
        # 5. 扩展功能处理
        results = {
            'success': True,
            'explanation': explanation,
            'concept': concept,
            'analysis': analysis,
            'extensions': {}
        }
        
        # 生成漫画图片
        if enable_comic and 'comic' in self.enabled_extensions:
            image_path = self.generate_comic_image(concept)
            if image_path:
                results['extensions']['image'] = {
                    'path': image_path,
                    'type': 'png',
                    'description': f'{concept}的漫画图示'
                }
        
        # 生成语音
        if enable_audio and 'audio' in self.enabled_extensions:
            audio_path = self.generate_audio_explanation(explanation[:3000])
            if audio_path:
                results['extensions']['audio'] = {
                    'path': audio_path,
                    'type': 'mp3',
                    'duration': '约 2-3 分钟'
                }
        
        # 视频推荐
        if enable_video and 'video' in self.enabled_extensions:
            videos = self.find_relevant_videos(concept)
            results['extensions']['videos'] = videos
            explanation += self.format_video_links(videos)
        
        return results
    
    def _build_v2_prompt(self, concept: str, analysis: Dict) -> str:
        """构建 v2.0 版本的提示词"""
        
        domain_style = ""
        if analysis['domains']:
            template = self.get_domain_template(analysis['domains'][0])
            domain_style = f"\n请采用{template['style']}进行解释。"
        
        difficulty_guide = {
            "beginner": "用 10 岁孩子能懂的语言，多打比方，少用术语",
            "intermediate": "可以适当使用专业术语，但要详细解释",
            "advanced": "深入分析，但保持逻辑清晰"
        }
        
        return f"""你是一个专业的知识通俗解释专家（v2.0 版），你的任务是把复杂的概念用最生动、最易懂的方式呈现。

### 用户问题
{self.query}

### 核心概念
{concept}

### 难度等级
{analysis['difficulty']} ({difficulty_guide[analysis['difficulty']]})

{domain_style}

---

## 🎯 输出格式要求（完整 Markdown）：

# 📚 {concept}（大白话版 v2.0）

> **💡 一句话总结**: [用不超过 30 字，生动地说清楚]

---

## 🎭 漫画场景/图示
[这里可以用 ASCII 画，或者描述一个生动的场景]

---

## 💡 生活化类比（至少 2 个）

| 比喻类型 | 通俗解释 |
|---------|---------|
| [类型 1] | [像什么] |
| [类型 2] | [为什么这样] |

---

## 🔑 核心要点（3-5 个）

每个要点包含：
- **是什么**: [定义]
- **为什么重要**: [价值]
- **怎么应用**: [例子]

---

## 🔄 对比表格

| 新概念 | 传统理解/对比项 |
|--------|------------|
| ...    | ...        |

---

## 🤔 你可能会问（3 个）

- ❓ [问题 1] → [简短回答]
- ❓ [问题 2] → [简短回答]
- ❓ [问题 3] → [简短回答]

---

## 🎯 一句话记住

[用一句容易记的话总结，最好押韵或有节奏感]

---

## 📹 视频学习推荐

[AI 会根据概念自动推荐相关科普视频链接]

**风格要求**:
✅ 像朋友聊天一样自然
✅ 多用"就像..."、"好比..."、"想象一下..."
✅ 每个专业术语后都跟一个生活例子
✅ 输出要有趣，让人愿意读下去

请输出完整的 Markdown 内容。"""
    
    def _check_api_config(self) -> bool:
        """检查 API 配置是否完整"""
        
        # 至少需要一种 AI 绘图服务配置
        if self.CONFIG.get('stable_diffusion_url') and self.CONFIG['stable_diffusion_url'] != 'http://localhost:7860':
            return True
        
        if self.CONFIG.get('dalle_api_key'):
            return True
        
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Knowledge Explainer v2.0 - 全功能知识通俗解释系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本解释
  ./knowledge-explainer-v2 explain "区块链"

  # 启用漫画生成（需配置 API）
  ./knowledge-explainer-v2 explain "AI 原理" --comic

  # 生成语音解说
  ./knowledge-explainer-v2 explain "光合作用" --audio

  # 互动问答模式
  ./knowledge-explainer-v2 interact "量子力学"

  # 全功能开启
  ./knowledge-explainer-v2 explain "区块链" --all-features -o output.md

        """
    )
    
    parser.add_argument('command', choices=['explain', 'interact', 'demo'], 
                       help='命令：explain(解释) | interact(互动) | demo(演示)')
    parser.add_argument('query', type=str, nargs='?', 
                       help='要解释的概念（如"区块链是什么"）')
    
    # 扩展功能开关
    parser.add_argument('--comic', '-c', action='store_true',
                       help='启用漫画图片生成（需配置 ComfyUI/Stable Diffusion）')
    parser.add_argument('--audio', '-a', action='store_true',
                       help='生成语音解说文件')
    parser.add_argument('--video', '-v', action='store_true',
                       help='搜索推荐相关科普视频')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='启用互动问答模式')
    parser.add_argument('--all-features', action='store_true',
                       help='启用所有扩展功能')
    
    # 其他选项
    parser.add_argument('--model', '-m', default='qwen2.5', 
                       help='Ollama 模型 (默认：qwen2.5)')
    parser.add_argument('--output', '-o', type=str, default=None, 
                       help='输出文件路径')
    parser.add_argument('--domain', '-d', type=str, default=None,
                       help='指定领域：medical/legal/tech/finance/science')
    
    args = parser.parse_args()
    
    # 构建启用的扩展功能列表
    enabled_extensions = []
    
    if args.all_features:
        enabled_extensions = ['comic', 'audio', 'video', 'interactive']
    else:
        if args.comic:
            enabled_extensions.append('comic')
        if args.audio:
            enabled_extensions.append('audio')
        if args.video:
            enabled_extensions.append('video')
        if args.interactive:
            enabled_extensions.append('interactive')
    
    # 演示模式
    if args.command == 'demo':
        print("\n=== Knowledge Explainer v2.0 Demo ===\n")
        print("预设示例问题:")
        demos = [
            "区块链是什么",
            "量子纠缠通俗解释",
            "人工智能怎么工作",
            "光合作用原理"
        ]
        
        for i, demo in enumerate(demos, 1):
            print(f"{i}. \"{demo}\"")
        
        print("\n功能特性:")
        print("• 🎨 漫画生成 (--comic)")
        print("• 🎤 语音解说 (--audio)")
        print("• 💬 互动问答 (--interactive)")
        print("• 📹 视频推荐 (--video)")
        print("• 🏥 领域模板 (--domain medical/legal/tech...)")
        
    # 解释模式
    elif args.command == 'explain':
        if not args.query:
            print("❌ 错误：请提供要解释的概念")
            sys.exit(1)
        
        explainer = KnowledgeExplainerV2(args.query, enabled_extensions)
        
        # 手动指定领域
        if args.domain:
            explainer.domain = args.domain
        
        result = explainer.explain_with_ollama_v2(
            model=args.model,
            enable_comic=('--comic' in sys.argv or '--all-features' in sys.argv),
            enable_audio=('--audio' in sys.argv or '--all-features' in sys.argv),
            enable_video=('--video' in sys.argv or '--all-features' in sys.argv)
        )
        
        if result['success']:
            explanation = result['explanation']
            
            # 输出结果
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(explanation)
                
                print(f"\n✅ v2.0 解释完成！")
                print(f"📄 文本已保存：{args.output}")
                
                # 显示生成的扩展文件
                if result['extensions']:
                    print("\n🎁 额外生成:")
                    if 'image' in result['extensions']:
                        print(f"   🖼️  漫画图片：{result['extensions']['image']['path']}")
                    if 'audio' in result['extensions']:
                        print(f"   🎵 语音文件：{result['extensions']['audio']['path']}")
                    if 'videos' in result['extensions']:
                        print(f"   📹 推荐视频：{len(result['extensions']['videos'])}个链接")
            else:
                print("✅ v2.0 完整解释：" + "="*60 + "\n")
                print(explanation)
        else:
            print(f"❌ 失败：{result['error']}")
    
    # 互动模式
    elif args.command == 'interact':
        if not args.query:
            print("❌ 错误：请提供要讨论的概念")
            sys.exit(1)
        
        explainer = KnowledgeExplainerV2(args.query)
        explainer.interactive_mode()


if __name__ == '__main__':
    main()
