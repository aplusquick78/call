import requests
from bs4 import BeautifulSoup
import datetime
import random
import os

# 서울 25개 구 전체
seoul_gu = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]

# 경기도 전체 (시 + 군 포함 31개 지역)
# 사장님이 말씀하신 가평, 양평, 연천, 여주 등을 모두 추가했습니다.
gyeonggi_si = [
    "수원시", "성남시", "고양시", "용인시", "부천시", "안산시", "안양시", "남양주시", 
    "화성시", "평택시", "의정부시", "시흥시", "파주시", "광명시", "김포시", "군포시", 
    "광주시", "이천시", "양주시", "오산시", "구리시", "안성시", "포천시", "의왕시", 
    "하남시", "여주시", "여주군", "가평군", "양평군", "연천군", "동두천시", "과천시"
]

services = ["퀵서비스", "오토바이퀵", "다마스퀵", "라보퀵", "용달"]

def get_random_keyword():
    region = random.choice(["서울", "경기"])
    if region == "서울":
        gu = random.choice(seoul_gu)
        town = gu
        town_full = f"서울특별시 {gu}"
    else:
        si_gun = random.choice(gyeonggi_si)
        town = si_gun
        town_full = f"경기도 {si_gun}"
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
    # 현재 시간 (KST 기준)
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    today_str = now.strftime("%Y-%m-%d")
    time_tag = now.strftime("%H%M%S")

    post_dir = '_posts'
    if not os.path.exists(post_dir):
        os.makedirs(post_dir)
        
    town, town_full, service = get_random_keyword()
    selected_keyword = f"{town_full} {service}"
    
    # 파일명 생성
    file_path = f"{post_dir}/{today_str}-{time_tag}-{selected_keyword.replace(' ', '-')}.md"

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
    print(f"🚀 [전지역 무한모드] 파일 생성됨: {file_path}")

if __name__ == "__main__":
    create_post()
