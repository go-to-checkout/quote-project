from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "token_blacklist" (
    "token_blacklist_id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "token" TEXT NOT NULL,
    "expired_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "token_blacklist" IS 'JWT 토큰 블랙리스트 모델 - ERD token_blacklist 테이블';
CREATE TABLE IF NOT EXISTS "users" (
    "user_id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) UNIQUE,
    "password_hash" VARCHAR(50) NOT NULL
);
COMMENT ON TABLE "users" IS '사용자 모델 - ERD users 테이블';
CREATE TABLE IF NOT EXISTS "diaries" (
    "diary_id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "title" VARCHAR(50) NOT NULL,
    "content" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "diaries" IS '일기 모델 - ERD diaries 테이블';
CREATE TABLE IF NOT EXISTS "bookmarks" (
    "bookmark_id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "quote_id" INT NOT NULL,
    CONSTRAINT "uid_bookmarks_user_id_176fbb" UNIQUE ("user_id", "quote_id")
);
COMMENT ON TABLE "bookmarks" IS '북마크 모델 - ERD bookmarks 테이블';
CREATE TABLE IF NOT EXISTS "quotes" (
    "quote_id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "author" VARCHAR(50)
);
COMMENT ON TABLE "quotes" IS '명언 모델 - ERD quotes 테이블';
CREATE TABLE IF NOT EXISTS "questions" (
    "question_id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" TEXT NOT NULL
);
COMMENT ON TABLE "questions" IS '질문 모델 - ERD questions 테이블';
CREATE TABLE IF NOT EXISTS "user_questions" (
    "user_question_id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "question_id" INT NOT NULL
);
COMMENT ON TABLE "user_questions" IS '사용자 질문 이력 모델 - ERD user_questions 테이블';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
