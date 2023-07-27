from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import AnyUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Token
from app.db.session import get_async_session
from app.schemas import TokenResponse
from app.utils import generate_token


app = FastAPI(title='URLShortenerFastAPI')


@app.get('/')
def root():
    return {'success': 'This is the test URL'}


@app.post('/', response_model=TokenResponse)
async def create_token(original_url: AnyUrl, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Token).where(Token.original_url == original_url)
    existing_token = await db.scalar(stmt)
    if existing_token:
        pass
    new_token = Token(original_url=str(original_url), short_url=await generate_token(db))
    db.add(new_token)
    await db.commit()
    await db.refresh(new_token)

    return new_token


@app.get('/{short_url}')
async def redirect(short_url: str, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Token).where(Token.short_url == short_url)
    token = await db.scalar(stmt)
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='The token you provided was not found')

    return RedirectResponse(token.original_url)


