import os
import yaml

# 1. 데이터 불러오기
with open('_data/towns.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# 2. 폴더 및 파일 생성 루프
for region in data:
    reg_name = region['region'] # 서울특별시
    
    # [시 단위 index 생성]
    os.makedirs(reg_name, exist_ok=True)
    with open(f"{reg_name}/index.html", "w", encoding='utf-8') as f:
        f.write(f"---\nlayout: board\ntown_full: {reg_name}\n---\n")

    for district in region['districts']:
        dist_name = district['name'] # 강남구
        
        # [구 단위 index 생성] -> 이제 404 안 뜹니다!
        dist_path = f"{reg_name}/{dist_name}"
        os.makedirs(dist_path, exist_ok=True)
        
        # 구 페이지 내용: 해당 구의 모든 동네를 리스팅
        town_list_html = "".join([f"<li><a href='./{t}/'>{t} 신속한 배송</a></li>" for t in district['towns']])
        with open(f"{dist_path}/index.html", "w", encoding='utf-8') as f:
            f.write(f"---\nlayout: board\ntown_full: {reg_name} {dist_name}\n---\n<ul>{town_list_html}</ul>")

        for town in district['towns']: # 삼성동
            # [동 단위 index 생성]
            path = f"{dist_path}/{town}"
            os.makedirs(path, exist_ok=True)
            
            content = f"---\nlayout: board\ntown: {town}\ntown_full: {reg_name} {dist_name} {town}\n---\n"
            with open(f"{path}/index.html", "w", encoding='utf-8') as f:
                f.write(content)

print("시/구/동 전방위 인덱스 생성 완료! 이제 404 없습니다.")
