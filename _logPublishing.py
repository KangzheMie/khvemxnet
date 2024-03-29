import os
import re
from pathlib import Path

def parse_file_and_generate_html(input_file_path, output_dir):
    # 确保输出目录存在，如果不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(input_file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
    
    # 使用正则表达式分割内容，仅匹配##开头的行，避免匹配到###开头的行
    sections = re.split(r'\n(?=##[^#])', file_content)
    
    for section in sections:
        # 分割标题和正文
        title_end_index = section.find("\n") # 找到标题和正文的分割点
        title = section[2:title_end_index].strip() if title_end_index != -1 else section[2:].strip()  # 提取标题
        body = section[title_end_index:].strip() if title_end_index != -1 else "" # 提取正文
        
        # 将###开头的行转换为<h3>，并为每一段文本添加<p>标签
        body_html = ""
        for line in body.split("\n"):
            if line.startswith("###"):
                body_html += f"<h3>{line[3:].strip()}</h3>"
            else:
                body_html += f"<p>{line.strip()}</p>"
        
        # 生成HTML文件内容
        html_content = f"<html><head><title>{title}</title></head><body>{body_html}</body></html>"
        
        # 生成文件名，并替换不适合文件名的字符
        filename = f"{title.replace(' ', '_').replace('/', '_')}.html"
        full_path = os.path.join(output_dir, filename)
        
        # 写入文件
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"文件 {full_path} 已生成。")

def add_script_to_html_log(directory_path, log_name):
    # 遍历指定目录下的所有HTML文件
    for html_file in Path(directory_path).glob('*.html'):
        with open(html_file, 'r+', encoding='utf-8') as file:
            content = file.read()
            script = f"""
<script>
  if (window.location.href.indexOf('?page={html_file.stem}') === -1) {{
    window.location.href = '/subpage/wangkangzhe/index.html?page=./log/{log_name}/{html_file.stem}.html';
  }}
</script>
"""
            # 检查文件是否已包含该脚本
            if script.strip() not in content:
                # 在文件内容开头添加脚本
                content = script + content
                # 移动文件指针到文件开头
                file.seek(0)
                # 写入修改后的内容
                file.write(content)
                # 截断文件，移除原始内容之后的任何内容
                file.truncate()
    print("脚本添加完成！")

def add_script_to_html(directory_path):
    # 遍历指定目录下的所有HTML文件
    for html_file in Path(directory_path).glob('*.html'):
        with open(html_file, 'r+', encoding='utf-8') as file:
            content = file.read()
            script = f"""
<script>
  if (window.location.href.indexOf('?page={html_file.stem}') === -1) {{
    window.location.href = '/subpage/wangkangzhe/index.html?page=./log/{html_file.stem}';
  }}
</script>
"""
            # 检查文件是否已包含该脚本
            if script.strip() not in content:
                # 在文件内容开头添加脚本
                content = script + content
                # 移动文件指针到文件开头
                file.seek(0)
                # 写入修改后的内容
                file.write(content)
                # 截断文件，移除原始内容之后的任何内容
                file.truncate()
    print("脚本添加完成！")

# 获取脚本所在目录的绝对路径   更改当前工作目录
script_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_path)

# 执行脚本

log_name_list = ['RiCh','BiJi']
log_titles = {
    'RiCh': '宇宙随时可以打败我，但不是今天',
    'BiJi': '赛博笔记，记录随手记录'
}
log_flowers = {
    'RiCh': '🌻',
    'BiJi': '🌺'
}

for log_name in log_name_list:
    parse_file_and_generate_html(f"./source/log/{log_name}.md", f"./log/{log_name}/")

    # 初始化一个列表来收集所有合适的文件名
    titles = []
    # 遍历目录中的所有文件
    for filename in os.listdir(f'./log/{log_name}/'):
        if filename.endswith(".html"):
            # 使用os.path.splitext去除文件扩展名
            titles.append(os.path.splitext(filename)[0])
    # 为每个分类生成HTML文件
    filepath = f'./log/log_{log_name}.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('<div class="timeline">\n')
        f.write(f'    <h2>{log_titles.get(log_name, "通用标题")}</h2>\n')
        f.write('    <ul>\n')
        # 按日期倒序排序
        for title in sorted(titles, reverse=True):
            f.write(f'        <li>\n')
            f.write(f'            <span class="date"> {log_flowers.get(log_name, "🌻")}</span>\n')
            f.write(f'            <span class="event"><a href="./log/{log_name}/{title}.html">{title}</a></span>\n')
            f.write('        </li>\n')
        f.write('    </ul>\n')
        f.write('</div>\n')
    print(f"log_{log_name}.html生成完毕。")
    add_script_to_html_log(f'./log/{log_name}/',log_name)

add_script_to_html('./log')