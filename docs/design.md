# AI Research Assistant CLI 设计文档

## 1. 项目目标

面向学习和科研笔记的 AI 命令行工具。用户可以输入 .txt 或 .md 文件，让工具生成摘要、回答问题、生成后续学习任务。

## 2. 架构概述

```text
用户输入 → CLI 解析 → 文件读取 → Prompt 构建 → AI 处理 → 结果输出
                ↓                                      ↓
            配置管理（环境变量）                    [可选] 保存到文件
```

CLI 入口（cli.py）负责解析命令行参数，调用文件读取模块（file_loader.py）加载文件内容，然后通过 prompt 构建模块（prompts.py）生成结构化 prompt，再通过 AI 客户端（ai_client.py）处理内容，最后输出结果。配置模块（config.py）负责从环境变量读取配置。输出模块（output_writer.py）负责将结果保存到文件。

## 3. 模块设计

### cli.py — CLI 入口

- 使用 argparse 解析命令行参数
- 支持子命令：summarize, ask, tasks, history
- 支持 --save 参数保存输出到文件
- 支持 --verbose/-v 全局参数启用调试日志
- 调用其他模块完成实际工作
- 统一捕获 ResearchAssistantError，输出友好的 Error 消息
- 未知异常默认输出通用提示；verbose 模式显示完整 traceback
- 不直接调用 Anthropic SDK

### exceptions.py — 自定义异常

- 定义异常层次结构：ResearchAssistantError → FileLoadError, ConfigError, AIClientError, OutputWriteError
- 所有异常继承自 ResearchAssistantError，由 cli.py 统一捕获

### logger.py — 日志配置

- 使用 Python 标准库 logging
- setup_logger(verbose) 配置日志级别（WARNING 或 DEBUG）
- get_logger() 获取已配置的 logger 实例

### config.py — 配置管理

- 从环境变量读取配置
- 提供默认值（mock 模式）
- 验证配置有效性
- 支持的环境变量：
  - `RESEARCH_ASSISTANT_MODE`：AI 模式（mock/real）
  - `ANTHROPIC_API_KEY`：Anthropic API 密钥
  - `RESEARCH_ASSISTANT_MODEL`：模型名称

### file_loader.py — 文件读取

- 读取 .txt 和 .md 文件
- 返回文件内容的字符串
- 处理文件不存在和不支持的文件格式

### output_writer.py — 输出保存

- 提供 save_output 函数保存 AI 输出到文件
- 自动生成唯一的文件名（输入文件名 + 命令类型）
- 创建 outputs/ 目录（如果不存在）
- 返回保存的文件路径
- 输出格式为 Markdown

### prompts.py — 提示词工程

- 提供 builder 函数构建结构化 prompt
- 每个 prompt 包含：
  - 任务说明（Task）
  - 输入内容（Note Content）
  - 限制条件（Constraints）
  - 输出格式要求（Output Format）
- 输出格式使用 Markdown，便于 CLI 展示

### ai_client.py — AI 客户端

- 定义 AIClient 抽象基类
- 实现 MockClient 返回固定响应
- 实现 ClaudeClient 调用 Anthropic Claude API
- 提供 get_client 工厂函数
- 根据配置选择客户端（mock 或 real）

## 4. 数据流

```text
用户输入文件路径
    ↓
config 读取环境变量配置
    ↓
file_loader 读取文件内容
    ↓
prompts.build_xxx() 构建结构化 prompt
    ↓
ai_client 处理内容（根据配置选择 mock 或 real）
    ↓
CLI 输出结果（Markdown 格式）
    ↓
[可选] output_writer 保存到文件（如果 --save）
```

## 5. 输出保存设计

### 文件命名规则

格式：`{input_filename}_{command}.md`

示例：
- `sample_note_summarize.md`
- `sample_note_ask.md`
- `sample_note_tasks.md`

### 默认输出目录

`outputs/` 目录，如果不存在会自动创建。

### 使用方式

```bash
# 不保存（默认）
research summarize examples/sample_note.md

# 保存到文件
research summarize examples/sample_note.md --save
```

### 错误处理

- 目录创建失败：打印错误信息
- 文件写入失败：打印错误信息

## 6. Prompt 设计原则

### 设计目标

- 结构化：输出使用固定 Markdown 格式
- 可靠性：只基于输入笔记回答，信息不足时明确说明
- 可测试：prompt 结构固定，便于测试验证

### Prompt 结构

每个 prompt 都包含以下部分：

1. **角色说明**：定义 AI 为研究助手
2. **任务说明**：明确要做什么
3. **限制条件**：约束 AI 行为
4. **输入内容**：用户提供的笔记
5. **输出格式**：固定的 Markdown 结构

### 三类 Prompt 的设计差异

#### Summarize Prompt

- 任务：生成摘要
- 输出结构：
  - Summary（2-3 句摘要）
  - Key Points（3-5 个要点）
  - Terms（重要术语）
  - Follow-up Questions（深入问题）
- 特点：提取和压缩信息

#### Ask Prompt

- 任务：回答问题
- 输出结构：
  - Answer（基于笔记的回答）
  - Evidence from the Note（引用原文）
  - Caveats（局限性说明）
- 特点：引用证据，承认不确定性

#### Tasks Prompt

- 任务：生成学习任务
- 输出结构：
  - Learning Tasks（3 个任务）
  - Suggested Order（建议顺序）
  - Estimated Difficulty（难度评估）
- 特点：可执行、有梯度

### 约束条件

所有 prompt 都包含以下约束：
- 只基于输入笔记回答
- 信息不足时明确说明
- 保持输出格式一致

## 7. 配置层设计

### 环境变量

| 变量 | 用途 | 默认值 |
|------|------|--------|
| RESEARCH_ASSISTANT_MODE | AI 模式 | mock |
| ANTHROPIC_API_KEY | Anthropic API 密钥 | None |
| RESEARCH_ASSISTANT_MODEL | 模型名称 | claude-sonnet-4-20250514 |

### 模式选择逻辑

```text
get_client()
    ↓
get_mode() 读取 RESEARCH_ASSISTANT_MODE
    ↓
if mode == "mock":
    return MockClient()
elif mode == "real":
    validate_real_mode()  # 检查 API key
    return ClaudeClient(api_key, model)
```

### 错误处理

- 无效的模式值：ConfigError
- real 模式没有 API key：ConfigError
- API 调用失败：Anthropic SDK 异常

## 8. AI Client 设计

### 抽象接口

```python
class AIClient(ABC):
    def summarize(self, prompt: str) -> str
    def ask(self, prompt: str) -> str
    def generate_tasks(self, prompt: str) -> str
```

### MockClient

- 返回固定的模拟响应
- 不需要 API key
- 用于开发和测试

### ClaudeClient

- 使用 Anthropic Python SDK
- 通过 `anthropic.Anthropic(api_key)` 初始化
- 调用 `client.messages.create()` 发送请求
- 解析响应并返回文本

### 工厂函数

`get_client()` 根据配置返回对应的客户端实例。

## 9. 错误处理

### 异常体系

所有自定义异常继承自 `ResearchAssistantError`，由 `cli.py` 统一捕获：

```text
ResearchAssistantError (基类，继承 Exception)
├── FileLoadError      — 文件读取错误（不存在、格式不支持、空文件）
├── ConfigError        — 配置错误（环境变量缺失或无效）
├── AIClientError      — AI 调用失败（认证、限流、网络、响应格式）
└── OutputWriteError   — 输出保存失败（磁盘、权限）
```

### 错误处理流程

```text
模块抛出自定义异常
    ↓
cli.py main() 顶层 try/except
    ↓
ResearchAssistantError → logger.error("Error: ...") → sys.exit(1)
未知异常 → 非 verbose: "An unexpected error occurred. Use --verbose for details."
       → verbose: 显示完整 traceback
    ↓
sys.exit(1)
```

### 错误场景对照

| 场景 | 异常类型 | 用户看到的消息 |
|------|----------|--------------|
| 文件不存在 | FileLoadError | `Error: File not found: path/to/file` |
| 不支持的文件格式 | FileLoadError | `Error: Unsupported file type: .csv. Supported types: .md, .txt` |
| 空文件 | FileLoadError | `Error: File is empty: path/to/file` |
| 未知命令 | argparse 自动处理 | 帮助信息 |
| 无效的模式 | ConfigError | `Error: Invalid RESEARCH_ASSISTANT_MODE=foo...` |
| real 模式没有 API key | ConfigError | `Error: RESEARCH_ASSISTANT_MODE is 'real', but ANTHROPIC_API_KEY is not set.` |
| API 认证失败 | AIClientError | `Error: API authentication failed. Check your ANTHROPIC_API_KEY.` |
| API 限流 | AIClientError | `Error: API rate limit exceeded. Please try again later.` |
| API 其他错误 | AIClientError | `Error: API call failed. Check your network connection and try again.` |
| 输出保存失败 | OutputWriteError | `Error: Failed to save output to ...` |

## 10. 日志设计

### 概述

使用 Python 标准库 `logging` 模块，不引入第三方依赖。

### 配置

```python
from research_assistant.logger import setup_logger

# 默认模式：WARNING 级别，用户只看到错误消息
logger = setup_logger(verbose=False)

# 调试模式：DEBUG 级别，显示详细信息
logger = setup_logger(verbose=True)
```

### 日志级别

- **默认（WARNING）**：用户只看到 `Error: ...` 消息
- **verbose（DEBUG）**：显示 API 调用详情（模型名、prompt 长度、响应长度）、文件保存路径

### `--verbose` 参数

作为全局参数放在 argparse 主 parser 上（不是子命令参数），所有子命令自动支持：

```bash
research --verbose summarize file.md
research -v ask file.md "question"
```

### 安全约束

日志中**禁止**记录以下内容：

| 禁止内容 | 原因 |
|----------|------|
| API key 的值 | 泄露密钥 = 他人可用你的配额 |
| API key 的任何部分 | 即使截断也有泄露风险 |
| 用户笔记的完整内容 | 笔记可能是私密研究笔记 |
| prompt 的完整内容 | prompt 包含用户笔记 |
| AI 输出的完整内容 | 可能包含敏感分析结果 |

允许在 DEBUG 级别记录的元数据：

- 文件名（不含路径）
- 命令名
- prompt 长度（字符数）
- AI 响应长度（字符数）
- 输出文件路径

## 11. 测试策略

| 模块 | 测试重点 |
|------|----------|
| exceptions.py | 异常层次结构、所有异常可被基类捕获、消息保留 |
| logger.py | logger 创建、级别设置、不重复添加 handler |
| config.py | 默认值、环境变量读取、验证逻辑、ConfigError 来自 exceptions |
| file_loader.py | 正常读取、文件不存在、格式不支持、空文件（均抛 FileLoadError） |
| output_writer.py | 文件创建、目录创建、内容写入、文件名格式、OutputWriteError |
| prompts.py | builder 函数输出包含必要内容和格式 |
| ai_client.py | MockClient 返回值、ClaudeClient API 调用、AIClientError 包装、不泄露 API key |
| cli.py | 友好错误消息、--verbose 参数、未知异常处理（通过 monkeypatch 测试） |

### 测试原则

- 测试中禁止调用真实 API
- 使用 monkeypatch 模拟 Anthropic SDK
- MockClient 测试不需要模拟
- ClaudeClient 测试通过模拟异常子类实现（避免 httpx.Response 依赖）
- Prompt 测试验证输出结构和内容
- Output writer 测试使用 tmp_path 处理临时文件
- CLI 错误处理测试通过 monkeypatch sys.argv 和 capsys 验证

## 12. 未来扩展

- 支持 PDF 文件解析
- 添加历史记录存储（JSON 文件）
- 添加 RAG（检索增强生成）
- 添加 Web UI
