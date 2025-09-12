from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB 접속 정보
DATABASE_URL = "mysql+pymysql://root:seokhun@localhost:3306/self_reflection"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, echo=True, future=True)

# 세션 로컬 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 의존성 주입용 함수
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
