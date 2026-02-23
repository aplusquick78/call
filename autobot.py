import requests
from bs4 import BeautifulSoup
import datetime
import random
import os

# 데이터 설정
seoul_gu = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]
gyeonggi_si = ["수원시", "성남시", "고양시", "용인시", "부천시", "안산시", "안양시", "남양주시", "화성시", "평택시", "의정부시", "시흥시", "파주시", "광명시", "김포시", "군포시", "광주시", "이천시", "양주시", "오산시", "구리시", "안성시", "포천시", "의왕시", "하남시"]
services = ["퀵서비스", "오토바이퀵", "다마스퀵", "라보퀵", "용달"]

def get_random_keyword():
    region = random.choice(["서울", "경기"])
    if region == "서울":
        gu = random.choice(seoul_gu)
        town = gu
        town_full = f"서울특별시 {gu}"
    else:
        si = random.choice(gyeonggi_si)
        town = si
        town_full = f"경기도 {si}"
    service = random.choice(services)
    return town, town_full, service

def get_naver_text(keyword):
    url = f"https://search.naver.com/search.naver?where=view&query={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        descriptions = soup.select('.api_txt_lines.dsc_txt')
        text_list = [d.get_text() for d in descriptions[:5]]
        random.shuffle(text_list)
        return " ".join(text_list[:3])
    except:
        return f"{keyword} 전문 서비스를 제공하고 있습니다."

def create_post():
    # 현재 시간 (KST)
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    current_hour = now.hour
    today_str = now.strftime("%Y-%m-%d")

    # [테스트용] 시간 제한을 0~24시로 풀었습니다.
    if not (0 <= current_hour <= 24):
        print(f"🚫 현재 {current_hour}시: 범위를 벗어남")
        return

    post_dir = '_posts'
    if not os.path.exists(post_dir):
        os.makedirs(post_dir)
        
    today_posts = [f for f in os.listdir(post_dir) if f.startswith(today_str)]
    if len(today_posts) >= 10:
        print(f"✅ 오늘 이미 {len(today_posts)}개 완료")
        return

    town, town_full, service = get_random_keyword()
    selected_keyword = f"{town_full} {service}"
    time_tag = now.strftime("%H%M%S")
    file_path = f"{post_dir}/{today_str}-{time_tag}-{selected_keyword.replace(' ', '-')}.md"

    content_text = get_naver_text(selected_keyword)
    post_data = f"""---
layout: post
title: "{selected_keyword} 완료 리포트"
date: {today_str}
town: "{town}"
town_full: "{town_full}"
---
### 🚚 {selected_keyword} 현장 소식
{town_full} 지역 신속한 배송 리포트입니다.
#### ✅ 현장 리포트
{content_text}
#### 📞 이용 안내
* **24시간 접수처: 1661-4262**
**신속한 배송** 에이플러스 퀵서비스였습니다.
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(post_data)
    print(f"🚀 파일 생성됨: {file_path}")

if __name__ == "__main__":
    create_post()
