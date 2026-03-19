#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama 集成模块 - 自动生成解说词

使用本地大模型根据主题生成 TTS 解说词，避免硬编码。
"""

import subprocess
import json


def generate_tts_script(topic, model="qwen2.5:latest", max_tokens=300):
    """
    使用 Ollama 自动生成 TTS 解说词
    
    Args:
        topic: 要解释的主题
        model: Ollama 模型名称（默认：qwen2.5:latest）
        max_tokens: 生成长度限制
        
    Returns:
        生成的解说文本，失败返回 None
    """
    
    # 系统提示词：定义输出格式和风格
    system_prompt = """你是一个专业的知识视频解说员。你的任务是为教学视频生成简洁、生动的解说词。

要求：
1. 解说词必须简短精炼，每句话不超过 20 个字
2. 总共生成 6 段话（标题开场 + 4 个要点 + 总结）
3. 用大白话，避免专业术语
4. 每段话独立成行，不要换行符
5. 风格要生动有趣，让人容易记住

输出格式：每段一行，共 6 行"""


    # 用户提示词
    user_prompt = f"""请为以下主题生成视频解说词（6 段话）：

主题：{topic}

请按照以下结构组织内容：
第 1 行：标题开场（一句话介绍主题）
第 2 行：第 1 个要点
第 3 行：第 2 个要点
第 4 行：第 3 个要点
第 5 行：第 4 个要点
第 6 行：总结记忆口诀

只输出这 6 行内容，不要其他文字。"""

    try:
        # 调用 Ollama API (简化版)
        prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # 使用 ollama run 命令（标准模式）
        cmd = [
            "ollama", "run", model
        ]
        
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60  # 超时 60 秒
        )
        
        if result.returncode != 0:
            print(f"⚠️ Ollama 调用失败：{result.stderr}")
            return None
        
        # 清理输出（去掉可能的多余内容）
        output = result.stdout.strip()
        
        # 如果输出包含 "```" 代码块标记，提取内容
        if "```" in output:
            output = output.split("```")[1] if output.count("```") >= 2 else output
            output = output.split("\n")[-6:]  # 取最后 6 行
        
        # 分割成段落（按换行符）
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        
        # 确保只有 6 段
        if len(lines) > 6:
            lines = lines[:6]
        
        # 用空行连接（TTS 需要段落间隔）
        script = "\n\n".join(lines)
        
        print(f"✅ Ollama 生成解说词成功（{len(lines)}段）")
        return script
        
    except subprocess.TimeoutExpired:
        print("⚠️ Ollama 调用超时")
        return None
    except Exception as e:
        print(f"⚠️ Ollama 调用异常：{e}")
        return None


def test_ollama_integration():
    """测试 Ollama 集成"""
    topic = "费曼学习法"
    
    print("=" * 70)
    print(f"🧪 测试 Ollama 解说词生成")
    print(f"主题：{topic}")
    print("=" * 70)
    print()
    
    script = generate_tts_script(topic)
    
    if script:
        print()
        print("生成结果:")
        print("-" * 70)
        print(script)
        print("-" * 70)
    else:
        print("生成失败")


if __name__ == "__main__":
    test_ollama_integration()
