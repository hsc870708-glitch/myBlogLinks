import feedparser
from datetime import datetime
import html
import os

def generate_files():
    # 1. 네이버 블로그 RSS 주소
    rss_url = "https://rss.blog.naver.com/hsc870708.xml"
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        print("RSS 피드를 가져오지 못했습니다. 주소를 확인해주세요.")
        return

    # 2. 링크 리스트 생성 및 특수문자 처리
    links = []
    for entry in feed.entries:
        # PC 주소를 모바일 주소로 변환
        m_link = entry.link.replace("blog.naver.com", "m.blog.naver.com")
        links.append({
            "title": entry.title,
            "link": m_link
        })

    # 현재 날짜 (UTC 기준)
    now = datetime.now().strftime("%Y-%m-%d")

    # 3. index.html 내용 생성
    # google-site-verification 코드는 본인의 것을 그대로 유지하세요.
    html_items = "".join([f'<li><a href="{item["link"]}">{html.escape(item["title"])}</a></li>' for item in links])
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="google0db6c9b04da404f5.html" />
    <title>기록하는 생활 - 백링크 저장소</title>
</head>
<body>
    <h1>블로그 포스트 색인 목록</h1>
    <p>마지막 업데이트: {now}</p>
    <ul>
        {html_items}
    </ul>
</body>
</html>"""

    # 4. sitemap.xml 내용 생성 (에러 방지를 위해 html.escape 적용)
    xml_items = []
    for item in links:
        escaped_link = html.escape(item['link'])
        xml_items.append(f"""  <url>
    <loc>{escaped_link}</loc>
    <lastmod>{now}</lastmod>
    <priority>0.8</priority>
  </url>""")

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://hsc870708-glitch.github.io/myBlogLinks/</loc>
    <lastmod>{now}</lastmod>
    <priority>1.0</priority>
  </url>
{"".join(xml_items)}
</urlset>"""

    # 5. 파일 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"성공: {len(links)}개의 링크가 업데이트 되었습니다.")

if __name__ == "__main__":
    generate_files()
