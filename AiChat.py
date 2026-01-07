#!/usr/bin/env python3
import sys
import os
import json
import subprocess
import openai

# ===== OpenAI 配置 =====
openai.api_key = os.getenv("OPENAI_API_KEY", "Your-Key")
openai.base_url = os.getenv("OPENAI_API_BASE", "https://free.v36.cm/v1/")

# ===== 数据库 =====
DB_PATH = "./Lang/mc_zh_en_db.json"

with open(DB_PATH, "r", encoding="utf-8") as f:
    MC_DB = json.load(f)

def find_keyword(question: str):
    """滑动窗口中文匹配"""
    hits = []
    for name in MC_DB.keys():
        if name in question:
            hits.append(name)
    return hits

def fetch_wiki(en_name: str):
    try:
        out = subprocess.check_output(
            ["python3", "WikiSearch.py", en_name],
            stderr=subprocess.DEVNULL,
            timeout=8
        ).decode().strip()
        return out if out != "missing" else None
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        return

    question = sys.argv[1].strip()
    if not question:
        return

    print(f"[DEBUG] 玩家问题: {question}", file=sys.stderr)

    keywords = find_keyword(question)
    wikidata = None
    en_name = None

    if keywords:
        key = keywords[0]
        entry = MC_DB[key]
        en_name = entry["en"]

        print(f"[DEBUG] 命中关键词: {key} → {en_name}", file=sys.stderr)

        wikidata = fetch_wiki(en_name)

        if wikidata:
            print(f"[DEBUG] Wiki 数据获取成功（{len(wikidata)} 字）", file=sys.stderr)
        else:
            print("[DEBUG] Wiki 数据缺失", file=sys.stderr)

    # ===== 构造 Prompt =====
    system_prompt = (
        "你是 Minecraft Java 版 1.21.x 的服务器 AI 助手。"
        "只允许依据提供的资料回答，不得编造。"
        "语言简洁，适合游戏聊天框。"
    )

    user_prompt = f"玩家提问：{question}\n"

    if wikidata:
        user_prompt += f"\n【权威资料】\n{wikidata}\n"
        user_prompt += "\n请基于以上资料回答玩家问题。"
    else:
        user_prompt += "\n请基于你的已知常识回答，若不确定请说明。"

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

        answer = completion.choices[0].message.content.strip()
        print(answer.replace("\n", " "))

    except Exception as e:
        print("这个问题暂时无法回答。")

if __name__ == "__main__":
    main()
