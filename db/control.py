import asyncpg
import datetime
import os
from db.encrypt import AESCipher
from typing import Optional, Tuple, List, Any

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
PASS_DB = os.getenv("PASS_DB")
USER_DB = os.getenv("USER_DB")
URL_DB = os.getenv("URL_DB")
NAME_DB = os.getenv("NAME_DB")

# Подключение к PostgreSQL (используйте пул соединений для эффективности)
async def get_db_connection():
    return await asyncpg.connect(
        user=USER_DB,
        password=PASS_DB,
        database=NAME_DB,
        host=URL_DB
    )



async def readUsersId() -> List[int]:
    """Чтение всех зарегистрированных user_id"""
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("SELECT user_id FROM users")
        return [row['user_id'] for row in rows]
    finally:
        await conn.close()


async def deleteUserId(user_id: int) -> None:
    """Удаление пользователя по user_id"""
    conn = await get_db_connection()
    try:
        await conn.execute("DELETE FROM users WHERE user_id = $1", user_id)
    finally:
        await conn.close()


async def writeLoginReadId(user_id: int, rdr_name: str, rdr_id: str) -> None:
    """Запись логина и читательского билета (с шифрованием)"""
    crypt = AESCipher(ENCRYPTION_KEY)
    encrypted_name = crypt.encrypt(rdr_name)
    encrypted_id = crypt.encrypt(rdr_id)

    conn = await get_db_connection()
    try:
        await conn.execute(
            "UPDATE users SET rdr_name = $1, rdr_id = $2 WHERE user_id = $3",
            encrypted_name, encrypted_id, user_id
        )
    finally:
        await conn.close()


async def readUserInfo(user_id: int) -> Tuple[Optional[str], Optional[str]]:
    """Получение логина и пароля пользователя (с расшифровкой)"""
    conn = await get_db_connection()
    try:
        row = await conn.fetchrow(
            "SELECT rdr_name, rdr_id FROM users WHERE user_id = $1",
            user_id
        )
        if not row or row['rdr_name'] is None or row['rdr_id'] is None:
            return (None, None)

        crypt = AESCipher(ENCRYPTION_KEY)
        name = crypt.decrypt(row['rdr_name'])
        rdr_id = crypt.decrypt(row['rdr_id'])
        return (name, rdr_id)
    finally:
        await conn.close()


async def writeResult(user_id: int, info: Any) -> None:
    """Запись результата (сериализация в строку)"""
    conn = await get_db_connection()
    try:
        await conn.execute(
            "UPDATE users SET info = $1 WHERE user_id = $2",
            str(info), user_id
        )
    finally:
        await conn.close()


async def readResult(user_id: int) -> Any:
    """Чтение результата (десериализация из строки)"""
    conn = await get_db_connection()
    try:
        row = await conn.fetchrow(
            "SELECT info FROM users WHERE user_id = $1",
            user_id
        )
        return eval(row['info']) if row and row['info'] else None
    finally:
        await conn.close()


async def acceptPrivacyRead(user_id: int) -> int:
    """Проверка принятия политики конфиденциальности"""
    conn = await get_db_connection()
    try:
        row = await conn.fetchrow(
            "SELECT privacy FROM users WHERE user_id = $1",
            user_id
        )
        return int(row['privacy']) if row and row['privacy'] else 0
    finally:
        await conn.close()


async def acceptPrivacyWrite(user_id: int) -> None:
    """Запись факта принятия политики конфиденциальности"""
    if user_id in await readUsersId():
        await deleteUserId(user_id)

    conn = await get_db_connection()
    try:
        await conn.execute(
            "INSERT INTO users (user_id, privacy, date_accept) VALUES ($1, $2, $3)",
            user_id, 1, datetime.datetime.now()
        )
    finally:
        await conn.close()