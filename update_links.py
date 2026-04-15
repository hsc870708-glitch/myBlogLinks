import feedparser
from datetime import datetime

# 1. 네이버 블로그 RSS 주소 (본인 아이디 입력)
rss_url = "https://rss.blog.naver.com/retriangle.xml"
feed = feedparser.parse(rss_url)

# 2. 링크 리스트 생성
links = []
for entry in feed.entries:
    # PC 주소를 모바일 주소로 변환 (중요!)
    m_link = entry.link.replace("blog.naver.com", "m.blog.naver.com")
    links.append({"title": entry.title, "link": m_link})

# 3. index.html 내용 생성
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="본인인증코드">
    <title>백링크 저장소</title>
</head>
<body>
    <h1>포스트 목록</h1>
    <ul>
        {"".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in links])}
    </ul>
</body>
</html>
"""

# 4. sitemap.xml 내용 생성
now = datetime.now().strftime("%Y-%m-%d")
xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://hsc870708-glitch.github.io/myBlogLinks/</loc>
        <lastmod>{now}</lastmod>
        <priority>1.0</priority>
    </url>
    {"".join([f'<url><loc>{item["link"]}</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>' for item in links])}
</urlset>
"""

# 5. 파일 저장
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

print("파일 생성 완료! 이제 깃허브에 Push 하세요.")
