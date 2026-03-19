#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Explainer - 知识通俗解释器 v1.0
将复杂概念用大白话 + 可视化方式呈现
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import re

# 视觉生成库（可选）
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class KnowledgeExplainer:
    """知识通俗解释器"""
    
    def __init__(self, query: str):
        self.query = query
        self.concept = ""
        self.difficulty_level = "beginner"  # beginner, intermediate, advanced
        self.output_dir = Path("/tmp/knowledge-explainer")
        self.output_dir.mkdir(exist_ok=True)
        
    def analyze_query(self) -> Dict:
        """分析用户问题，判断概念和难度"""
        
        # 简单关键词检测来判断领域
        keywords = {
            "tech": ["人工智能", "AI", "区块链", "量子", "云计算", "大数据"],
            "science": ["物理", "化学", "生物", "宇宙", "基因", "细胞"],
            "finance": ["投资", "股票", "比特币", "通货膨胀", "经济"],
            "philosophy": ["哲学", "存在主义", "伦理学", "认识论"]
        }
        
        detected_fields = []
        for field, words in keywords.items():
            if any(word in self.query for word in words):
                detected_fields.append(field)
        
        # 判断难度级别
        question_indicators = {
            "beginner": ["是什么", "啥是", "怎么理解", "通俗解释", "简单说"],
            "intermediate": ["原理", "机制", "如何工作", "为什么"],
            "advanced": ["数学表达", "理论推导", "深层分析", "批判性"]
        }
        
        for level, indicators in question_indicators.items():
            if any(ind in self.query for ind in indicators):
                self.difficulty_level = level
                break
        
        return {
            "query": self.query,
            "fields": detected_fields,
            "difficulty": self.difficulty_level,
            "timestamp": datetime.now().isoformat()
        }
    
    def extract_concept(self) -> str:
        """从问题中提取核心概念"""
        
        # 常见模式匹配
        patterns = [
            r'(?:什么是 | 啥是|解释一下|通俗讲)\s*([^\？]+)\??',
            r'([^\s]+\s*(?:和|与)[^\s]+)(?:的什么区别|有啥不同)',
            r'([^\s]+)(?:怎么工作|如何运作|原理是什么)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.query)
            if match:
                self.concept = match.group(1).strip()
                return self.concept
        
        # 默认取整个查询作为概念
        self.concept = self.query
        return self.concept
    
    def create_analogies(self) -> List[Dict]:
        """生成生活化类比"""
        
        analogy_templates = {
            "beginner": [
                {"type": "日常生活", "template": "就像{scenario}一样"},
                {"type": "食物比喻", "template": "好比做{food}时..."},
                {"type": "游戏类比", "template": "想象一下你在玩{game}..."}
            ],
            "intermediate": [
                {"type": "工作场景", "template": "就像在职场中..."},
                {"type": "交通比喻", "template": "好比城市交通系统..."},
                {"type": "建筑类比", "template": "就像盖房子的过程..."}
            ],
            "advanced": [
                {"type": "学术对比", "template": "类似于{field}中的..."},
                {"type": "历史参照", "template": "正如历史上..."},
                {"type": "跨学科联系", "template": "这与{discipline}有相似之处"}
            ]
        }
        
        return analogy_templates.get(self.difficulty_level, analogy_templates["beginner"])
    
    def generate_ascii_art(self, concept: str) -> str:
        """生成简单的 ASCII 艺术图"""
        
        ascii_templates = {
            "blockchain": """
    [A] === [B] === [C] === [D]
      ↓       ↓       ↓       ↓
    [账本][账本][账本][账本]
     全网同步，无人能改！ ✅
            """,
            
            "ai": """
    👁️ 眼睛 (输入) 
      ↓
    🧠 大脑 (AI 处理)
      ↓  
    👄 嘴巴 (输出结果)
    
    = 学习 → 理解 → 回答 =
            """,
            
            "inflation": """
    💰 钱多了 → 🛒 东西还是那么多
              ↓
    💸 同样的钱买到的东西变少
              ↓
    📈 价格标签往上涨
    = 通货膨胀 =
            """,
            
            "default": """
    ┌─────────────┐
    │   {concept} │
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │  核心要点   │
    ├─────────────┤
    │ • 要点 1     │
    │ • 要点 2     │
    │ • 要点 3     │
    └─────────────┘
            """
        }
        
        # 简单关键词匹配
        if "区块链" in concept or "blockchain" in concept.lower():
            return ascii_templates["blockchain"]
        elif "人工" in concept and "智能" in concept:
            return ascii_templates["ai"]
        elif "通货膨胀" in concept or "通胀" in concept:
            return ascii_arrays["inflation"]
        else:
            return ascii_templates["default"].format(concept=concept)
    
    def create_comparison_table(self, concept: str) -> str:
        """生成对比表格"""
        
        # 通用模板
        table_template = """
| 🟢 {concept} | 🔵 传统方式/对比项 |
|--------------|-------------------|
| **特点 1**   | 对比内容 1         |
| **特点 2**   | 对比内容 2         |
| **优势**     | vs 劣势           |
| **适用场景** | 何时使用          |
"""
        return table_template.format(concept=concept)
    
    def generate_visual_explanation(self, concept: str) -> str:
        """生成视觉化解释（ASCII/Mermaid）"""
        
        # Mermaid 流程图模板
        mermaid_template = """
```mermaid
graph TD
    A[{概念：{concept}}] --> B(核心要素 1)
    A --> C(核心要素 2)  
    A --> D(核心要素 3)
    
    B --> E[实际例子]
    C --> F[生活场景]
    D --> G[应用场景]
```
"""
        return mermaid_template.format(concept=concept[:10])  # 限制长度
    
    def create_explanation_content(self, analysis: Dict) -> str:
        """创建完整的解释内容"""
        
        concept = self.extract_concept()
        
        content_parts = [
            f"# 📚 {concept}（大白话版）",
            "",
            "> 💡 **一句话总结**：[AI 将在此生成通俗定义]",
            "",
            "---",
            "",
            "## 🎭 漫画/图示场景",
            "",
            self.generate_ascii_art(concept),
            "",
            "---",
            "",
            "## 💡 生活化类比",
            "",
            "| 类型 | 比喻说明 |",
            "|------|---------|",
        ]
        
        # 添加类比
        analogies = self.create_analogies()
        for i, analogy in enumerate(analogies[:3], 1):
            content_parts.append(f"| {analogy['type']} | 就像{self.generate_analogy_text(i)} |")
        
        content_parts.extend([
            "",
            "---",
            "",
            "## 🔑 核心要点（3-5 个）",
            "",
            "1. **要点一**: [AI 将生成]",
            "2. **要点二**: [AI 将生成]",
            "3. **要点三**: [AI 将生成]",
            "",
            "---",
            "",
            "## 🤔 常见问题",
            "",
            "- ❓ 为什么重要？→ [AI 回答]",
            "- ❓ 怎么用？ → [AI 回答]",
            "- ❓ 有什么例子？ → [AI 回答]",
            "",
            "---",
            "",
            "## 📹 推荐资源",
            "",
            "- 🎥 [相关科普视频链接]",
            "- 📚 [延伸阅读材料]",
            "- 🔗 [互动学习网站]",
            "",
            f"\n*由 Knowledge Explainer v1.0 生成 | {datetime.now().strftime('%Y-%m-%d')}*"
        ])
        
        return "\n".join(content_parts)
    
    def generate_analogy_text(self, index: int) -> str:
        """生成类比文本"""
        
        analogies = {
            1: "日常生活里常见的...",
            2: "厨房做饭时遇到的...",
            3: "玩游戏时的..."
        }
        
        return analogies.get(index, "生活中的例子...")
    
    def explain_with_ollama(self, model: str = "qwen2.5") -> Dict:
        """使用 Ollama 进行智能解释"""
        
        import subprocess
        
        # 分析问题
        analysis = self.analyze_query()
        concept = self.extract_concept()
        
        # 构建提示词
        prompt = self._create_ollama_prompt(concept, analysis)
        
        try:
            result = subprocess.run(
                ['ollama', 'run', model, prompt],
                capture_output=True,
                text=True,
                timeout=300  # 5 分钟超时
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'explanation': result.stdout,
                    'concept': concept,
                    'analysis': analysis
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
                
        except FileNotFoundError:
            return {
                'success': False,
                'error': '未找到 Ollama，请运行：ollama serve'
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '解释超时，概念可能太复杂'
            }
    
    def _create_ollama_prompt(self, concept: str, analysis: Dict) -> str:
        """创建 Ollama 提示词"""
        
        difficulty_guide = {
            "beginner": "用 10 岁孩子能懂的语言，多打比方，少用术语",
            "intermediate": "可以适当使用专业术语，但要解释清楚",
            "advanced": "深入分析，但保持逻辑清晰"
        }
        
        return f"""你是一个知识通俗解释专家，你的任务是把复杂的概念用大白话讲清楚。

### 用户问题
{self.query}

### 核心概念
{concept}

### 用户水平
{analysis['difficulty']} ({difficulty_guide[analysis['difficulty']]})

### 领域
{', '.join(analysis['fields']) or '通用'}

---

## 请按照以下格式输出（使用 Markdown）：

# 📚 {concept}（大白话版）

> **💡 一句话总结**: [用不超过 30 字，通俗地说清楚]

---

## 🎭 漫画/图示场景
[这里用 ASCII 字符画一个简单图示或对话场景，帮助理解]

---

## 💡 生活化类比
用 2-3 个生活化的例子解释：
1. **像什么**: [打比方]
2. **为什么这样**: [解释原因]  
3. **实际例子**: [具体场景]

---

## 🔑 核心要点（3-5 个）
用简洁的要点总结，每个要点包含：
- **是什么**
- **为什么重要**
- **怎么应用**

---

## 🔄 对比表格（如适用）
| 新方式 | 传统方式/对比项 |
|--------|----------------|
| ...    | ...            |

---

## 🤔 你可能还会问
列出 3 个相关问题并简要回答：
- ❓ [问题 1] → [简短回答]
- ❓ [问题 2] → [简短回答]  
- ❓ [问题 3] → [简短回答]

---

## 🎯 一句话记住
[用一句容易记的话总结核心]

**风格要求**:
✅ 说人话：多用"就像..."、"好比..."、"想象一下..."
❌ 不说教：避免学术腔和术语堆砌  
✅ 给例子：每个要点配生活案例
✅ 有层次：从简单到深入分层解释

请输出完整的 Markdown 格式内容。"""


def main():
    parser = argparse.ArgumentParser(
        description='知识通俗解释器 - 大白话 + 可视化呈现复杂概念',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python explainer.py explain "区块链是什么"

  # 指定模型
  python explainer.py explain "量子纠缠" --model qwen2.5
  
  # 导出到文件
  python explainer.py explain "人工智能原理" -o explanation.md
        
        """
    )
    
    parser.add_argument('command', choices=['explain', 'demo'], 
                       help='命令：explain(解释) 或 demo(演示)')
    parser.add_argument('query', type=str, nargs='?', 
                       help='要解释的概念或问题（如"区块链是什么"）')
    parser.add_argument('--model', '-m', default='qwen2.5', 
                       help='Ollama 模型名称 (默认：qwen2.5)')
    parser.add_argument('--output', '-o', type=str, default=None, 
                       help='输出文件路径')
    
    args = parser.parse_args()
    
    # 演示模式
    if args.command == 'demo':
        demo_queries = [
            "区块链是什么",
            "人工智能怎么工作的",
            "通货膨胀的原因",
            "光合作用怎么做到的"
        ]
        
        print("\n=== Knowledge Explainer Demo ===\n")
        for i, query in enumerate(demo_queries, 1):
            print(f"{i}. \"{query}\"")
        print("\n选择一个序号测试功能，或直接输入自定义问题:")
        
    # 解释模式
    elif args.command == 'explain':
        if not args.query:
            print("❌ 错误：请提供要解释的概念或问题")
            print("示例：python explainer.py explain \"区块链是什么\"")
            sys.exit(1)
        
        print(f"\n🧠 正在分析：{args.query}\n")
        
        explainer = KnowledgeExplainer(args.query)
        
        # 分析问题
        analysis = explainer.analyze_query()
        concept = explainer.extract_concept()
        
        print(f"✓ 识别概念：{concept}")
        print(f"✓ 难度等级：{analysis['difficulty']}")
        print(f"✓ 相关领域：{', '.join(analysis['fields']) or '通用'}\n")
        
        if analysis['difficulty'] == 'beginner':
            print("🎯 策略：使用大白话 + 生活比喻 + 简单图示\n")
        elif analysis['difficulty'] == 'intermediate':
            print("🎯 策略：平衡专业性与可读性，适度深入\n")
        else:
            print("🎯 策略：深度解析，但保持清晰结构\n")
        
        # 调用 AI 解释
        result = explainer.explain_with_ollama(args.model)
        
        if result['success']:
            explanation = result['explanation']
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(explanation)
                print(f"✅ 解释完成！已保存至：{args.output}")
            else:
                print("✅ 完整解释如下：" + "="*60 + "\n")
                print(explanation)
                print("\n" + "="*60)
        else:
            print(f"❌ 解释失败：{result['error']}")
            sys.exit(1)


if __name__ == '__main__':
    main()
