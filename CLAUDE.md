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

## 模块职责

| 模块 | 职责 |
|------|------|
| cli.py | CLI 入口，命令解析 |
| file_loader.py | 读取 .txt/.md 文件 |
| prompts.py | prompt 模板定义 |
| ai_client.py | AI 客户端抽象 + mock |
