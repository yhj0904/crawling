#!/usr/bin/env bash
set -euo pipefail

# ───────── 설정값 ─────────
VENV=".venv"            # 가상환경 폴더
CRAWLER="main.py"    # 크롤러 파일
DBSAVE="db_save.py"     # DB 저장 파일

# ───────── 1. 가상환경 ─────────
python3 -m venv "$VENV"
source "$VENV/bin/activate"

# ───────── 2. 패키지 ─────────
python -m pip install --upgrade pip
pip install requests beautifulsoup4 lxml pymongo

# ───────── 3. 크롤러 실행 ─────────
python "$CRAWLER"

# 방금 생성된 최신 JSON 찾기
LATEST_JSON=$(ls -t iris_*.json | head -n 1)

# ───────── 4. MongoDB 저장 ─────────
python "$DBSAVE" "$LATEST_JSON"
