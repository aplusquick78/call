import yaml
import os

# 1. 설정: 데이터 읽기
with open('_data/towns.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# 2. 파일 생성 로직
count = 0
for region_group in data:
    region = region_group['region']
    for district in region_group['districts']:
        district_name = district['name']
        for town in district['towns']:
            # 사장님이 원하시는 새로운 폴더 구조: 개포동퀵서비스/
            folder_name = f"{town}퀵서비스"
            
            # 만약 이름이 겹치는 동네(신사동 등)가 있으면 구 이름을 붙여서 충돌 방지
            if os.path.exists(folder_name):
                folder_name = f"{district_name}{town}퀵서비스"
            
            # 폴더 생성
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            
            # index.html 내용 (layout: board 유지)
            content = f"""---
layout: board
town: {town}
town_full: {region} {district_name} {town}
---"""
            
            # 파일 쓰기
            with open(f"{folder_name}/index.html", 'w', encoding='utf-8') as f:
                f.write(content)
            
            count += 1

print(f"✅ 작업 완료! 총 {count}개의 '동네이름퀵서비스' 폴더와 index.html이 생성되었습니다.")
