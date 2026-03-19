#!/usr/bin/env python3
"""
PNG 序列转 MP4 视频工具
用于将 Blender 渲染的 PNG 序列合成为最终 MP4 视频

用法：python png_to_mp4.py --input-dir /path/to/png/folder --output output.mp4
"""

import subprocess
import sys
import os
from pathlib import Path

def convert_png_to_mp4(input_dir, output_file, fps=30, crf=23):
    """
    将 PNG 序列转换为 MP4 视频
    
    Args:
        input_dir: PNG 序列所在目录
        output_file: 输出 MP4 文件路径
        fps: 帧率（默认 30）
        crf: 编码质量（18-28，越小质量越高，默认 23）
    """
    input_path = Path(input_dir)
    
    # 检查目录是否存在
    if not input_path.exists():
        print(f"错误：输入目录不存在 {input_dir}")
        return False
    
    # 检查 PNG 文件
    png_files = list(input_path.glob("frame_*.png"))
    if not png_files:
        print(f"错误：在 {input_dir} 中未找到 PNG 序列")
        return False
    
    print(f"发现 {len(png_files)} 帧 PNG")
    
    # FFmpeg 命令
    cmd = [
        'ffmpeg',
        '-y',  # 覆盖输出文件
        '-framerate', str(fps),
        '-i', os.path.join(input_dir, 'frame_%04d.png'),
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', str(crf),
        '-pix_fmt', 'yuv420p',
        output_file
    ]
    
    print(f"开始转换：{output_file}")
    print(f"命令：{' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ 转换成功！输出：{output_file} ({file_size:.2f} MB)")
            return True
        else:
            print(f"❌ 转换失败:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("错误：未找到 ffmpeg，请先安装：sudo apt install ffmpeg")
        return False
    except Exception as e:
        print(f"错误：{e}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='PNG 序列转 MP4')
    parser.add_argument('--input-dir', required=True, help='PNG 序列目录')
    parser.add_argument('--output', required=True, help='输出 MP4 文件路径')
    parser.add_argument('--fps', type=int, default=30, help='帧率（默认 30）')
    parser.add_argument('--crf', type=int, default=23, help='编码质量 CRF（18-28，默认 23）')
    
    args = parser.parse_args()
    
    success = convert_png_to_mp4(args.input_dir, args.output, args.fps, args.crf)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
