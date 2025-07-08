import fitz  # PyMuPDF 库
import os    # 用于处理文件和目录

# 获取脚本所在目录
current_folder = os.path.dirname(os.path.realpath(__file__))

# 目标字符串
target_string = "nfendianzishangwuyouxiangongsi"

# 获取目录下所有 PDF 文件
pdf_files = [f for f in os.listdir(current_folder) if f.lower().endswith('.pdf')]

if not pdf_files:
    print(f"错误：当前目录 {current_folder} 未找到任何 PDF 文件")
    exit(1)

for filename in pdf_files:
    # 定义输入和输出 PDF 文件路径
    input_pdf = os.path.join(current_folder, filename)
    output_pdf = os.path.join(current_folder, f"modified_{filename}")

    print(f"\n正在处理 PDF: {input_pdf}")
    print(f"输出 PDF: {output_pdf}")

    try:
        # 打开 PDF 文件
        pdf_document = fitz.open(input_pdf)

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
            
            # 检查目标字符串的存在形式
            print(f"\n页面 {page_num + 1} 中 '{target_string}' 的存在形式：")
            text_dict = page.get_text("dict")
            blocks = text_dict["blocks"]
            rects_to_redact = []
            lines_to_delete = []
            found = False
            
            for block in blocks:
                if "lines" not in block:
                    continue
                block_rect = fitz.Rect(block["bbox"])
                for line in block["lines"]:
                    line_text = "".join(span["text"] for span in line["spans"]).strip()
                    if target_string in line_text:
                        found = True
                        # 打印行信息
                        print(f"- 所在行文本: {line_text}")
                        print(f"- 所在文本块坐标: {block_rect}")
                        # 打印每段的字体和大小
                        for span in line["spans"]:
                            print(f"  - 文本片段: '{span['text']}', 字体: {span['font']}, 大小: {span['size']}, 坐标: {fitz.Rect(span['bbox'])}")
                        # 记录要删除的行和坐标
                        lines_to_delete.append(line_text)
                        for span in line["spans"]:
                            if target_string in span["text"]:
                                rects_to_redact.append(fitz.Rect(span["bbox"]))
            
            if not found:
                print(f"页面 {page_num + 1} 未找到 '{target_string}'，跳过。")
                continue
            
            # 打印要删除的行
            print(f"\n页面 {page_num + 1} 要删除的行（包含 '{target_string}'）：")
            for i, line in enumerate(lines, 1):
                if line in lines_to_delete:
                    print(f"行 {i}: {line}")
            
            # 合并重叠的矩形区域以避免重复修订
            merged_rects = []
            for rect in rects_to_redact:
                merged = False
                for existing in merged_rects:
                    if rect.intersects(existing):
                        existing |= rect  # 合并矩形
                        merged = True
                        break
                if not merged:
                    merged_rects.append(rect)
            
            # 应用修订，删除目标行的文本
            for rect in merged_rects:
                page.add_redact_annot(rect, text="")
            page.apply_redactions()
            
            # 获取并打印保留的行
            remaining_lines = [line for line in lines if line not in lines_to_delete]
            remaining_line_numbers = [i for i, line in enumerate(lines, 1) if line not in lines_to_delete]
            print(f"\n页面 {page_num + 1} 保留的文本行（带行号）：")
            for i, line in zip(remaining_line_numbers, remaining_lines):
                print(f"行 {i}: {line}")
            
            print(f"页面 {page_num + 1} 已删除包含 '{target_string}' 的文本，保留其他内容。")
        
        # 保存修改后的 PDF
        pdf_document.save(output_pdf, garbage=4, deflate=True)
        print(f"修改后的 PDF 已保存为: {output_pdf}")

        # 关闭 PDF
        pdf_document.close()

    except Exception as e:
        print(f"处理 {input_pdf} 时出错: {e}")