from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "nickname" VARCHAR(50),
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "revoked_tokens" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "jti" VARCHAR(50) NOT NULL UNIQUE,
    "expires_at" TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_revoked_tok_jti_9261cc" ON "revoked_tokens" ("jti");
CREATE TABLE IF NOT EXISTS "diaries" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "user_id" CHAR(36) NOT NULL,
    "title" VARCHAR(200),
    "content" TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_diaries_user_id_12cb33" ON "diaries" ("user_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
