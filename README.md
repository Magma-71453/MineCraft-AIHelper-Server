# MineCraft-AIHelper-Server

一个轻量级的 Minecraft 服务器 AI 助手工具，支持任何兼容 OpenAI API 的模型。
## 功能特性

- 🤖 智能信息整理 - AI 作为图书管理员，整合并呈现 Wiki 权威信息
- 📚 自动 Wiki 查询 - 检测游戏关键词自动搜索 Minecraft Wiki
- ⚡ 高效监听机制 - 通过 tmux capture-pane 实时捕获玩家消息
- 🔌 模型灵活 - 无需高性能模型，基础文本处理能力即可

## 工作原理
```
玩家消息 → tmux capture-pane 实时监听
              ↓
    检测到游戏关键词（如"钻石"、"creeper"）
              ↓
    查询 /Lang/mc_zh_en_db.json 获取游戏 ID
              ↓
    WikiSearch.py 向 Minecraft Wiki 提交查询
              ↓
    获取 Wiki 权威信息
              ↓
    AiChat.py 整理并呈现信息
              ↓
    回复发送至游戏聊天
```

### 关于 AI 模型选择

**本工具不需要高性能 AI 模型！** 由于主要信息来自 Minecraft Wiki 的权威数据，AI 仅需具备基本的文本整理和分析能力，因此，即使是较小的模型也能胜任此任务。

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

## 快速开始

### 1. 创建 Python 虚拟环境

现代 Linux 系统要求使用虚拟环境管理 Python 包：
```bash
# 创建虚拟环境
python3 -m venv ~/minecraft-ai-venv

# 激活虚拟环境
source ~/minecraft-ai-venv/bin/activate

# 安装依赖
pip install openai requests
```

### 2. 配置虚拟环境路径

编辑 `Start.fish` 第 3 行，将路径修改为你创建的虚拟环境：
```fish
source ~/minecraft-ai-venv/bin/activate.fish
```

### 3. 配置 API 密钥

编辑 `AiChat.py`，填入你的 OpenAI API Key：
```python
OPENAI_KEY = "your-api-key-here"
```

### 4. 启动服务
```bash
fish Start.fish
```

或使用其他 shell：
```bash
bash -c "fish Start.fish"
```

### 5. 开始使用

玩家在游戏中提及游戏物品、生物或机制时，AI 助手会自动查询 Wiki 并整理相关信息进行回复。

## 技术细节

- **消息监听**: 使用 `tmux capture-pane` 捕获服务器日志
- **关键词检测**: 自动识别游戏相关词汇
- **数据库索引**: 通过 `./Lang/mc_zh_en_db.json` 快速定位游戏 ID
- **Wiki 查询**: `WikiSearch.py` 提交查询并获取权威信息
- **信息整理**: AI 将 Wiki 内容整理为易读的回复

## 文件说明

- `Start.fish` - 主程序，负责 tmux 监听和消息转发
- `AiChat.py` - AI 交互核心，整理 Wiki 信息
- `WikiSearch.py` - Minecraft Wiki 查询模块
- `Lang/mc_zh_en_db.json` - 游戏物品/实体 ID 数据库
- `Lang/` - 多语言支持文件

## 许可证

MIT License