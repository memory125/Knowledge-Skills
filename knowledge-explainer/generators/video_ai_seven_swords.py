#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 七剑客教学视频生成器 v5.5 - 居中对齐版
专门为 AI_SEVEN_SWORDS 主题定制，修复居中对齐问题
"""

import subprocess
from PIL import Image, ImageDraw, ImageFont
import os
import sys
import math
import random


def load_chinese_fonts():
    """加载最美中文字体"""
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 72)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 56)
        font_text = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 32)
        font_extra_small = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 28)
        return {
            'title': font_title, 
            'subtitle': font_subtitle, 
            'text': font_text, 
            'small': font_small,
            'extra_small': font_extra_small
        }, "Noto Sans CJK"
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/arphic/uming.ttc", 40)
            return {k: font for k in ['title', 'subtitle', 'text', 'small', 'extra_small']}, "uming.ttc"
        except:
            default_font = ImageFont.load_default()
            return {k: default_font for k in ['title', 'subtitle', 'text', 'small', 'extra_small']}, "default"


GLOBAL_FONTS, FONT_NAME = load_chinese_fonts()

# 配色方案（霓虹渐变）
COLORS = {
    'bg': '#0a0a14',           # 深色背景
    'accent': '#e94560',       # 主色调（珊瑚红）
    'primary': '#0f3460',      # 主要强调色（深蓝）
    'white': '#ffffff',        # 白色
    'gray_light': '#cccccc',   # 浅灰色
    'gray_dark': '#666666',    # 深灰色
    
    # 霓虹渐变配色
    'agent': '#ff6b6b',        # Agent - 珊瑚红（CEO）
    'skill': '#4ecdc4',        # Skill - 薄荷绿（工具包）
    'rag': '#ffe66d',          # RAG - 暖黄（外接大脑）
    'mcp': '#a855f7',          # MCP - 紫色（通用插座）
    'lsp': '#ec4899',          # LSP - 粉色（代码助手）
    'acp_protocol': '#06b6d4', # ACP Protocol - 青色（Agent 普通话）
    'acp_context': '#f59e0b',  # ACP Context - 琥珀色（上下文注入）
}

# AI 七剑客详细内容
AI_SEVEN_SWORDS_CONTENT = {
    "title": "🎯 AI 七剑客",
    "subtitle": "Agent, Skill, RAG, MCP, LSP, ACP 大白话解析",
    "concepts": [
        {
            "icon": "👨‍💼", 
            "name": "Agent = CEO",
            "desc": "智能体，能独立思考、制定计划、分配任务",
            "color": COLORS['agent'],
            "key_point": "有目标感·会拆解·能执行·会检查"
        },
        {
            "icon": "🧰", 
            "name": "Skill = 工具包",
            "desc": "给 Agent 安装的插件，扩展新能力",
            "color": COLORS['skill'],
            "key_point": "可扩展·模块化·可共享"
        },
        {
            "icon": "🧠", 
            "name": "RAG = 外接大脑",
            "desc": "先查资料再回答，不瞎编八道",
            "color": COLORS['rag'],
            "key_point": "不瞎编·可溯源·实时更新"
        },
        {
            "icon": "🔌", 
            "name": "MCP = 通用插座",
            "desc": "统一接口，所有 AI 工具即插即用",
            "color": COLORS['mcp'],
            "key_point": "一个接口·适配所有·打破孤岛"
        },
        {
            "icon": "👨‍💻", 
            "name": "LSP = 代码助手",
            "desc": "深度理解编程语言，自动补全 + 查 bug",
            "color": COLORS['lsp'],
            "key_point": "懂语法·会补全·提前发现错误"
        },
        {
            "icon": "📢", 
            "name": "ACP(协议) = Agent 普通话",
            "desc": "多个 Agent 协作沟通的标准语言",
            "color": COLORS['acp_protocol'],
            "key_point": "任务同步·避免冲突·团队作战"
        },
        {
            "icon": "🧠", 
            "name": "ACP(上下文) = 背景注入器",
            "desc": "临时增强情境理解，知道更多背景",
            "color": COLORS['acp_context'],
            "key_point": "情境感知·记忆增强·个性化"
        }
    ],
    "summary": "Agent=CEO | Skill=工具 | RAG=查资料 | MCP=插座 | LSP=代码助手 | ACP 协议=团队协作 | ACP 上下文=背景注入",
}


def create_gradient_bg(w, h):
    """渐变背景 + 星点装饰"""
    img = Image.new('RGB', (w, h), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    cx, cy = w // 2, h // 2
    
    # 多层光晕（模拟景深）
    for r in range(500, 0, -40):
        alpha = int(30 * (1 - r/500))
        color = (10+alpha, 10+alpha, 20+alpha)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    
    # 星点装饰（固定分布）
    random.seed(42)
    for _ in range(15):
        x, y = random.randint(0, w), random.randint(0, h)
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(220, 220, 255))
    
    return img


def text_with_glow(draw, text, pos, color, font):
    """带阴影发光效果的文字 - 使用 anchor='mm' 居中对齐"""
    # 阴影层（简化）
    for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
        draw.text((pos[0]+dx, pos[1]+dy), text, fill=(0,0,0), font=font, anchor="mm")
    
    # 主文字 - 使用 anchor='mm' 居中
    draw.text(pos, text, fill=color, font=font, anchor="mm")


def gradient_line(draw, x1, y1, x2, y2, color):
    """渐变线条"""
    length = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    
    for i in range(0, length, 3):
        t = i / max(length, 1)
        x, y = int(x1 + (x2-x1)*t), int(y1 + (y2-y1)*t)
        draw.line([(x, y), (x+4, y)], fill=color, width=4)


def progress_bar(draw, w, h, current, total):
    """高级进度条"""
    bar_h, bar_y = 10, h - 45
    pad, bar_w = 30, w - 60
    seg_w = bar_w // total
    
    # 背景轨道（居中）
    track_left = w//2 - bar_w//2
    draw.rounded_rectangle([track_left, bar_y, track_left+bar_w, bar_y+bar_h], radius=5, fill=(30,30,50))
    
    # 进度段
    for i in range(total):
        x = track_left + i * seg_w
        if i < current:
            draw.rounded_rectangle([x, bar_y, x+seg_w-2, bar_y+bar_h], radius=3, fill=COLORS['accent'])
        elif i == current:
            draw.rounded_rectangle([x, bar_y, x+seg_w-2, bar_y+bar_h], radius=3, fill=COLORS['white'])
        else:
            draw.rounded_rectangle([x, bar_y, x+seg_w-2, bar_y+bar_h], radius=3, fill=(60,60,80))


def create_title_scene(topic):
    """Scene 1: 标题开场 - 所有内容在卡片上"""
    w, h = 1920, 1080
    img = create_gradient_bg(w, h)
    draw = ImageDraw.Draw(img)
    
    # 大卡片（容纳所有标题内容）- 居中
    card_w, card_h = 1200, 450
    card_x = w//2 - card_w//2
    card_y = h//2 - card_h//2
    
    # 卡片阴影
    draw.rounded_rectangle([card_x-15, card_y-15, card_x+card_w+15, card_y+card_h+15], 
                          radius=30, fill=(0,0,0,80))
    
    # 卡片主体（深色半透明）
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], 
                          radius=30, fill=COLORS['primary'])
    
    # 主标题（发光效果）- 在卡片上居中
    text_with_glow(draw, AI_SEVEN_SWORDS_CONTENT["title"], (w//2, card_y + 100), COLORS['white'], GLOBAL_FONTS['title'])
    
    # 副标题 - 在卡片上居中
    draw.text((w//2, card_y + 200), AI_SEVEN_SWORDS_CONTENT["subtitle"], 
              fill=COLORS['accent'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # 装饰线（在卡片内）
    gradient_line(draw, w//2-200, card_y + 300, w//2+200, card_y + 300, COLORS['accent'])
    
    # 底部说明 - 在卡片上居中
    draw.text((w//2, card_y + 370), "大白话解析 AI 领域核心概念", fill=COLORS['gray_light'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # 进度条
    progress_bar(draw, w, h, 0, len(AI_SEVEN_SWORDS_CONTENT["concepts"]) + 2)
    
    return img


def create_concept_scene(topic, idx):
    """Scene 2-8: 概念详解 - 所有内容在卡片上"""
    w, h = 1920, 1080
    concept = AI_SEVEN_SWORDS_CONTENT["concepts"][idx]
    
    img = create_gradient_bg(w, h)
    draw = ImageDraw.Draw(img)
    
    # 大卡片（容纳所有概念内容）- 居中
    card_w, card_h = 1200, 500
    card_x = w//2 - card_w//2
    card_y = h//2 - card_h//2
    
    # 阴影
    draw.rounded_rectangle([card_x-15, card_y-15, card_x+card_w+15, card_y+card_h+15], 
                          radius=30, fill=(0,0,0,80))
    
    # 卡片主体（彩色）- 使用概念专属颜色
    color = concept["color"]
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], 
                          radius=30, fill=color)
    
    # 场景编号 - 在卡片上顶部居中
    draw.text((w//2, card_y + 50), f"第{idx+1}剑", fill=COLORS['white'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    # 图标（大号）- 在卡片上居中
    text_with_glow(draw, concept["icon"], (w//2, card_y + 120), COLORS['white'], GLOBAL_FONTS['subtitle'])
    
    # 概念名称 - 在卡片上居中
    draw.text((w//2, card_y + 190), concept["name"], fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
    
    # 描述文字 - 在卡片上居中
    draw.text((w//2, card_y + 270), concept["desc"], fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # 核心要点 - 在卡片上居中
    draw.text((w//2, card_y + 350), f"✨ {concept['key_point']}", fill=COLORS['white'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    # 侧边装饰条（右侧对齐，不遮挡）
    for i, col in enumerate([COLORS['agent'], COLORS['skill'], COLORS['rag']]):
        y_pos = 300 + i * 140
        draw.rounded_rectangle([w-80, y_pos, w-20, y_pos+50], radius=10, fill=col)
    
    # 底部进度条（居中）
    progress_bar(draw, w, h, idx+1, len(AI_SEVEN_SWORDS_CONTENT["concepts"]) + 2)
    
    return img


def create_summary_scene(topic):
    """Scene 9: 总结记忆口诀 - 所有内容在卡片上"""
    w, h = 1920, 1080
    img = create_gradient_bg(w, h)
    draw = ImageDraw.Draw(img)
    
    # 大总结卡片（居中）- 容纳所有内容
    card_w, card_h = 1300, 450
    card_x = w//2 - card_w//2
    card_y = h//2 - card_h//2
    
    # 阴影
    draw.rounded_rectangle([card_x-15, card_y-15, card_x+card_w+15, card_y+card_h+15], 
                          radius=30, fill=(0,0,0,100))
    
    # 卡片主体（深蓝背景）
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], 
                          radius=30, fill=COLORS['primary'])
    
    # 标题 - 在卡片上居中
    text_with_glow(draw, "💡 记忆口诀", (w//2, card_y + 70), COLORS['rag'], GLOBAL_FONTS['title'])
    
    # 分隔线
    gradient_line(draw, w//2-250, card_y + 140, w//2+250, card_y + 140, COLORS['accent'])
    
    # 分两行显示总结 - 在卡片上居中
    summary = AI_SEVEN_SWORDS_CONTENT["summary"]
    half_len = len(summary) // 2
    line1 = summary[:half_len]
    line2 = summary[half_len:]
    
    draw.text((w//2, card_y + 210), line1, fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    draw.text((w//2, card_y + 270), line2, fill=COLORS['gray_light'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # 额外说明 - 在卡片上居中
    extra_text = "Agent=CEO | Skill=工具包 | RAG=查资料 | MCP=插座"
    draw.text((w//2, card_y + 350), extra_text, fill=COLORS['gray_light'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    extra_text2 = "LSP=代码助手 | ACP 协议=团队协作 | ACP 上下文=背景注入"
    draw.text((w//2, card_y + 395), extra_text2, fill=COLORS['gray_light'], font=GLOBAL_FONTS['extra_small'], anchor="mm")
    
    # 版权信息 - 单独小卡片在底部
    footer_y = h - 70
    footer_w = 800
    footer_x = w//2 - footer_w//2
    draw.rounded_rectangle([footer_x, footer_y, footer_x+footer_w, footer_y+50], radius=15, fill=(30,30,50,200))
    draw.text((w//2, footer_y+25), "© 2026 Knowledge Explainer | OpenClaw AI", 
              fill=COLORS['gray_dark'], font=GLOBAL_FONTS['extra_small'], anchor="mm")
    
    return img


def generate_ai_seven_swords_video(topic, output_path=None, fps=30):
    """生成 AI 七剑客视频"""
    
    if not output_path:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_base = os.path.join(skill_dir, "output", topic)
        os.makedirs(output_base, exist_ok=True)
        output_path = os.path.join(output_base, f"{topic}_v5.5_centered.mp4")
    
    # 动态计算帧数
    title_frames = 90           # 标题 3 秒 (3*30)
    summary_frames = 120        # 总结 4 秒 (4*30)
    concept_frames_each = 90    # 每个概念 3 秒 (3*30)
    total_concepts = len(AI_SEVEN_SWORDS_CONTENT["concepts"])
    total_frames = title_frames + total_concepts * concept_frames_each + summary_frames
    
    frame_dir = os.path.join(os.path.dirname(output_path), "frames_7swords_v5.5")
    os.makedirs(frame_dir, exist_ok=True)
    
    print(f"🎬 AI 七剑客视频生成器 v5.5 (居中对齐版)")
    print(f"   • 主题：{topic}")
    print(f"   • 总概念数：{total_concepts}")
    print(f"   • 总帧数：{total_frames} (时长：{total_frames/fps:.1f}s)")
    print(f"   • 字体：{FONT_NAME}")
    print(f"   • 渲染模式：居中锚点 (anchor='mm')")
    
    # 生成帧
    for frame_num in range(total_frames):
        if frame_num < title_frames:
            img = create_title_scene(topic)
        elif frame_num < title_frames + total_concepts * concept_frames_each:
            idx = (frame_num - title_frames) // concept_frames_each
            img = create_concept_scene(topic, idx)
        else:
            img = create_summary_scene(topic)
        
        frame_path = os.path.join(frame_dir, f"frame_{frame_num:04d}.png")
        img.save(frame_path, "PNG")
        
        if frame_num % 100 == 0:
            print(f"   • 进度：{int(100*frame_num/total_frames)}%")
    
    # FFmpeg 合并
    input_pattern = os.path.join(frame_dir, "frame_%04d.png")
    cmd = ["ffmpeg", "-y", "-framerate", str(fps), "-i", input_pattern, 
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", output_path]
    
    print("🔄 正在合并帧为视频（高质量编码）...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 清理临时文件
    import shutil
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)
    
    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024*1024)
        print(f"✅ AI 七剑客视频生成成功：{output_path}")
        print(f"   • 大小：{size_mb:.2f} MB")
        print(f"   • 时长：{total_frames/fps:.1f}秒")
        print(f"   • 质量：CRF18 高保真 + 居中对齐")
        return output_path
    else:
        print(f"❌ FFmpeg 失败：{result.stderr}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        topic = "AI_SEVEN_SWORDS"
    else:
        topic = sys.argv[1]
    
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 70)
    print(f"🎬 AI 七剑客教学视频生成器 v5.5 (居中对齐版)")
    print("=" * 70)
    print(f"✅ 字体：{FONT_NAME}")
    if output_path:
        print(f"📁 输出路径：{output_path}")
    print()
    
    generate_ai_seven_swords_video(topic, output_path)
    
    print()
    print("=" * 70)
    print("✅ AI 七剑客视频生成完成！")
    print("=" * 70)
