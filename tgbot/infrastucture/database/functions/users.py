from sqlalchemy import insert, select, inspect, func, update
from sqlalchemy.dialects.postgresql import array_agg
from sqlalchemy.orm import aliased, join

from tgbot.infrastucture.database.models.answers import Answers
from tgbot.infrastucture.database.models.questions import Questions
from tgbot.infrastucture.database.models.users import User

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


async def create_user(session, telegram_id, full_name, username, language_code, referrer_id=None, deep_link=None):
    stmt = insert(User).values(
        telegram_id=telegram_id,
        full_name=full_name,
        username=username,
        language_code=language_code,
        referrer_id=referrer_id,
        deep_link=deep_link
    )
    await session.execute(stmt)


async def deactivate_user(session, telegram_id):
    stmt = update(User).where(User.telegram_id == telegram_id).values(active=False)
    await session.execute(stmt)


async def edit_notif_user(session, telegram_id, setting):
    stmt = update(User).where(User.telegram_id == telegram_id).values(reflection_time=setting)
    await session.execute(stmt)


async def select_all_users(session):
    stmt = select(User.telegram_id).filter_by(active=True)
    result = await session.execute(stmt)
    rows = result.all()
    result_dict = [u._asdict() for u in rows]
    return result_dict


async def select_scheduler_users(session, hour):
    stmt = select(User.telegram_id).filter_by(active=True).filter_by(reflection_time=hour)
    result = await session.execute(stmt)
    rows = result.all()
    result_dict = [u._asdict() for u in rows]
    return result_dict


async def select_daily_question(session, category):
    stmt = select(Questions.id, Questions.question, Questions.category).where(Questions.id > 1647).filter_by(category=category).order_by(func.random())
    result = await session.execute(stmt)
    rows = result.all()
    result_dict = [u._asdict() for u in rows]
    return result_dict[0]

async def write_answer(session, telegram_id, question_id, category, answer):
    stmt = insert(Answers).values(
        telegram_id=telegram_id,
        question_id=question_id,
        category=category,
        answer=answer
    )
    await session.execute(stmt)


async def load_questions(session, category, random=True):
    stmt = select(Questions.id, Questions.question, Questions.category).filter_by(category=category)
    if random: stmt = stmt.order_by(func.random())
    result = await session.execute(stmt)
    rows = result.all()
    result_dict = [u._asdict() for u in rows]
    return result_dict


async def get_last_answers(session, telegram_id, category):
    stmt = select(Questions.question, array_agg(Answers.answer), func.max(Answers.created_at)).filter_by(
        category=category
    ).join(
        Answers,
        Answers.question_id == Questions.id
    ).group_by(Questions.question).filter_by(
        telegram_id=telegram_id).order_by(func.max(Answers.created_at).desc())
    result = await session.execute(stmt)
    rows = result.all()
    result_dict = [u._asdict() for u in rows]
    return result_dict

async def count_questions_in_category(session, category):
    stmt = select(func.count(Questions.question)).filter_by(category=category)
    result = await session.execute(stmt)
    return result.first()[0]

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
