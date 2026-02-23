import requests
from bs4 import BeautifulSoup
import datetime
import random
import os

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
    # 💡 town, town_full 변수를 분리해서 가져옵니다.
    town, town_full, service = get_random_keyword()
    selected_keyword = f"{town_full} {service}"
    
    # 서버 시간 이슈 방지를 위해 날짜 설정
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    # 파일명 중복을 피하되 정렬이 깨지지 않게 시간 추가
    time_tag = now.strftime("%H%M%S")
    
    file_title = selected_keyword.replace(" ", "-")
    file_path = f"_posts/{date_str}-{time_tag}-{file_title}.md"

    content_text = get_naver_text(selected_keyword)

    # 사장님 사이트 레이아웃 변수(town, town_full)를 상단에 추가했습니다.
    post_data = f"""---
layout: post
title: "{selected_keyword} 완료 리포트"
date: {date_str}
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
    print(f"✅ [{selected_keyword}] 포스팅 생성 완료!")

if __name__ == "__main__":
    create_post()
