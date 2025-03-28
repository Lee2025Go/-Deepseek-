import requests
from bs4 import BeautifulSoup
import markdown
import os
import json
import time
from tqdm import tqdm

# Deepseek API Key (请替换成你的实际 API Key)
DEEPSEEK_API_KEY = "你的Deepseek API Key"

# -------------------- 辅助函数 --------------------

def print_progress(step, total_steps, description):
    """
    打印进度信息
    """
    percentage = (step / total_steps) * 100
    print(f"\n[{step}/{total_steps}] {description} - {percentage:.1f}%")
    print("-" * 50)

def get_website_input():
    """
    获取网站输入，支持多种输入方式
    """
    print("\n请选择输入方式：")
    print("1. 直接输入网址（用逗号分隔）")
    print("2. 从预设网站列表中选择")
    print("3. 从文件导入网址列表")
    
    while True:
        choice = input("\n请选择输入方式（1-3）：").strip()
        if choice == "1":
            while True:
                urls_input = input("请输入要爬取的网站网址，用逗号分隔（最多10个）：").strip()
                urls = [url.strip() for url in urls_input.split(",") if url.strip()]
                if 1 <= len(urls) <= 10:
                    return urls
                print("错误：请输入1-10个网址！")
        
        elif choice == "2":
            preset_sites = [
                "https://www.36kr.com",
                "https://www.techcrunch.com",
                "https://www.theverge.com",
                "https://www.engadget.com",
                "https://www.wired.com"
            ]
            print("\n预设网站列表：")
            for i, site in enumerate(preset_sites, 1):
                print(f"{i}. {site}")
            
            while True:
                try:
                    selections = input("\n请输入要选择的网站序号（用逗号分隔，最多10个）：").strip()
                    indices = [int(x.strip()) for x in selections.split(",")]
                    if all(1 <= i <= len(preset_sites) for i in indices) and 1 <= len(indices) <= 10:
                        return [preset_sites[i-1] for i in indices]
                    print("错误：请输入有效的序号（1-5）且数量在1-10之间！")
                except ValueError:
                    print("错误：请输入有效的数字！")
        
        elif choice == "3":
            file_path = input("请输入网址列表文件路径（每行一个网址）：").strip()
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                if 1 <= len(urls) <= 10:
                    return urls
                print("错误：文件中的网址数量必须在1-10之间！")
            except FileNotFoundError:
                print("错误：找不到指定的文件！")
        
        print("错误：请输入有效的选项（1-3）！")

def select_or_input(prompt, suggestions, item_type="选项"):
    """
    让用户选择或输入内容
    """
    print(f"\n{prompt}")
    print("-" * 50)
    print("建议的" + item_type + "：")
    for i, item in enumerate(suggestions.split('\n'), 1):
        print(f"{i}. {item}")
    
    while True:
        choice = input(f"\n请选择{item_type}序号或直接输入新的{item_type}：").strip()
        try:
            index = int(choice)
            if 1 <= index <= len(suggestions.split('\n')):
                return suggestions.split('\n')[index-1]
        except ValueError:
            pass
        return choice

def get_deepseek_response(prompt):
    """
    调用 Deepseek API 并返回响应。
    """
    url = "https://api.deepseek.com/v1/chat/completions"  # 正确的 Deepseek API 端点
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-reasoner",  # 替换成Deepseek的模型名称
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 检查请求是否成功
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Deepseek API 请求失败: {e}")
        return None

def get_web_content(url):
    """
    爬取网页内容。
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # 这里需要根据网站的HTML结构提取文章内容，例如：
        # content = soup.find('div', class_='article-content').text
        # 热点新闻可能在不同的标签中，需要根据实际情况调整
        content = soup.get_text() # 粗略提取全部文字
        return content
    except requests.exceptions.RequestException as e:
        print(f"网页爬取失败: {e}")
        return None

def save_article(article_title, article_content):
    """
    保存文章到 Markdown 文件。
    """
    folder_path = "articles"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"{article_title}.md")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(article_content)
        print(f"文章已保存到: {file_path}")
    except Exception as e:
        print(f"保存文章失败: {e}")


# -------------------- 功能模块 --------------------

class ContentCollection:
    """
    内容收集模块。
    """
    def __init__(self, urls):
        self.urls = urls

    def collect_data(self):
        """
        从指定网站收集数据。
        """
        all_content = ""
        for url in self.urls:
            content = get_web_content(url)
            if content:
                all_content += content + "\n\n"
        return all_content

    def analyze_data(self, content):
        """
        分析收集到的数据，给出主题建议。
        """
        prompt = f"分析以下科技新闻内容，给出3个文章主题建议，并简要说明理由：\n\n{content}"
        suggestions = get_deepseek_response(prompt)
        return suggestions

    def get_topic_suggestions(self):
        """
        获取文章主题建议。
        """
        content = self.collect_data()
        if content:
            suggestions = self.analyze_data(content)
            return suggestions
        else:
            return "未能成功收集到任何内容。"


class TitleGeneration:
    """
    标题拟定模块。
    """
    def __init__(self, topic):
        self.topic = topic

    def generate_titles(self):
        """
        根据主题生成标题建议。
        """
        prompt = f"根据以下文章主题，给出5个吸引人的文章标题建议，以及对应的文章类型（例如：评测、分析、教程）和文章风格（例如：幽默、专业、科普）：\n\n{self.topic}"
        titles = get_deepseek_response(prompt)
        return titles


class OutlineGeneration:
    """
    大纲拟定模块。
    """
    def __init__(self, topic, title, article_type, article_style):
        self.topic = topic
        self.title = title
        self.article_type = article_type
        self.article_style = article_style

    def generate_outlines(self):
        """
        根据主题、标题、类型和风格生成文章大纲。
        """
        prompt = f"根据以下信息，设计5个详细的文章大纲：\n\n主题：{self.topic}\n标题：{self.title}\n类型：{self.article_type}\n风格：{self.article_style}"
        outlines = get_deepseek_response(prompt)
        return outlines


class ContentCreation:
    """
    内容撰写模块。
    """
    def __init__(self, topic, outline):
        self.topic = topic
        self.outline = outline

    def write_section(self, section_title):
        """
        根据小标题撰写文章段落。
        """
        prompt = f"请按照一篇成品文章的标准，撰写关于'{section_title}'的内容，主题为：{self.topic}。"
        content = get_deepseek_response(prompt)
        return content

    def write_article(self):
        """
        根据大纲撰写整篇文章。
        """
        article = ""
        for section in self.outline.split("\n"): # 假设大纲按行分隔
            if section.strip(): # 忽略空行
                article += f"## {section.strip()}\n\n"  # 添加 Markdown 二级标题
                article += self.write_section(section.strip()) + "\n\n"
        return article


class ContentRefinement:
    """
    内容润色模块。
    """
    def __init__(self, article):
        self.article = article

    def refine_article(self):
        """
        润色文章内容，使其更符合中文表达习惯。
        """
        prompt = f"请润色以下文章，使其在用词、标点符号、语法上更符合中文读者的习惯：\n\n{self.article}"
        refined_article = get_deepseek_response(prompt)
        return refined_article


class MarkdownConversion:
    """
    Markdown 转换模块。
    """
    def __init__(self, article):
        self.article = article

    def convert_to_markdown(self):
        """
        将文章转换为 Markdown 格式。
        """
        return self.article  # 假设文章已经是用 Markdown 格式撰写

    def refine_markdown(self):
        """
        润色 Markdown 语法，确保使用得当。
        """
        #  可以使用正则表达式或 markdown 库来检查和修正 Markdown 语法
        #  这里只是一个占位符
        return self.convert_to_markdown()


# -------------------- 交互界面 --------------------

def main():
    """
    主函数，负责与用户交互。
    """
    total_steps = 8
    current_step = 0
    
    print("\n=== 欢迎使用科技文章自动生成工具！===\n")
    print("本工具将帮助您完成科技文章的创作，共分为8个步骤。")
    print("=" * 50)

    # 1. 内容收集
    current_step += 1
    print_progress(current_step, total_steps, "第一步：内容收集")
    urls = get_website_input()
    
    print("\n正在收集内容，请稍候...")
    with tqdm(total=len(urls), desc="爬取进度") as pbar:
        content_collection = ContentCollection(urls)
        topic_suggestions = content_collection.get_topic_suggestions()
        pbar.update(len(urls))
    
    print("\n主题建议：")
    print("-" * 50)
    print(topic_suggestions)
    print("-" * 50)

    # 2. 标题拟定
    current_step += 1
    print_progress(current_step, total_steps, "第二步：标题拟定")
    topic = input("请选择或输入文章主题：").strip()
    
    print("\n正在生成标题建议，请稍候...")
    with tqdm(total=1, desc="生成进度") as pbar:
        title_generation = TitleGeneration(topic)
        title_suggestions = title_generation.generate_titles()
        pbar.update(1)
    
    title = select_or_input("请选择或输入文章标题", title_suggestions, "标题")

    # 3. 大纲拟定
    current_step += 1
    print_progress(current_step, total_steps, "第三步：大纲拟定")
    article_type = input("请输入文章类型（例如：评测、分析、教程）：").strip()
    article_style = input("请输入文章风格（例如：幽默、专业、科普）：").strip()
    
    print("\n正在生成大纲建议，请稍候...")
    with tqdm(total=1, desc="生成进度") as pbar:
        outline_generation = OutlineGeneration(topic, title, article_type, article_style)
        outline_suggestions = outline_generation.generate_outlines()
        pbar.update(1)
    
    outline = select_or_input("请选择或输入文章大纲", outline_suggestions, "大纲")

    # 4. 内容撰写
    current_step += 1
    print_progress(current_step, total_steps, "第四步：内容撰写")
    print("\n正在生成文章内容，请稍候...")
    with tqdm(total=1, desc="生成进度") as pbar:
        content_creation = ContentCreation(topic, outline)
        article = content_creation.write_article()
        pbar.update(1)

    # 5. 内容润色
    current_step += 1
    print_progress(current_step, total_steps, "第五步：内容润色")
    print("正在润色文章内容...")
    with tqdm(total=1, desc="润色进度") as pbar:
        content_refinement = ContentRefinement(article)
        refined_article = content_refinement.refine_article()
        pbar.update(1)

    # 6. Markdown 转换
    current_step += 1
    print_progress(current_step, total_steps, "第六步：Markdown转换")
    print("正在转换Markdown格式...")
    with tqdm(total=1, desc="转换进度") as pbar:
        markdown_conversion = MarkdownConversion(refined_article)
        markdown_article = markdown_conversion.convert_to_markdown()
        refined_markdown_article = markdown_conversion.refine_markdown()
        pbar.update(1)

    # 7. 文章储存
    current_step += 1
    print_progress(current_step, total_steps, "第七步：文章储存")
    save_article(title, refined_markdown_article)

    # 8. 内容展示和反馈
    current_step += 1
    print_progress(current_step, total_steps, "第八步：内容展示和反馈")
    print("\n最终文章：")
    print("=" * 50)
    print(refined_markdown_article)
    print("=" * 50)

    while True:
        feedback = input("\n请对文章提出意见或建议（输入 '满意' 表示完成，输入 '修改' 重新生成）：").strip()
        if feedback.lower() == "满意":
            print("\n文章生成完成！感谢使用！")
            break
        elif feedback.lower() == "修改":
            print("\n请重新运行程序以生成修改后的文章。")
            break
        else:
            print("\n收到您的反馈，请选择 '满意' 或 '修改' 继续。")


if __name__ == "__main__":
    main()
