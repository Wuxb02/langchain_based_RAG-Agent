# LangChain Agent

基于 LangChain 框架构建的智能对话系统，分别实现了 RAG（检索增强生成）和 ReAct Agent 能力。

## 项目简介

本项目分别实现了两个智能客服系统，结合了向量检索和多工具调用能力。

## 主要功能

- **RAG 知识库问答**：基于 ChromaDB 的向量检索系统
- **ReAct Agent**：支持多工具调用的智能代理
- **流式输出**：实时响应用户查询
- **工具集成**：天气查询、位置获取、数据报告等
- **中间件支持**：工具监控、日志记录、提示词切换

## 项目结构

```
langchain_agent/
├── Agent_test/          # Agent 核心实现
│   ├── agent/          # ReAct Agent 实现
│   │   ├── react_agent.py
│   │   └── tools/      # 工具集和中间件
│   ├── rag/            # RAG 服务
│   │   ├── rag_service.py
│   │   └── vector_store.py
│   ├── model/          # 模型工厂
│   ├── utils/          # 工具函数
│   ├── config/         # 配置文件
│   ├── prompts/        # 提示词模板
│   └── app.py          # Streamlit 应用入口
└── RAG_test/           # RAG 功能测试
```

## 快速开始

### 环境要求

- Python >= 3.10
- 依赖包管理：uv

### 安装依赖

```bash
# 使用 uv 安装依赖
uv sync
```

### 运行应用

```bash
# 启动 Streamlit 应用
streamlit run Agent_test/app.py
```

## 技术栈

- **LangChain**：Agent 框架和工具链
- **ChromaDB**：向量数据库
- **Streamlit**：Web 界面
- **OpenAI API**：大语言模型

## 配置说明

在 `Agent_test/config/` 目录下配置相关参数：
- 模型参数
- 向量数据库设置

## License

MIT
