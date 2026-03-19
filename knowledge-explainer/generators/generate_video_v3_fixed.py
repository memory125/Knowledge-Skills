#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四剑客概念视频生成器 v3.0 - 分段展示版 (修复透明度问题)
"""

import subprocess
from PIL import Image, ImageDraw, ImageFont
import os

def load_chinese_fonts():
    """加载最美的中文字体 - Google Noto Sans/Serif CJK (思源系列)"""
    try:
        # 使用 Google Noto Sans CJK (思源黑体) - 现代简约，清晰易读
        font_title = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 72)  # Bold 粗体
        font_subtitle = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 56)  # Regular 常规
        font_text = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 32)
        return {'title': font_title, 'subtitle': font_subtitle, 'text': font_text, 'small': font_small}, "Noto Sans CJK (思源黑体)"
    except:
        try:
            # 备用：Noto Serif CJK (思源宋体) - 传统优雅
            font_title = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", 72)
            font_subtitle = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 56)
            font_text = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 40)
            font_small = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 32)
            return {'title': font_title, 'subtitle': font_subtitle, 'text': font_text, 'small': font_small}, "Noto Serif CJK (思源宋体)"
        except:
            # 最终回退：uming/ukai
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/arphic/uming.ttc", 40)
                return {k: font for k in ['title', 'subtitle', 'text', 'small']}, "uming.ttc"
            except:
                default_font = ImageFont.load_default()
                return {k: default_font for k in ['title', 'subtitle', 'text', 'small']}, "default"

# 全局字体和颜色配置
GLOBAL_FONTS, FONT_NAME = load_chinese_fonts()

COLORS = {
    'bg': '#1a1a2e',
    'agent': '#e94560',
    'skill': '#0f3460',
    'rag': '#16213e',
    'mcp': '#533483',
    'white': '#ffffff',
    'gray_light': '#cccccc',  # 替代 rgba(255,255,255,0.7)
    'gray_med': '#dddddd',     # 替代 rgba(255,255,255,0.8)
    'gray_dark': '#666666'     # 替代 rgba(255,255,255,0.4)
}

def create_scene_title(progress):
    """Scene 1: 标题开场 (0-3s)"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    alpha_factor = min(progress / 0.15, 1) if progress < 0.15 else 1
    
    # 主标题
    if alpha_factor > 0.1:
        draw.text((width // 2, 280), "📚 MCP, RAG, Agent, Skill", 
                  fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
    
    # 副标题
    if alpha_factor > 0.5:
        draw.text((width // 2, 400), "四剑客深度解析", 
                  fill=COLORS['agent'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # 底部提示
    if progress > 0.10:
        draw.rounded_rectangle([200, 700, width - 200, 800], radius=20, fill=COLORS['skill'])
        draw.text((width // 2, 750), "MCP | RAG | Agent | Skill", 
                  fill=COLORS['gray_light'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    return img

def create_agent_scene(progress):
    """Scene 2: Agent 详解 (3-7s)"""
    width, height = 1920, 1080
    local_progress = (progress - 0.15) / 0.20
    
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # 场景标题
    draw.text((width // 2, 80), "第 1 剑：Agent", fill=COLORS['agent'], font=GLOBAL_FONTS['title'], anchor="mm")
    draw.text((width // 2, 180), "智能体 · CEO 级别", fill=COLORS['gray_light'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # Agent 卡片
    if local_progress > 0:
        draw.rounded_rectangle([width//2-350, 280, width//2+350, 480], radius=20, fill=COLORS['agent'])
        draw.text((width // 2, 320), "🤖", fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
        draw.text((width // 2, 390), "Agent", fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # 特点列表
    features = ["✅ 能独立决策和行动", "✅ 接受目标，自动规划", "✅ 像 CEO 一样指挥团队"]
    for i, feat in enumerate(features):
        if local_progress > i * 0.2:
            draw.text((width // 2, 560 + i * 65), feat, fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # 导航条
    draw.rectangle([0, height-80, width, height], fill=COLORS['skill'])
    draw.text((width // 2, height - 40), "Agent ▮ Skill ◯ RAG ◯ MCP", fill=COLORS['gray_light'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img

def create_skill_scene(progress):
    """Scene 3: Skill 详解 (7-11s)"""
    width, height = 1920, 1080
    local_progress = (progress - 0.35) / 0.20
    
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    draw.text((width // 2, 80), "第 2 剑：Skill", fill=COLORS['skill'], font=GLOBAL_FONTS['title'], anchor="mm")
    draw.text((width // 2, 180), "技能 · 工具包", fill=COLORS['gray_light'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    if local_progress > 0:
        draw.rounded_rectangle([width//2-350, 280, width//2+350, 480], radius=20, fill=COLORS['skill'])
        draw.text((width // 2, 320), "🛠️", fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
        draw.text((width // 2, 390), "Skill", fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    features = ["✅ 封装好的功能模块", "✅ 被动调用，不主动思考", "✅ 像螺丝刀/锤子一样"]
    for i, feat in enumerate(features):
        if local_progress > i * 0.2:
            draw.text((width // 2, 560 + i * 65), feat, fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    draw.rectangle([0, height-80, width, height], fill=COLORS['rag'])
    draw.text((width // 2, height - 40), "Agent ▮ Skill ▮ RAG ◯ MCP", fill=COLORS['gray_light'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img

def create_rag_scene(progress):
    """Scene 4: RAG 详解 (11-15s)"""
    width, height = 1920, 1080
    local_progress = (progress - 0.55) / 0.20
    
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    draw.text((width // 2, 80), "第 3 剑：RAG", fill=COLORS['rag'], font=GLOBAL_FONTS['title'], anchor="mm")
    draw.text((width // 2, 180), "检索增强生成 · 有依据", fill=COLORS['gray_light'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    if local_progress > 0:
        draw.rounded_rectangle([width//2-350, 280, width//2+350, 480], radius=20, fill=COLORS['rag'])
        draw.text((width // 2, 320), "📚", fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
        draw.text((width // 2, 390), "RAG", fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    features = ["✅ 先检索，再生成", "✅ 避免幻觉，有依据", "✅ 像资料库 + 专家"]
    for i, feat in enumerate(features):
        if local_progress > i * 0.2:
            draw.text((width // 2, 560 + i * 65), feat, fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    draw.rectangle([0, height-80, width, height], fill=COLORS['mcp'])
    draw.text((width // 2, height - 40), "Agent ▮ Skill ▮ RAG ▮ MCP", fill=COLORS['gray_light'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img

def create_mcp_scene(progress):
    """Scene 5: MCP 详解 (15-18s)"""
    width, height = 1920, 1080
    local_progress = (progress - 0.75) / 0.15
    
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    draw.text((width // 2, 80), "第 4 剑：MCP", fill=COLORS['mcp'], font=GLOBAL_FONTS['title'], anchor="mm")
    draw.text((width // 2, 180), "模型上下文协议 · 连万物", fill=COLORS['gray_light'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    if local_progress > 0:
        draw.rounded_rectangle([width//2-350, 280, width//2+350, 480], radius=20, fill=COLORS['mcp'])
        draw.text((width // 2, 320), "🌉", fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
        draw.text((width // 2, 390), "MCP", fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    features = ["✅ 统一连接协议", "✅ AI ↔ 数据/工具", "✅ 像通用 USB 接口"]
    for i, feat in enumerate(features):
        if local_progress > i * 0.2:
            draw.text((width // 2, 560 + i * 65), feat, fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    draw.rectangle([0, height-80, width, height], fill=COLORS['bg'])
    draw.text((width // 2, height - 40), "Agent ▮ Skill ▮ RAG ▮ MCP ✓", fill=COLORS['gray_light'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img

def create_summary_scene(progress):
    """Scene 6: 记忆口诀 (18-20s)"""
    width, height = 1920, 1080
    local_progress = (progress - 0.90) / 0.10
    
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    if local_progress > 0:
        draw.text((width // 2, 150), "💡 记忆口诀", fill=COLORS['agent'], font=GLOBAL_FONTS['title'], anchor="mm")
    
    comparisons = [
        ("Agent", "CEO", COLORS['agent']),
        ("Skill", "工具", COLORS['skill']),
        ("RAG", "资料库", COLORS['rag']),
        ("MCP", "桥梁", COLORS['mcp'])
    ]
    
    card_w, card_h = 400, 180
    gap = 60
    start_x = (width - 4 * card_w - 3 * gap) // 2
    
    for i, (name, meaning, color) in enumerate(comparisons):
        if local_progress > i * 0.25:
            x = start_x + i * (card_w + gap)
            draw.rounded_rectangle([x, 350, x+card_w, 350+card_h], radius=15, fill=color)
            draw.text((x + card_w//2, 420), name, fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
            draw.text((x + card_w//2, 480), f"= {meaning}", fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    if local_progress > 0.7:
        draw.rounded_rectangle([150, 650, width-150, 800], radius=20, fill='#b83247')
        summary = "Agent 能决策 | Skill 被调用 | RAG 有依据 | MCP 连万物"
        draw.text((width // 2, 725), summary, fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    draw.text((width // 2, 1000), "© 2026 Knowledge Explainer v3.0 | OpenClaw AI", fill=COLORS['gray_dark'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img

def create_frame(frame_num, total_frames):
    """根据帧号创建对应场景"""
    progress = frame_num / total_frames
    
    if progress < 0.15:
        return create_scene_title(progress)
    elif progress < 0.35:
        return create_agent_scene(progress)
    elif progress < 0.55:
        return create_skill_scene(progress)
    elif progress < 0.75:
        return create_rag_scene(progress)
    elif progress < 0.90:
        return create_mcp_scene(progress)
    else:
        return create_summary_scene(progress)

def generate_video():
    """生成完整视频"""
    output_dir = "output"
    total_frames = 600
    fps = 30
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎬 开始生成分场景视频...")
    print(f"   • 总帧数：{total_frames}")
    print(f"   • 时长：{total_frames/fps:.1f}秒")
    print(f"   • 场景：6 个 (标题/Agent/Skill/RAG/MCP/总结)")
    print()
    
    for frame_num in range(total_frames):
        img = create_frame(frame_num, total_frames)
        frame_path = os.path.join(output_dir, f"frame_{frame_num:04d}.png")
        img.save(frame_path, "PNG")
        
        if frame_num % 60 == 0:
            print(f"   • 进度：{int(100*frame_num/total_frames)}%")
    
    # FFmpeg 合并
    input_pattern = os.path.join(output_dir, "frame_%04d.png")
    output_mp4 = os.path.join(output_dir, "four_heroes_v3.mp4")
    
    print("🔄 正在合并帧为视频...")
    cmd = ["ffmpeg", "-y", "-framerate", str(fps), "-i", input_pattern, 
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", output_mp4]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        size_mb = os.path.getsize(output_mp4) / (1024*1024)
        print(f"✅ 视频生成成功：{output_mp4}")
        print(f"   • 大小：{size_mb:.2f} MB")
        return output_mp4
    else:
        print(f"❌ 失败:")
        print(result.stderr)
        return None

if __name__ == "__main__":
    print("=" * 70)
    print("🎬 四剑客概念视频生成器 v3.0 - 分场景展示版")
    print("=" * 70)
    print(f"✅ 字体：{FONT_NAME}")
    print()
    
    mp4_path = generate_video()
    
    if mp4_path:
        print()
        print("=" * 70)
        print("✅ 视频生成完成！")
        print("=" * 70)
        print(f"📁 {mp4_path}")
        print()
        print("📊 场景结构:")
        print("   0-3s:   标题开场")
        print("   3-7s:   Agent 详解")
        print("   7-11s:  Skill 详解")
        print("   11-15s: RAG 详解")
        print("   15-18s: MCP 详解")
        print("   18-20s: 记忆口诀总结")
