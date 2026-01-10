# MineCraft-AIHelper-Server

一个轻量级、高性能的 Minecraft 服务器 AI 助手工具。它不仅能通过 AI 与玩家聊天，还能作为“图书管理员”，自动查询 Minecraft Wiki 的权威资料来回答游戏问题。

**✨ 本版本新增特性：消息哈希去重验证 & 本地数据缓存系统。**

## 🌟 功能特性

- **🤖 智能问答**：基于 OpenAI API（支持 GPT-4o-mini 等模型），通过游戏内聊天框回复玩家。
- **🛡️ 智能防抖（新）**：在 `Start.fish` 中引入 MD5 哈希验证，确保同一条消息不会被重复处理，避免 AI 刷屏 [6]。
- **🚀 极速响应（新）**：引入 `./Cache/` 本地缓存机制。查询过的 Wiki 资料会永久保存，下次询问相同物品时直接秒回，无需等待网络请求。
- **📚 权威资料**：检测到游戏关键词（如“钻石”、“苦力怕”）时，自动抓取 Minecraft Wiki 数据作为 AI 回答的依据，拒绝瞎编 [1, 2]。
- **🔌 低资源占用**：本地仅作为服务器日志监听，通过 `tmux` 监听日志并把玩家消息发送openai，轻量高效 [1, 2]。

## 🛠️ 工作流程

得益于新的优化机制，系统现在的处理流程更加严谨高效：

1.  **监听与去重 (`Start.fish`)**:
    *   通过 `tmux capture-pane` 实时捕获服务器日志 [1, 2, 6]。
    *   **[哈希校验]** 计算消息内容的 MD5 值，与上一条记录对比。如果哈希值相同，直接跳过（防止重复回复）[6]。
2.  **关键词匹配 (`AiChat.py`)**:
    *   接收问题，并在 `Lang/mc_zh_en_db.json` 数据库中查找是否包含游戏物品/生物的关键词 [1, 4]。
3.  **缓存优先查询**:
    *   **[检查缓存]** 系统优先检查 `./Cache/` 目录下是否有对应的资料文件 [4, 7]。
    *   **[命中]** 如果存在，直接读取本地文件（速度极快）。
    *   **[未命中]** 如果不存在，调用 `WikiSearch.py` 发起网络请求 [4]。
4.  **数据获取与存储 (`WikiSearch.py`)**:
    *   从 Minecraft Wiki API 下载数据 [7]。
    *   **[写入缓存]** 将清洗后的文本自动保存到 `./Cache/`，供下次使用 [7]。
5.  **AI 生成与回复**:
    *   将玩家问题 + Wiki 资料（如果有）发送给 AI 模型 [4]。
    *   AI 生成简洁的回答，通过 `tmux send-keys` 发送到游戏内 [1, 6]。

## 🚀 快速开始

### 1. 创建 Tmux 会话与运行 Minecraft 服务器

为了让 `Start.fish` 脚本能够稳定监听服务器日志，请确保您的 Minecraft 服务器运行在一个 Tmux 会话中。

**操作步骤：**

1.  **SSH 登录到您的服务器。**
2.  **创建一个新的 Tmux 会话：**
    ```bash
    tmux new-session -t mc
    ```
    这里的 `mc` 是会话的名称，您可以自定义。
3.  **在 Tmux 会话中启动 Minecraft 服务器：**
    进入您的 Minecraft 服务器目录，然后使用您的服务器启动命令（例如 `java -Xmx1024M -Xms1024M -jar server.jar nogui`）。
    ```bash
    # 示例：进入服务器目录并启动
    cd /path/to/your/minecraft/server
    java -Xmx1024M -Xms1024M -jar server.jar nogui
    ```
4.  **分离 Tmux 会话 (可选):**
    按下 `Ctrl+b` 然后按 `d` 键，可以将 Tmux 会话置于后台运行，您仍然可以继续执行其他命令。

### 2. 安装与配置

#### 2.1. 克隆项目与环境配置

```bash
# 假设您已将项目文件下载到服务器上的 MineCraft-AIHelper-Server 目录
cd MineCraft-AIHelper-Server

# 创建 Python 虚拟环境 (推荐)
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装 Python 依赖
pip install openai requests
```

#### 2.2. 配置虚拟环境路径

编辑 `Start.fish` 文件，将第 3 行的虚拟环境激活路径修改为您实际创建的虚拟环境路径：

```fish
# Start.fish (第 3 行)
source ./venv/bin/activate.fish  # 确保这里的路径正确
```

#### 2.3. 配置 API 密钥

编辑 `AiChat.py` 文件，找到 OpenAI 配置部分，填入您的 OpenAI API Key 和 Base URL（如果使用转发服务）。

```python
# AiChat.py
# 示例：
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-xxxxxxxx") # 或者直接填写你的 API Key
openai.base_url = os.getenv("OPENAI_API_BASE", "https://free.v36.cm/v1/") # 如果使用第三方 API 服务
```

### 3. 启动 AI 助手服务

在您的服务器上，进入项目目录，然后运行启动脚本：

```bash
# 使用 Fish Shell 直接运行
fish Start.fish
```

或在其他 Shell 环境中运行：

```bash
bash -c "fish Start.fish"
```

**运行后的步骤：**
1.  脚本启动后，会提示您输入或选择 Minecraft 服务器所在的 Tmux 会话名称（在步骤 1 中创建的 `mc` 会话）。
2.  输入会话名称后，脚本将开始监听 `@悦灵`（或您在 `Start.fish` 中设定的其他触发词）。

### 4. 开始使用

当玩家在游戏内聊天框提及游戏物品、生物、机制等，并且消息被 `Start.fish` 捕获后（例如，消息包含 `@悦灵 钻石怎么合成？`），AI 助手会自动查询 Wiki（优先查本地缓存），并将整理后的信息回复到游戏聊天框中。

## 📂 文件说明

-   `Start.fish`: **主控脚本**。负责通过 Tmux 监听服务器日志，进行消息哈希去重，调用 Python 脚本，并将 AI 的回复发送回游戏。
-   `AiChat.py`: **AI 核心逻辑**。负责处理玩家的问题，匹配关键词，优先从本地缓存读取 Wiki 数据，若缓存中不存在则调用 `WikiSearch.py`，最后构建 Prompt 发送给 OpenAI API。
-   `WikiSearch.py`: **Wiki 查询模块**。负责联网从 Minecraft Wiki API 查询指定条目信息，并将结果保存到本地缓存。
-   `Lang/mc_zh_en_db.json`: **关键词数据库**。存储了 Minecraft 中文物品/实体名称与对应 Wiki 英文条目的映射关系。
-   `Cache/`: **本地缓存目录**。自动创建，用于存放从 Wiki 下载并处理后的文本数据，以加速后续查询。

## 📝 常见问题

**Q: 如何清空或更新 Wiki 缓存？**
A: 直接删除 `./Cache/` 目录下的所有 `.txt` 文件即可。下次查询时，系统会重新从 Wiki 获取并缓存最新数据。

**Q: 为什么 AI 没有回复？**
1.  **Tmux 会话检查**: 确认 `Start.fish` 脚本中的 Tmux 会话名称是否正确。
2.  **触发词检查**: 确认玩家的消息中是否包含正确的触发词（默认是 `@悦灵`）。
3.  **API 密钥检查**: 确保 `AiChat.py` 中的 OpenAI API Key 配置正确，并且账户有足够的额度。
4.  **网络连接**: 确认服务器能正常访问 OpenAI API 或您配置的 `openai.base_url`。

## 📜 许可证

本项目遵循 MIT License。详情请参阅 `LICENSE` 文件 [5]。
