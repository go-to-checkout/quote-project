# 나만의 일기장 프로젝트

**💫 주요 기능**

- 회원가입
- 로그인/로그아웃 (JWT 인증)
- 일기 CRUD
- 일기 검색 및 정렬
- 명언 랜덤 제공
- 명언 북마크
- 자기성찰 질문 랜덤 제공

<iframe width="600" height="336" src="https://www.erdcloud.com/p/Fe5tr5uZK5BmNkYRk" frameborder="0" allowfullscreen></iframe>

#유비콘 서버시작
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
#가상환경가동
source .venv/scripts/activate
