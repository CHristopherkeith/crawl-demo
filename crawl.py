import requests
from bs4 import BeautifulSoup
import time
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

def fetch_page(page_num):
    url = f"https://book.douban.com/top250?start={page_num * 25}"
    print(f"抓取第 {page_num + 1} 页: {url}")
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_books(html):
    soup = BeautifulSoup(html, 'lxml')
    books = []
    for li in soup.select('tr.item'):
        title = li.select_one('div.pl2 a').get_text(strip=True).replace("\n", "")
        info = li.select_one('p.pl').text.strip()
        rating = li.select_one('span.rating_nums').text.strip()
        quote = li.select_one('span.inq')
        quote = quote.text.strip() if quote else ''
        books.append({
            'title': title,
            'info': info,
            'rating': rating,
            'quote': quote
        })
    return books

def crawl_all():
    all_books = []
    for page in range(2):  # 每页 25 本，共 10 页
        html = fetch_page(page)
        books = parse_books(html)
        all_books.extend(books)
        time.sleep(random.uniform(1, 2))  # 加一点延迟，防止被封
    return all_books

if __name__ == "__main__":
    book_list = crawl_all()
    for book in book_list[:10]:  # 打印前 10 本书看看
        print(f"{book['title']} | {book['info']} | {book['rating']}分 | {book['quote']}")
