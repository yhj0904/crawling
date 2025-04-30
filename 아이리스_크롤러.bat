@echo off
REM ──────────────────────────────────────────────
REM  run_iris.bat  : 크롤링 → JSON → MongoDB
REM  필요 조건  : Windows + Python 3.x (PATH 등록)
REM ──────────────────────────────────────────────
SETLOCAL ENABLEDELAYEDEXPANSION

REM 1) 가상환경 생성 및 활성화
python -m venv .venv
call .\.venv\Scripts\activate.bat

REM 2) 패키지 설치
python -m pip install --upgrade pip
pip install requests beautifulsoup4 lxml pymongo

REM 3) 크롤러 실행 (JSON 생성)
python main.py

REM 4) 최신 JSON 파일 찾기
FOR /F "delims=" %%F IN ('dir /b /a-d /o-d iris_*.json') DO (
    set "LATEST_JSON=%%F"
    goto :FOUND_JSON
)
echo [WARN] JSON 파일을 찾지 못했습니다.
goto :END

:FOUND_JSON
REM 5) MongoDB 저장
python db_save.py "%LATEST_JSON%"

:END
ENDLOCAL
