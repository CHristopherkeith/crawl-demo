import csv
import time
import random
from playwright.sync_api import sync_playwright

def fetch_page(page_num, page):
    """使用Playwright抓取页面内容"""
    url = f"https://book.douban.com/top250?start={page_num * 25}"
    print(f"抓取第 {page_num + 1} 页: {url}")
    
    page.goto(url, timeout=30000)
    page.wait_for_selector('tr.item', timeout=10000)
    
    return page

def parse_books(page):
    """解析页面中的图书信息"""
    books = []
    book_items = page.query_selector_all('tr.item')
    
    for item in book_items:
        title_el = item.query_selector('div.pl2 a')
        title = title_el.text_content().strip().replace("\n", "")
        
        info_el = item.query_selector('p.pl')
        info = info_el.text_content().strip()
        
        rating_el = item.query_selector('span.rating_nums')
        rating = rating_el.text_content().strip()
        
        quote_el = item.query_selector('span.inq')
        quote = quote_el.text_content().strip() if quote_el else ''
        
        books.append({
            'title': title,
            'info': info,
            'rating': rating,
            'quote': quote
        })
    return books

def save_to_csv(books, filename='douban_books_playwright.csv'):
    """将爬取的图书信息保存到CSV文件"""
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['title', 'info', 'rating', 'quote']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
    print(f"数据已保存到 {filename}，共 {len(books)} 条记录")

def crawl_all():
    all_books = []
    with sync_playwright() as playwright:
        # 使用本地Chrome浏览器而不是自动安装的Chromium
        browser = playwright.chromium.launch(
            headless=False,  # 设置为False使浏览器界面可见
            # channel="chrome"  # 指定使用已安装的Chrome，没有这一句时，需要执行playwright install chromium安装playwright自带的浏览器
        )
        
        try:
            page = browser.new_page()
            
            for i in range(2):  # 每页 25 本，共 2 页
                # 抓取页面
                page = fetch_page(i, page)
                
                # 解析图书信息
                books = parse_books(page)
                all_books.extend(books)
                
                # 加一点延迟，防止被封
                time.sleep(random.uniform(1, 2))
        
        finally:
            browser.close()
    
    return all_books

if __name__ == "__main__":
    book_list = crawl_all()
    for book in book_list[:10]:  # 打印前 10 本书看看
        print(f"{book['title']} | {book['info']} | {book['rating']}分 | {book['quote']}")
    # 保存到CSV文件
    save_to_csv(book_list) 