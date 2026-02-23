import yaml
import os
import shutil

# 1. towns.yml 읽기
with open('_data/towns.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# 2. 페이지 생성 로직
for region_group in data:
    region = region_group['region'].strip()
    
    # [시/도 페이지] 인천광역시 -> 인천, 경기도 -> 경기
    reg_name = region.replace("광역시", "").replace("특별시", "").replace("경기도", "경기").replace("특별자치시", "").replace("특별자치도", "").strip()
    reg_folder = f"{reg_name}퀵서비스"
    
    os.makedirs(reg_folder, exist_ok=True)
    with open(f"{reg_folder}/index.html", 'w', encoding='utf-8') as f:
        f.write(f"---\nlayout: board\ntown: {reg_name}\ntown_full: {region}\n---")

    for district in region_group['districts']:
        dist_full_name = district['name'].strip()
        
        # [구/군 페이지] 안양시 -> 안양, 강남구 -> 강남구
        if dist_full_name.endswith("시"):
            dist_name = dist_full_name.replace("시", "").strip()
        else:
            dist_name = dist_full_name
            
        dist_folder = f"{dist_name}퀵서비스"
        
        # 중복 방지 (예: 강서구 -> 서울강서구퀵서비스)
        if os.path.exists(dist_folder) and dist_folder != reg_folder:
            dist_folder = f"{reg_name}{dist_name}퀵서비스"
            
        os.makedirs(dist_folder, exist_ok=True)
        with open(f"{dist_folder}/index.html", 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: board\ntown: {dist_name}\ntown_full: {region} {dist_full_name}\n---")

        for town in district['towns']:
            # [동네 페이지] 기존 로직 유지
            town_name = town.strip()
            folder_name = f"{town_name}퀵서비스"
            
            # 중복 이름 처리 (예: 신사동 -> 강남구신사동)
            if os.path.exists(folder_name):
                folder_name = f"{dist_name}{town_name}퀵서비스"
            
            os.makedirs(folder_name, exist_ok=True)
            
            content = f"---\nlayout: board\ntown: {town_name}\ntown_full: {region} {dist_full_name} {town_name}\n---"
            
            with open(f"{folder_name}/index.html", 'w', encoding='utf-8') as f:
                f.write(content)

print("✅ 시/도, 구/군, 동별 모든 페이지 생성이 완료되었습니다.")
