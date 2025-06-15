from datetime import datetime
from app.database.session import async_session  # Импортируй свою async сессию
from app.database.models import Metric

async def log_event(user_id: int, event_type: str):
    async with async_session() as session:
        metric = Metric(
            user_id=user_id,
            event_type=event_type,
            timestamp=datetime.utcnow()
        )
        session.add(metric)
        await session.commit()
