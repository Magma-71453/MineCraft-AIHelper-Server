#!/usr/bin/env fish

source ./venv/bin/activate.fish
tmux ls
read -P "请选择 MC tmux 会话: " MC_SERVER
set -gx MC_SERVER $MC_SERVER

set last_hash ""

echo "开始监听 @悦灵 ……"

while true
    # 捕获日志
    set line (
        tmux capture-pane -t $MC_SERVER -p -S -50 |
        grep "@悦灵" |
        grep "<" |
        grep ">" |
        grep -v "\[Server\]" |
        tail -n 1
    )

    if test -z "$line"
        sleep 1
        continue
    end

    # === 优化部分：哈希去重 ===
    # 计算当前行的 MD5 哈希值 (适配 Linux md5sum 输出格式)
    set current_hash (echo -n "$line" | md5sum | cut -d ' ' -f 1)

    if test "$current_hash" = "$last_hash"
        sleep 0.5
        continue
    end

    # 更新最后一次处理的哈希值
    set last_hash "$current_hash"
    # ========================

    # 提取 @悦灵 后的内容
    set question (echo $line | sed -E 's/^.*@悦灵[ ]*//')

    if test -z "$question"
        sleep 1
        continue
    end

    echo "🔍 检测到玩家消息："
    echo "    $line"
    echo "📨 提交给 AI 的问题：$question"

    set reply (python3 AiChat.py "$question")

    if test -n "$reply"
        echo "🤖 AI 回复：$reply"
        tmux send-keys -t $MC_SERVER "say $reply" Enter
    else
        echo "⚠ AI 无返回结果"
    end

    sleep 1
end
