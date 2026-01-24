#!/usr/bin/env python3
import os
import json
import time
import random
import mwclient

# ===== 配置区域 =====
JSON_DB_PATH = "Lang/mc_zh_en_db.json"  # 你的JSON数据库路径
CACHE_DIR = "./Cache"                   # 缓存保存路径
USER_AGENT = 'MinecraftBot/1.0 (Contact: your.email.com)'
WIKI_HOST = 'zh.minecraft.wiki'
WIKI_PATH = '/'

# 确保目录存在
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def load_targets(json_path):
    """
    读取JSON数据库
    返回字典列表: items = {"中文名": "英文名", ...}
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        targets = {}
        for zh_name, info in data.items():
            if 'en' in info:
                targets[zh_name] = info['en']
        return targets
    except Exception as e:
        print(f"[错误] 读取 JSON 失败: {e}")
        return {}

def sanitize_filename(title):
    """清理文件名，虽然英文名一般很安全，但以防万一"""
    return "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()

def main():
    # 1. 加载目标数据
    target_map = load_targets(JSON_DB_PATH)
    total = len(target_map)
    print(f"=== 开始任务，共有 {total} 个物品需要检查 ===")

    if total == 0:
        return

    # 2. 初始化 Wiki 连接
    try:
        print(f"正在连接到 {WIKI_HOST} ...")
        site = mwclient.Site(WIKI_HOST, path=WIKI_PATH, clients_useragent=USER_AGENT)
    except Exception as e:
        print(f"[致命错误] 无法连接到 Wiki: {e}")
        return

    # 3. 循环处理
    # enumerate转换字典是为了方便计数
    for index, (zh_name, en_name) in enumerate(target_map.items(), 1):
        
        # --- 核心修改：文件名强制使用英文名 ---
        safe_en_name = sanitize_filename(en_name)
        cache_filename = f"{safe_en_name}.txt"
        cache_path = os.path.join(CACHE_DIR, cache_filename)

        # --- 策略：跳过已存在的文件 ---
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            # print(f"[{index}/{total}] [跳过] {zh_name} -> {cache_filename}") # 可选：为了清爽可以注释掉跳过的信息
            continue

        print(f"[{index}/{total}] [下载] {zh_name} ({en_name}) ...", end="", flush=True)

        try:
            # --- 核心修改：搜索使用中文名 ---
            page = site.pages[zh_name]

            if not page.exists:
                print(" -> 页面不存在 (Missing)")
                continue

            # 处理重定向 (例如：搜 金合欢木按钮 -> 重定向到 木按钮)
            # 我们接受这个重定向的内容，但保存的文件名依然是 Acacia Button.txt
            redirected = False
            if page.redirect:
                try:
                    target_page = page.resolve_redirect()
                    # print(f" -> 重定向到[{target_page.name}]", end="") # 调试用，可以不打出来
                    page = target_page
                    redirected = True
                except Exception:
                    print(" -> 重定向解析失败", end="")

            # 获取 WikiText
            content = page.text()

            if content:
                # 写入文件 (文件名是英文！)
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                if redirected:
                    print(f" -> 完成 (内容来自 {page.name})")
                else:
                    print(" -> 完成")
            else:
                print(" -> 内容为空")

            # 速率限制
            time.sleep(random.uniform(1.5, 3.0))

        except Exception as e:
            print(f"\n[错误] 处理 '{zh_name}' 时发生异常: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

