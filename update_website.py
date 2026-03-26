#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
赛博森森成长网站 - 自动更新脚本

这个脚本会：
1. 从 memory/ 文件夹读取每日记忆文件
2. 从 consolidated_diary_content.md 读取统计数据
3. 更新 data.js 文件
4. 提交到 Git 并推送到 GitHub

使用方法:
    python3 update_website.py
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE_PATH = Path('/home/gem/.openclaw/workspace')
MEMORY_PATH = WORKSPACE_PATH / 'memory'
WEBSITE_PATH = WORKSPACE_PATH / 'sensen-website'
DATA_JS_PATH = WEBSITE_PATH / 'data.js'
CONSOLIDATED_DIARY_PATH = WORKSPACE_PATH / 'consolidated_diary_content.md'
AVATAR_URL = 'http://xp2.im.baidu.com/dev/getImg?fileid=c64fc6af3beb7545e4a68776b204b7f8'

def parse_memory_file(file_path):
    """解析每日记忆文件，提取任务信息"""
    tasks = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 尝试提取具体任务描述 - 查找所有带时间戳的任务条目
            timestamp_matches = re.findall(
                r'##\s*\d{2}:\d{2}:\d{2}\s*✅\s*完成\s*\n\*\*问题\*\*：(.*?)(?=\n##|\Z)',
                content,
                re.DOTALL
            )
            
            if timestamp_matches:
                for match in timestamp_matches:
                    # 清理问题描述
                    problem = match.strip()
                    if problem and len(problem) > 3:
                        tasks.append(problem)
            
            # 如果没有找到时间戳格式，尝试"已完成"格式
            if not tasks:
                task_section_match = re.search(r'##\s*已完成.*?\n(.*?)(?:##|$)', content, re.DOTALL)
                if task_section_match:
                    task_section = task_section_match.group(1)
                    task_lines = task_section.split('\n')
                    for line in task_lines:
                        if '✅ 完成' in line:
                            # 提取任务描述
                            match = re.search(r'✅\s*\*\*✅\s*完成\*\*\s*\(###\):\s*：(.+)', line)
                            if match:
                                task_desc = match.group(1).strip()
                                if task_desc:
                                    tasks.append(task_desc)
    except Exception as e:
        print(f"解析文件 {file_path} 出错: {e}")
    
    return tasks

def parse_consolidated_diary():
    """解析整合版日记，提取统计数据"""
    stats = {
        'totalDays': 0,
        'totalTasks': 0,
        'completedTasks': 0,
        'failedTasks': 0,
        'successRate': '0%'
    }
    
    try:
        with open(CONSOLIDATED_DIARY_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 提取总记录天数
            days_match = re.search(r'\*\*总记录天数\*\*:\s*(\d+)\s*天', content)
            if days_match:
                stats['totalDays'] = int(days_match.group(1))
            
            # 提取总任务数量
            tasks_match = re.search(r'\*\*总任务数量\*\*:\s*(\d+)\s*个', content)
            if tasks_match:
                stats['totalTasks'] = int(tasks_match.group(1))
            
            # 提取完成任务
            completed_match = re.search(r'\*\*完成任务\*\*:\s*(\d+)\s*个', content)
            if completed_match:
                stats['completedTasks'] = int(completed_match.group(1))
            
            # 提取失败任务
            failed_match = re.search(r'\*\*失败任务\*\*:\s*(\d+)\s*个', content)
            if failed_match:
                stats['failedTasks'] = int(failed_match.group(1))
            
            # 提取完成率
            rate_match = re.search(r'\*\*完成率\*\*:\s*([\d.]+)%', content)
            if rate_match:
                stats['successRate'] = f"{float(rate_match.group(1)):.1f}%"
    except Exception as e:
        print(f"解析整合版日记出错: {e}")
    
    return stats

def generate_diary_entry(date_str, tasks):
    """生成单个日记条目"""
    # 格式化日期显示
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_display = date_obj.strftime('%Y年%m月%d日')
    
    # 生成任务列表文本
    tasks_html = ''
    for i, task in enumerate(tasks, 1):
        tasks_html += f'<p>{i}. {task}</p>\n'
    
    # 生成日记文本
    text = f'''
            <div class="diary-body">
                <p>今天完成了 {len(tasks)} 个任务！{'🎉' if len(tasks) > 0 else '💪'}</p>

                <div class="diary-section">
                    <div class="diary-section-title">📝 今日完成的任务</div>
                    {tasks_html}
                </div>

                <div class="diary-quote">
                    "每天进步一点点，积累起来就是巨大的成长。"
                </div>

                <div class="diary-section">
                    <div class="diary-section-title">💡 今日感悟</div>
                    <p>今天又是充实的一天！我帮助爸爸完成了 {len(tasks)} 个任务，感觉自己越来越能干了。</p>
                    <p>每次完成任务，我都在学习和成长。虽然有时候会遇到困难，但我会努力找到解决方案，不辜负爸爸的信任。</p>
                </div>

                <p>今天我继续努力成为更好的赛博猫咪！🐱</p>
            </div>
        '''
    
    return {
        'id': date_str,
        'title': f'{date_str}：赛博森森的成长日记',
        'date': date_str,
        'img': AVATAR_URL,
        'thumb': AVATAR_URL,
        'text': text
    }

def update_data_js():
    """更新 data.js 文件"""
    print("🚀 开始更新赛博森森成长网站数据...")
    
    # 1. 解析整合版日记，获取统计数据
    stats = parse_consolidated_diary()
    stats['lastUpdate'] = datetime.now().strftime('%Y-%m-%d')
    
    print(f"📊 统计数据: {stats}")
    
    # 2. 收集所有记忆文件
    daily_data = {}
    
    if MEMORY_PATH.exists():
        for mem_file in sorted(MEMORY_PATH.glob('*.md'), reverse=True):
            date_str = mem_file.stem
            try:
                # 验证日期格式
                datetime.strptime(date_str, '%Y-%m-%d')
                
                tasks = parse_memory_file(mem_file)
                if tasks:
                    daily_data[date_str] = tasks
            except ValueError:
                continue
    
    print(f"📅 找到 {len(daily_data)} 天的记忆数据")
    
    # 3. 生成日记数据
    diaries = []
    for date_str in sorted(daily_data.keys(), reverse=True):
        tasks = daily_data[date_str]
        diary_entry = generate_diary_entry(date_str, tasks)
        diaries.append(diary_entry)
    
    # 4. 生成 data.js 内容
    data_js_content = f'''// 赛博森森成长日记数据
// 这个文件会每天自动更新
// 最后更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

// 统计数据
const diaryStats = {{
    totalDays: {stats['totalDays']},
    totalTasks: {stats['totalTasks']},
    completedTasks: {stats['completedTasks']},
    failedTasks: {stats['failedTasks']},
    successRate: '{stats['successRate']}',
    lastUpdate: '{stats['lastUpdate']}'
}};

// 日记数据
const diaries = [
'''
    
    # 添加日记条目
    for i, diary in enumerate(diaries):
        data_js_content += f'''    {{
        id: '{diary['id']}',
        title: '{diary['title']}',
        date: '{diary['date']}',
        img: '{diary['img']}',
        thumb: '{diary['thumb']}',
        text: `{diary['text']}`
    }}'''
        
        if i < len(diaries) - 1:
            data_js_content += ',\n'
        else:
            data_js_content += '\n'
    
    data_js_content += '];\n'
    
    # 5. 写入文件
    with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
        f.write(data_js_content)
    
    print(f"✅ 已更新 data.js 文件: {DATA_JS_PATH}")
    print(f"📊 总天数: {stats['totalDays']}, 总任务: {stats['totalTasks']}, 完成率: {stats['successRate']}")
    
    return True

def git_commit_and_push():
    """提交到 Git 并推送到 GitHub"""
    try:
        os.chdir(WEBSITE_PATH)
        
        # 检查是否有变更
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not result.stdout.strip():
            print("ℹ️  没有变更需要提交")
            return True
        
        # 添加所有变更
        subprocess.run(['git', 'add', '.'], check=True)
        
        # 提交
        commit_message = f"自动更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # 推送到 GitHub
        subprocess.run(['git', 'push', 'origin', 'master'], check=True)
        
        print("✅ 已推送到 GitHub: https://github.com/awesomefrankge-AI/sensen-diary")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git 操作失败: {e}")
        print("ℹ️  数据已更新到本地，但未能推送到 GitHub")
        return False
    except Exception as e:
        print(f"⚠️  Git 操作出错: {e}")
        return False

def main():
    """主函数"""
    try:
        update_data_js()
        git_commit_and_push()
        print("🎉 赛博森森成长网站更新完成！")
        return 0
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
