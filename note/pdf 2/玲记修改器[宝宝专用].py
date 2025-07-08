import fitz  # PyMuPDF 库
import os   # 用于处理文件和目录
import logging

# 配置日志
logging.basicConfig(filename="pdf_processing.log", level=logging.INFO)

# 获取脚本所在目录
current_folder = os.path.dirname(os.path.realpath(__file__))

# 目标字符串数组（可随时添加字符串）
target_strings = [
    "nfendianzishangwuyouxiangongsi",
    "7C7",  # 可添加其他字符串
    "uguanyikejiyouxiangongsi",
    "gyaodianzishangwuyouxiangongsi",
    "7X 2X2",
    "Canada",
    "anzhouboyang Import and Export Trade Co., Ltd.",
    "uguanyikejiyouxiangongsi",

]

# 指定要删除的行号范围（行 3 到 13），设为 None 表示不删除行号范围
delete_line_range = (3, 13)
# delete_line_range = None  # 如果不想删除行号范围，取消注释此行

# 获取目录下所有 PDF 文件
pdf_files = [f for f in os.listdir(current_folder) if f.lower().endswith('.pdf')]

if not pdf_files:
    print(f"错误：当前目录 {current_folder} 未找到任何 PDF 文件")
    logging.error(f"当前目录 {current_folder} 未找到任何 PDF 文件")
    exit(1)

def get_unique_output_path(output_path):
    """生成唯一的输出文件名，避免覆盖"""
    base, ext = os.path.splitext(output_path)
    counter = 1
    while os.path.exists(output_path):
        output_path = f"{base}_{counter}{ext}"
        counter += 1
    return output_path

def clean_text(text):
    """清洗文本，移除多余空格和换行符"""
    return text.strip().replace("\n", " ").replace("\r", "")

def process_pdf(filename):
    # 定义输入和输出 PDF 文件路径
    input_pdf = os.path.join(current_folder, filename)
    output_pdf = get_unique_output_path(os.path.join(current_folder, f"modified_{filename}"))

    print(f"\n正在处理 PDF: {input_pdf}")
    print(f"输出 PDF: {output_pdf}")
    logging.info(f"正在处理 PDF: {input_pdf}")

    try:
        # 打开 PDF 文件
        pdf_document = fitz.open(input_pdf)
        if pdf_document.is_encrypted:
            print(f"错误：{input_pdf} 是加密文件，无法处理。")
            logging.error(f"{input_pdf} 是加密文件")
            return

        # 遍历每一页
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            
            # 获取页面文本并按行分割
            text = page.get_text("text")
            lines = text.splitlines()
            
            # 打印每行文本及行号
            print(f"\n页面 {page_num + 1} 文本行（带行号）：")
            for i, line in enumerate(lines, 1):
                print(f"行 {i}: {line}")
            
            # 初始化要删除的矩形区域和行
            rects_to_redact = []
            lines_to_delete = set()
            
            # 1. 处理目标字符串删除
            text_dict = page.get_text("dict")
            blocks = text_dict["blocks"]
            found_strings = []
            
            for block in blocks:
                if "lines" not in block:
                    continue
                block_rect = fitz.Rect(block["bbox"])
                for line in block["lines"]:
                    line_text = clean_text("".join(span["text"] for span in line["spans"]))
                    # 检查是否包含任一目标字符串
                    for target in target_strings:
                        if target in line_text:
                            found_strings.append((target, line_text, block_rect))
                            lines_to_delete.add(line_text)
                            for span in line["spans"]:
                                if target in clean_text(span["text"]):
                                    rects_to_redact.append(fitz.Rect(span["bbox"]))
            
            # 打印找到的目标字符串信息
            if found_strings:
                print(f"\n页面 {page_num + 1} 中找到的目标字符串：")
                for target, line_text, block_rect in found_strings:
                    print(f"- 目标: '{target}', 所在行: '{line_text}', 坐标: {block_rect}")
            else:
                print(f"页面 {page_num + 1} 未找到任何目标字符串。")
            
            # 2. 处理行号范围删除（如果指定）
            if delete_line_range:
                start_line, end_line = delete_line_range
                if start_line < 1 or end_line > len(lines) or start_line > end_line:
                    print(f"页面 {page_num + 1} 行号范围 {start_line}-{end_line} 无效，跳过行号删除。")
                else:
                    lines_to_delete.update(lines[start_line-1:end_line])
                    for block in blocks:
                        if "lines" not in block:
                            continue
                        for line in block["lines"]:
                            line_text = clean_text("".join(span["text"] for span in line["spans"]))
                            if line_text in lines[start_line-1:end_line]:
                                for span in line["spans"]:
                                    rects_to_redact.append(fitz.Rect(span["bbox"]))
            
            if not rects_to_redact:
                print(f"页面 {page_num + 1} 没有需要删除的内容，跳过。")
                continue
            
            # 打印要删除的行
            print(f"\n页面 {page_num + 1} 要删除的行：")
            for i, line in enumerate(lines, 1):
                if line in lines_to_delete:
                    print(f"行 {i}: {line}")
            
            # 合并重叠的矩形区域
            merged_rects = []
            for rect in rects_to_redact:
                merged = False
                for existing in merged_rects:
                    if rect.intersects(existing):
                        existing |= rect
                        merged = True
                        break
                if not merged:
                    merged_rects.append(rect)
            
            # 应用修订
            for rect in merged_rects:
                page.add_redact_annot(rect, text="")
            page.apply_redactions()
            
            # 获取并打印保留的行
            remaining_lines = [line for line in lines if line not in lines_to_delete]
            remaining_line_numbers = [i for i, line in enumerate(lines, 1) if line not in lines_to_delete]
            print(f"\n页面 {page_num + 1} 保留的文本行（带行号）：")
            for i, line in zip(remaining_line_numbers, remaining_lines):
                print(f"行 {i}: {line}")
            
            print(f"页面 {page_num + 1} 已删除目标内容，保留其他内容。")
        
        # 保存修改后的 PDF
        pdf_document.save(output_pdf, garbage=4, deflate=True)
        print(f"修改后的 PDF 已保存为: {output_pdf}")
        logging.info(f"修改后的 PDF 保存为: {output_pdf}")
        
        # 关闭 PDF
        pdf_document.close()

    except Exception as e:
        print(f"处理 {input_pdf} 时出错: {e}")
        logging.error(f"处理 {input_pdf} 时出错: {e}")

# 主程序
if __name__ == "__main__":
    for filename in pdf_files:
        process_pdf(filename)