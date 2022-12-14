from sqlalchemy import insert, select, inspect, func
from sqlalchemy.orm import aliased, join

from tgbot.infrastucture.database.models.answers import Answers
from tgbot.infrastucture.database.models.questions import Questions
from tgbot.infrastucture.database.models.users import User

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}




async def create_user(session, telegram_id, full_name, username, language_code, referrer_id=None):
    stmt = insert(User).values(
        telegram_id=telegram_id,
        full_name=full_name,
        username=username,
        language_code=language_code,
        referrer_id=referrer_id,
    )
    await session.execute(stmt)

async def write_answer(session, telegram_id, question_id, category, answer):
    stmt = insert(Answers).values(
        telegram_id=telegram_id,
        question_id=question_id,
        category=category,
        answer=answer
    )
    await session.execute(stmt)

async def load_questions(session, category):
    stmt = select(Questions.id, Questions.question, Questions.category).filter_by(category=category).order_by(func.random())
    result = await session.execute(stmt)
    rows = result.all()
    result_dict = [u._asdict() for u in rows]
   # rows = [dict(row) for row in rows]
   # print(result_dict)
    return result_dict

async def select_users_with_referrer(session):
    # Simple INNER JOIN

    # We need a new alias for the referrer table
    Referrer = aliased(User)
    stmt = select(
        User.full_name.label('user'),  # We can use 'label' to give an alias to the column
        Referrer.full_name.label('referrer'),
    ).join(
        Referrer,
        Referrer.telegram_id == User.referrer_id
    )
    return await session.execute(stmt)



async def select_all_users_and_some_referrers(session):
    # Left JOIN

    Referrer = aliased(User)
    stmt = select(
        User.full_name.label('user'),  # We can use 'label' to give an alias to the column
        Referrer.full_name.label('referrer'),
    ).join(
        Referrer,  # right join side
        Referrer.telegram_id == User.referrer_id,  # on clause
        isouter=True,  # outer join
    )
    return await session.execute(stmt)


async def select_some_users_and_all_referrers(session):
    # Right JOIN is a LEFT join, with tables swapped

    Referrer = aliased(User)
    stmt = select(
        User.full_name.label('user'),  # We can use 'label' to give an alias to the column
        Referrer.full_name.label('referrer'),
    ).select_from(
        join(
            Referrer,  # Making referrer the left join side for LEFT JOIN.
            User,
            onclause=Referrer.telegram_id == User.referrer_id,
            isouter=True,  # outer join
        )
    )
    return await session.execute(stmt)
