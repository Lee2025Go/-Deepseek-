# -Deepseek-
基于Deepseek的简易写作工作流
简介

本项目是一个基于 Python 的工具，旨在帮助用户自动化生成科技文章。它通过以下步骤完成文章的创作：
内容收集： 从用户指定的网站（支持直接输入、预设列表选择、文件导入）收集网页内容。
主题分析： 调用 Deepseek API 分析收集到的内容，给出文章主题建议。
标题拟定： 根据用户选择的主题，利用 Deepseek API 生成多个吸引人的文章标题、类型和风格建议。
大纲拟定： 根据用户选择的主题、标题、类型和风格，利用 Deepseek API 生成详细的文章大纲。
内容撰写： 依据生成的大纲，利用 Deepseek API 逐步撰写文章的各个段落。
内容润色： 使用 Deepseek API 对生成的文章进行润色，使其更符合中文表达习惯。
Markdown 转换： 将润色后的文章转换为 Markdown 格式。
文章储存： 将生成的 Markdown 格式文章保存到本地的 articles 文件夹中。

功能特点
多种网站输入方式： 支持直接输入网址、从预设列表选择、从文件导入网址列表，方便用户提供信息来源。
Deepseek API 驱动： 利用 Deepseek API 的强大语言模型能力，完成主题分析、标题生成、大纲生成、内容撰写和润色等核心任务。
可定制的文章风格： 用户可以指定期望的文章类型和风格，以更好地满足需求。
Markdown 输出： 生成的文章以 Markdown 格式保存，方便后续编辑和发布。
用户交互式体验： 通过清晰的步骤和用户提示，引导用户完成文章生成过程。
进度显示： 使用 tqdm 库显示每个步骤的进度，提升用户体验。


依赖环境
Python 3.x
requests (pip install requests)
beautifulsoup4 (pip install beautifulsoup4)
markdown (pip install markdown)
tqdm (pip install tqdm)

使用方法
克隆或下载本项目代码。
安装依赖库：
```bash
pip install -r requirements.txt
```
或者手动安装上述列出的依赖库。
配置 Deepseek API Key：
打开 main.py 文件。
将 DEEPSEEK_API_KEY = "你的Deepseek API Key" 这一行中的 "你的Deepseek API Key" 替换成你实际的 Deepseek API Key。请务必妥善保管你的 API Key。
运行脚本：
```bash
python main.py
```

按照终端提示进行操作：
选择网站输入方式并提供要分析的网站 URL。
选择或输入文章主题。
选择或输入文章标题。
输入文章类型和风格。
等待工具生成文章内容。
生成的 Markdown 格式文章将保存在 articles 文件夹中。
你可以选择对生成的文章表示满意或要求重新生成。


注意事项
Deepseek API 费用： 调用 Deepseek API 会产生费用，请注意你的 API 使用情况。
网站结构变化： 网页的 HTML 结构可能会发生变化，导致内容抓取失败。如果遇到这种情况，可能需要修改 get_web_content 函数中的内容提取逻辑。
文章质量： 自动生成的文章质量受多种因素影响，包括输入内容的质量、Deepseek API 的性能等。可能需要人工进行修改和完善。
API Key 安全： 请不要将你的 Deepseek API Key 泄露给他人。
项目结构

```
├── articles/ # 存储生成的 Markdown 文章
├── main.py # 主程序文件
└── README.md # 项目说明文档
```

未来改进方向
更智能的网页内容提取，能够自动适应不同网站的结构。
更丰富的文章类型和风格选项。
支持用户自定义提示词，以更精细地控制文章生成过程。
集成更多的内容润色和校对功能。
支持将文章发布到不同的平台。
错误处理和异常情况的优化。

贡献
欢迎提交 issue 和 pull request，为本项目做出贡献。
