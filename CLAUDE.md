# Claude Code 协作规则

## 项目信息

- 项目名：AI Research Assistant CLI
- 包名：research_assistant
- CLI 命令：research
- Python 版本：>=3.11

## 代码规范

- 使用 type hints
- 函数和变量用 snake_case
- 类用 PascalCase
- 每个模块顶部写 docstring 说明用途
- 字符串用双引号

## 测试规范

- 每个模块对应一个 test_ 文件
- 测试函数名：test_<功能>_<场景>
- 使用 pytest，不用 unittest
- 运行测试：make test 或 pytest -q
- 使用 tmp_path fixture 处理临时文件
- 使用 monkeypatch fixture 处理环境变量

## 修改流程

1. 先读现有代码
2. 做小的修改
3. 运行测试
4. 检查 git diff
5. 更新文档（如果行为变了）
6. 不要自动 commit

## 限制

- 不要引入新的外部依赖（除非必要）
- 不要修改 .gitignore
- 不要创建 .env 文件
- 不要硬编码 API key
- 不要自动 commit

## 安全规则

- 不要硬编码 API key 或 secret
- 不要在代码中读取 .env 文件（使用 os.environ）
- 不要在日志或输出中打印 API key
- 不要在错误信息中暴露 API key
- 不要将 API key 传递给第三方库以外的地方
- 配置读取失败时，给出清晰的错误信息，不要静默回退

## 模块职责

| 模块 | 职责 |
|------|------|
| cli.py | CLI 入口，命令解析 |
| config.py | 环境变量配置管理 |
| file_loader.py | 读取 .txt/.md 文件 |
| prompts.py | prompt 模板定义 |
| ai_client.py | AI 客户端抽象 + mock |
