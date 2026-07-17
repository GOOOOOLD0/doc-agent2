import fitz

def extract_text_by_page_range(pdf_path, start_page, end_page):
    """
    从PDF中提取指定页面范围的文本
    :param pdf_path: PDF文件路径
    :param start_page: 起始页码 (从1开始)
    :param end_page: 结束页码 (从1开始)
    :return: 合并后的文本字符串
    """
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    
    # 将用户输入的从1开始的页码转换为0开始的索引
    start_idx = max(0, start_page - 1)
    end_idx = min(total_pages, end_page)  # range函数是左闭右开，所以这里不用再减1
    
    if start_idx >= end_idx:
        print("错误：起始页不能大于或等于结束页。")
        return ""
    
    full_text = ""
    for page_num in range(start_idx, end_idx):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        full_text += page_text + "\n"  # 添加换行符分隔不同页面
        
    doc.close()
    return full_text

# --- 使用示例 ---
pdf_file = r"wiki\raw\regulations\radio_regulations_2020\source.pdf"
# 提取第2页到第5页 (用户视角的页码)
extracted_text = extract_text_by_page_range(pdf_file, start_page=2, end_page=5)
print(extracted_text)