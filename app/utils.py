from string import ascii_letters, digits
from random import choices

from sqlalchemy import select

from app.db.models import Token


ALPHANUM = ascii_letters + digits


async def generate_token(db):
    while True:
        token = ''.join(choices(ALPHANUM, k=6))
        stmt = select(Token).where(Token.short_url == token)
        is_exist = await db.scalar(stmt)
        if is_exist:
            continue
        else:
            break
    return token
