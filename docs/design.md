# AI Research Assistant CLI 设计文档

## 1. 项目目标

面向学习和科研笔记的 AI 命令行工具。用户可以输入 .txt 或 .md 文件，让工具生成摘要、回答问题、生成后续学习任务。

## 2. 架构概述

```text
用户输入 → CLI 解析 → 文件读取 → AI 处理 → 结果输出
                ↓
            配置管理（环境变量）
```

CLI 入口（cli.py）负责解析命令行参数，调用文件读取模块（file_loader.py）加载文件内容，然后通过 AI 客户端（ai_client.py）处理内容，最后输出结果。配置模块（config.py）负责从环境变量读取配置。

## 3. 模块设计

### cli.py — CLI 入口

- 使用 argparse 解析命令行参数
- 支持子命令：summarize, ask, tasks, history
- 调用其他模块完成实际工作
- 处理错误并输出友好的错误信息

### config.py — 配置管理

- 从环境变量读取配置
- 提供默认值（mock 模式）
- 验证配置有效性
- 支持的环境变量：
  - `RESEARCH_ASSISTANT_MODE`：AI 模式（mock/real）
  - `RESEARCH_ASSISTANT_API_KEY`：API 密钥
  - `RESEARCH_ASSISTANT_MODEL`：模型名称

### file_loader.py — 文件读取

- 读取 .txt 和 .md 文件
- 返回文件内容的字符串
- 处理文件不存在和不支持的文件格式

### prompts.py — 提示词模板

- 定义 prompt 模板常量
- 提供 format_prompt 函数格式化模板
- 模板包含占位符，如 {text}、{question}

### ai_client.py — AI 客户端

- 定义 AIClient 抽象基类
- 实现 MockClient 返回固定响应
- 提供 get_client 工厂函数
- 根据配置选择客户端（mock 或 real）
- real 模式未实现，会抛出 NotImplementedError

## 4. 数据流

```text
用户输入文件路径
    ↓
config 读取环境变量配置
    ↓
file_loader 读取文件内容
    ↓
prompts 格式化 prompt 模板
    ↓
ai_client 处理内容（根据配置选择 mock 或 real）
    ↓
CLI 输出结果
```

## 5. 配置层设计

### 环境变量

| 变量 | 用途 | 默认值 |
|------|------|--------|
| RESEARCH_ASSISTANT_MODE | AI 模式 | mock |
| RESEARCH_ASSISTANT_API_KEY | API 密钥 | None |
| RESEARCH_ASSISTANT_MODEL | 模型名称 | mock-model |

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
    raise NotImplementedError  # 未实现
```

### 错误处理

- 无效的模式值：ConfigError
- real 模式没有 API key：ConfigError
- real 模式有 API key：NotImplementedError（未实现）

## 6. Mock 策略

当前阶段不接入真实 AI API，使用 MockClient 返回固定的模拟响应：

- summarize: 返回 "[Mock Summary] ..."
- ask: 返回 "[Mock Answer] ..."
- generate_tasks: 返回 3 条模拟学习任务

这样可以在不依赖外部 API 的情况下测试整个数据流。

## 7. 错误处理

| 场景 | 处理方式 |
|------|----------|
| 文件不存在 | FileNotFoundError → 打印错误信息，退出码 1 |
| 不支持的文件格式 | ValueError → 打印错误信息，退出码 1 |
| 未知命令 | argparse 自动打印帮助信息 |
| 无效的模式 | ConfigError → 打印错误信息 |
| real 模式没有 API key | ConfigError → 打印错误信息和设置方法 |
| real 模式有 API key | NotImplementedError → 打印未实现信息 |

## 8. 测试策略

| 模块 | 测试重点 |
|------|----------|
| config.py | 默认值、环境变量读取、验证逻辑 |
| file_loader.py | 正常读取、文件不存在、格式不支持、空文件 |
| prompts.py | 模板包含占位符、格式化正确替换 |
| cli.py | 不测试（通过手动验证） |
| ai_client.py | 不测试（mock 实现简单） |

## 9. 未来扩展

- 接入真实 AI API（Claude、OpenAI 等）
- 支持 PDF 文件解析
- 添加历史记录存储（JSON 文件）
- 添加 RAG（检索增强生成）
- 添加 Web UI
