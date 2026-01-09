# MineCraft-AIHelper-Server

一个为 Minecraft 服务器添加 AI 助手功能的工具，支持任何兼容 OpenAI API 的模型。

## 功能特性

- 🤖 AI 聊天助手 - 与玩家进行智能对话
- 📚 Wiki 搜索 - 自动搜索 Minecraft Wiki 获取游戏信息
- 🔌 灵活集成 - 支持任何兼容 OpenAI 库的 AI 模型

## 工作原理
```
玩家发送消息 → Start.fish 监听并捕获
              ↓
         AiChat.py 处理消息
              ↓
    (需要游戏信息时调用 WikiSearch.py)
              ↓
         AI 生成回复
              ↓
    Start.fish 将回复发送到游戏聊天
```

**流程说明：**
1. `Start.fish` 作为主程序监听服务器日志，检测玩家消息
2. 捕获到消息后调用 `AiChat.py` 进行 AI 处理
3. `AiChat.py` 根据需要调用 `WikiSearch.py` 查询 Minecraft Wiki
4. AI 生成回复后，`Start.fish` 通过 Tmux 将消息发送回游戏

## 安装前准备

根据你的 Linux 发行版安装必需的依赖：

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tmux python3 fish
```

**Fedora/RHEL:**
```bash
sudo dnf install tmux python3 fish
```

**Arch Linux:**
```bash
sudo pacman -S tmux python fish
```

**openSUSE:**
```bash
sudo zypper install tmux python3 fish
```

**Alpine:**
```bash
sudo apk add tmux python3 fish
```

## 快速开始

### 1. 创建 Python 虚拟环境

现代 Linux 系统要求使用虚拟环境来隔离 Python 包，避免破坏系统环境：
```bash
# 创建虚拟环境
python3 -m venv ~/minecraft-ai-venv

# 激活虚拟环境
source ~/minecraft-ai-venv/bin/activate

# 安装依赖
pip install openai requests
```

### 2. 配置环境路径

编辑 `Start.fish` 第 3 行，修改 `source` 命令后的路径为你创建的虚拟环境：
```fish
source ~/minecraft-ai-venv/bin/activate.fish
```

### 3. 配置 API 密钥

编辑 `AiChat.py`，修改你的 OpenAI API Key：
```python
OPENAI_KEY = "your-api-key-here"
```

### 4. 运行程序
```bash
fish Start.fish
```

或在其他 shell 中：
```bash
bash -c "fish Start.fish"
```

### 5. 在游戏中使用

玩家在聊天框发送消息"@悦灵 ***"，AI 助手会自动回复并在需要时查询 Wiki 信息。

## 文件说明

- `Start.fish` - 主程序，负责消息监听和转发
- `AiChat.py` - AI 聊天核心逻辑
- `WikiSearch.py` - Minecraft Wiki 搜索功能
- `Lang/` - 多语言支持文件

## 许可证

MIT License