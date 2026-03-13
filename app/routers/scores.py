from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import HighScore
from app.schemas import ScoreCreate, ScoreResponse

router = APIRouter(prefix="/scores", tags=["scores"])

@router.post("/", response_model=ScoreResponse)
async def submit_score(score_in: ScoreCreate, db: AsyncSession = Depends(get_db)):
    db_score = HighScore(
        quicdial_id=score_in.quicdial_id,
        game=score_in.game,
        score=score_in.score
    )
    db.add(db_score)
    await db.commit()
    await db.refresh(db_score)
    return db_score

@router.get("/{game}/top", response_model=List[ScoreResponse])
async def get_top_scores(game: str, limit: int = 10, db: AsyncSession = Depends(get_db)):
    # Fetch the top scores sorted descending
    stmt = select(HighScore).filter(HighScore.game == game).order_by(HighScore.score.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
