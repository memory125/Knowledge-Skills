#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama 集成模块 v2.0 - 优化版提示词

使用本地大模型根据主题生成高质量 TTS 解说词。
"""

import subprocess


def generate_tts_script_optimized(topic, model="qwen2.5:latest"):
    """
    ✨ v5.1 优化：使用改进的提示词生成更高质量的解说词
    
    Args:
        topic: 要解释的主题
        model: Ollama 模型名称
        
    Returns:
        生成的解说文本，失败返回 None
    """
    
    # ✨ v5.1 核心优化：高精度提示词（结构化 + 示例驱动）
    prompt = f"""# 角色设定
你是专业知识视频解说员，擅长用口诀式语言解释复杂概念。

# 输出要求
生成 6 行解说词，每行独立成行，格式如下：
- 第 1 行：主题 + 一句话介绍（7-10 字）
- 第 2-5 行：4 个核心要点（各 7-10 字）
- 第 6 行：总结记忆口诀（7-10 字）

# 风格要求
✅ 朗朗上口像顺口溜
✅ 每行不超过 10 个字  
✅ 用大白话不用术语
✅ 押韵更好记

# 优秀示例
主题：费曼学习法
输出：
费曼学习真神奇
选个主题要明确
假装教给别人听
卡住回头补漏洞
简化语言去术语
真正懂才能讲清

主题：量子力学  
输出：
量子世界真奇妙
粒子行为怪又刁
波粒二相非传统
测不准理让人愁
多世界解疑无踪
微观量子记心间

# 当前任务
主题：{topic}

请直接输出 6 行解说词，不要任何额外文字。"""

    try:
        cmd = ["ollama", "run", model]
        
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"⚠️ Ollama 调用失败：{result.stderr}")
            return None
        
        # 清理输出（提取 6 行解说词）
        output = result.stdout.strip()
        
        # 过滤掉可能的多余内容（只保留纯文本行）
        lines = []
        for line in output.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('主题：'):
                continue
            if len(line) < 30:  # 避免过长行（可能是说明文字）
                lines.append(line)
        
        # 确保只有 6 段
        if len(lines) > 6:
            lines = lines[:6]
        
        # 如果不足 6 段，用主题生成默认内容
        if len(lines) < 6:
            print(f"⚠️ Ollama 输出不足 6 行（{len(lines)}），使用默认模板")
            return f"""{topic}知识深又广

首先理解基本定义和概念框架

其次掌握核心原理和工作机制

第三了解实际应用场景和方法

最后总结要点便于记忆应用"""
        
        script = "\n\n".join(lines)
        
        print(f"✅ Ollama v2.0 生成解说词成功（{len(lines)}段）")
        return script
        
    except subprocess.TimeoutExpired:
        print("⚠️ Ollama 调用超时")
        return None
    except Exception as e:
        print(f"⚠️ Ollama 调用异常：{e}")
        return None


def test_optimized_prompts():
    """测试优化后的提示词"""
    topics = ["区块链", "人工智能", "相对论"]
    
    for topic in topics:
        print("=" * 70)
        print(f"🧪 测试 Ollama v2.0 - 主题：{topic}")
        print("=" * 70)
        
        script = generate_tts_script_optimized(topic)
        
        if script:
            print("\n生成结果:")
            print("-" * 70)
            print(script)
            print("-" * 70 + "\n")


if __name__ == "__main__":
    test_optimized_prompts()
