# AI Multi-Agent Automation System

多智能体 AI 自动化系统，用于提升研发与数据处理流程效率。该系统实现了一个任务驱动的多 Agent 协作架构，集成了大模型（OpenAI LLM）、本地代码执行、数据检索分析与 GitHub 自动化，无缝串联研发闭环，降低人工参与度。

## 核心特性

- 多 Agent 协作：主 Agent 负责任务理解、拆解与调度，子 Agent 专注信息检索、内容生成、代码分析执行等分工。
- Chain of Thought：支持链式推理，增强复杂任务的稳定性与可解释性。
- Tool Use 能力：可调用本地环境、数据接口与 GitHub API，实现全自动联动。
- GitHub 集成：自动化问题解决、PR 检查、代码审查与修复。
- 本地代码执行与安全沙箱。
- 数据采集、检索与分析能力。
- Docker 一键部署、扩展性强。

## 项目结构

```
.
├── agent/               # 主 Agent 及子 Agent 实现
│   ├── subagents/       # 领域子 Agent，各司其职
│   └── subagent_base.py # 子 Agent 抽象基类
├── tools/               # 本地执行、数据/代码检索、GitHub工具
├── utils/               # 工具与辅助代码
├── tests/               # 测试代码
├── config.py            # 全局配置（OpenAI key、GitHub token等）
├── main.py              # 系统启动入口
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 快速开始

### 1. 配置环境

```shell
cp config.py.example config.py
# 编辑 config.py，填入 OpenAI API Key、GitHub Token 等
```

### 2. 本地运行

```shell
pip install -r requirements.txt
python main.py
```

### 3. Docker 部署

```shell
docker-compose up --build
```

### 4. 主要用例

- 任务自动分解与跟踪
- 数据自动采集、预处理、分析
- 代码生成、代码自动修复与审查
- 跨 Agent 联动复杂任务执行
- GitHub 自动化集成（如自动开/关 issue、自动审查 PR 等）

## 后续开发

- 集成更多 LLM，如 ChatGLM、Qwen 等（可参考 agent/ 子 Agent 结构进行扩展）
- 增加更多类型子 Agent（如知识学习、数据可视化等）
- 强化 Agent 间的消息通信与协作管理
- 进一步优化安全策略和运行隔离

## 许可证

MIT License

---

欢迎 issue、PR 与合作！
