name: Generate Town Pages

on:
  push:
    paths:
      - '_data/towns.yml'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install PyYAML
        run: pip install pyyaml

      - name: Run Generator Script
        run: |
          python - <<EOF
          import yaml
          import os

          # 1. towns.yml 읽기
          with open('_data/towns.yml', 'r', encoding='utf-8') as f:
              data = yaml.safe_load(f)

          # 2. 페이지 생성 로직
          for region_group in data:
              region = region_group['region']
              for district in region_group['districts']:
                  dist_name = district['name']
                  for town in district['towns']:
                      # [중요] 주소 구조: 동이름퀵서비스 (중복 시 구이름 붙임)
                      folder_name = f"{town}퀵서비스"
                      
                      # 중복 이름 처리 (예: 신사동)
                      if os.path.exists(folder_name):
                          folder_name = f"{dist_name}{town}퀵서비스"
                      
                      os.makedirs(folder_name, exist_ok=True)
                      
                      # 파일 내용 (사장님 layout: board 적용)
                      content = f"---\nlayout: board\ntown: {town}\ntown_full: {region} {dist_name} {town}\n---"
                      
                      with open(f"{folder_name}/index.html", 'w', encoding='utf-8') as f:
                          f.write(content)
          EOF

      - name: Commit and Push changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "Automated town pages generation" || exit 0
          git push
