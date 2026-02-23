import requests
from bs4 import BeautifulSoup
import datetime
import random
import os
import sys

# 서울/경기 지역 데이터
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
    # [설정] 한국 시간 기준 현재 시간 구하기
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    current_hour = now.hour
    today_str = now.strftime("%Y-%m-%d")

    # 1️⃣ 시간 제한: 08시 ~ 22시 사이만 작동
    if not (8 <= current_hour <= 22):
        print(f"🚫 현재 {current_hour}시: 포스팅 가능 시간이 아닙니다. (08~22시 사이만 작동)")
        return

    # 2️⃣ 개수 제한: 오늘 이미 10개가 생성되었는지 확인
    post_dir = '_posts'
    if not os.path.exists(post_dir):
        os.makedirs(post_dir)
        
    today_posts = [f for f in os.listdir(post_dir) if f.startswith(today_str)]
    
    if len(today_posts) >= 10:
        print(f"✅ 오늘 이미 {len(today_posts)}개의 포스팅을 완료했습니다. 내일 다시 시작합니다.")
        return

    # --- 여기서부터 포스팅 생성 로직 ---
    town, town_full, service = get_random_keyword()
    selected_keyword = f"{town_full} {service}"
    
    time_tag = now.strftime("%H%M%S")
    file_title = selected_keyword.replace(" ", "-")
    file_path = f"_posts/{today_str}-{time_tag}-{file_title}.md"

    content_text = get_naver_text(selected_keyword)

    post_data = f"""---
layout: post
title: "{selected_keyword} 완료 리포트"
date: {today_str}
town: "{town}"
town_full: "{town_full}"
---

### 🚚 {selected_keyword} 현장 실시간 소식

{town_full} 지역에서 저희 에이플러스 퀵을 찾아주시는 모든 고객님께 감사드립니다. 언제나 **신속한 배송**을 원칙으로 안전하게 모시겠습니다.

---

#### ✅ 현장 리포트
{content_text}

---

#### 📞 이용 안내
서울 및 경기 전 지역을 그물망처럼 연결하여 가장 가까운 기사님을 **신속하게** 배차해 드립니다. 

* **24시간 접수처: 1661-4262**
* **전차종(오토바이, 다마스, 라보, 1톤) 대기**

**신속한 배송** 에이플러스 퀵서비스였습니다.
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(post_data)
    print(f"🚀 [{selected_keyword}] 포스팅 생성 완료! (오늘 {len(today_posts) + 1}/10)")

if __name__ == "__main__":
    create_post()
