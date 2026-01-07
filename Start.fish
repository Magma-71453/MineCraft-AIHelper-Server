#!/usr/bin/env fish

source ~/MC-AiChat/bin/activate.fish

read -P "请选择 MC tmux 会话: " MC_SERVER
set -gx MC_SERVER $MC_SERVER

set last_msg ""

echo "开始监听 @悦灵 ……"

while true
    # 直接在管道里处理，避免 fish 拆变量
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

    # 去重（用整行文本，宽松但可靠）
    if test "$line" = "$last_msg"
        sleep 1
        continue
    end
    set last_msg "$line"

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
