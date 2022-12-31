from sqlalchemy import delete, select, and_, asc, \
    desc, func, update
from DataBase.Tables import *
from DataBase.Settings import *

# +++ Духно Михаил misha.duhno@mail.ru +++
engine = create_engine(
    f'postgresql+psycopg2://{user}:{password}@{connection}/{database}')
conn = engine.connect()


def get_roles():
    s = select([
        roles_table.c.id,
        roles_table.c.title
    ]).select_from(
        roles_table)

    rs = conn.execute(s)
    return rs.fetchall()


# Функция для получения данных по логину пользователя
def get_user(username, hashed_password):
    try:
        s = select([
            users_table.c.user_id,
            users_table.c.login,
            users_table.c.hashed_password
        ]).select_from(
            users_table
        ).where(
            and_(users_table.c.login == username,
                 users_table.c.hashed_password == hashed_password)
        )

        rs = conn.execute(s)
        return rs.fetchone()
    except Exception as e:
        print(e)
        return False


def get_news():
    s = select([
        posts_table.c.header,
        posts_table.c.image,
        posts_table.c.description,
        posts_table.c.award,
        posts_table.c.event_date
    ]).select_from(
        posts_table
    )

    rs = conn.execute(s)
    return rs.fetchall()


def get_events():
    s = select([
        posts_table.c.header,
        posts_table.c.image,
        posts_table.c.description,
        posts_table.c.award,
        posts_table.c.event_date
    ]).select_from(
        posts_table
    ).where(
        posts_table.c.award is not None
    )

    rs = conn.execute(s)
    return rs.fetchall()


def get_user_achievments(user_id):
    s = select([
        achievments_table.c.header,
        achievments_table.c.description,
        achievments_table.c.image
    ]).select_from(
        users_achievments_table.join(achievments_table)
    ).where(users_achievments_table.c.user_id == user_id)

    rs = conn.execute(s)
    return rs.fetchall()


def get_achievments():
    s = select([
        achievments_table.c.header,
        achievments_table.c.description,
        achievments_table.c.image
    ]).select_from(
        achievments_table)

    rs = conn.execute(s)
    return rs.fetchall()


# --- Духно Михаил misha.duhno@mail.ru ---


# +++ Выходцев Егор wf-game-acc@bk.ru +++
def get_user_logpass(user_id):
    s = select([
        users_table.c.login,
        users_table.c.hashed_password
    ]).select_from(users_table).where(users_table.c.user_id == user_id)
    rs = conn.execute(s)
    return rs.fetchone()


# Вывод предметов по дате добавления по убыванию
def filter_date_desc(amount):
    if amount:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price,
            item_table.c.amount
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            desc(item_table.c.add_date))
        rs = conn.execute(s)
        return rs.fetchall()
    else:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            desc(item_table.c.add_date))
        rs = conn.execute(s)
        return rs.fetchall()


# Вывод предметов по дате добавления по возрастанию
def filter_date_asc(amount):
    if amount:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price,
            item_table.c.amount
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            asc(item_table.c.add_date))
        rs = conn.execute(s)
        return rs.fetchall()
    else:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            asc(item_table.c.add_date))
        rs = conn.execute(s)
        return rs.fetchall()


# Вывод предметов по убыванию цены
def filter_price_desc(amount):
    if amount:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price,
            item_table.c.amount
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            desc(item_table.c.price))
        rs = conn.execute(s)
        return rs.fetchall()
    else:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            desc(item_table.c.price))
        rs = conn.execute(s)
        return rs.fetchall()


# Вывод предметов по возрастанию цены
def filter_price_asc(amount):
    if amount:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price,
            item_table.c.amount
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            asc(item_table.c.price))
        rs = conn.execute(s)
        return rs.fetchall()
    else:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            asc(item_table.c.price))
        rs = conn.execute(s)
        return rs.fetchall()


# Вывод предметов по убыванию популярности (числу покупок)
def filter_popularity_desc(amount):
    if amount:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price,
            item_table.c.amount
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            desc(item_table.c.purchases_amount))
        rs = conn.execute(s)
        return rs.fetchall()
    else:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            desc(item_table.c.purchases_amount))
        rs = conn.execute(s)
        return rs.fetchall()


# Вывод предметов по возрастанию популярности (числу покупок)
def filter_popularity_asc(amount):
    if amount:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price,
            item_table.c.amount
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            asc(item_table.c.purchases_amount))
        rs = conn.execute(s)
        return rs.fetchall()
    else:
        s = select([
            item_table.c.item_id,
            item_table.c.name,
            item_table.c.image,
            item_table.c.price
        ]).select_from(item_table).where(item_table.c.amount > 0).order_by(
            asc(item_table.c.purchases_amount))
        rs = conn.execute(s)
        return rs.fetchall()


# Добавление предмета в базу данных/каталог
def add_item(name, image, price, amount):
    try:
        ins = item_table.insert().values(
            name=name,
            image=image,
            price=price,
            add_date=func.current_date(),
            purchases_amount=0,
            amount=amount
        )
        ri = conn.execute(ins)
        return '200'
    except Exception as e:
        print(e)
        return '501'


# Удаление предмета из базы данных/каталога
def delete_item(del_id):
    try:
        de = delete(item_table).where(item_table.c.item_id == del_id)
        rd = conn.execute(de)
        return '200'
    except Exception as e:
        print(e)
        return '501'


# Добавление (регистрация) пользователя
def add_user(
        first_name, last_name, birth_date, sex, email,
        phone_number,
        hashed_password, wallet_addres, private_key, middle_name=None, ):
    try:
        ins = users_table.insert().values(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            login=email,
            email=email,
            hashed_password=hashed_password,
            wallet_addres=wallet_addres,
            phone_number=phone_number,
            birth_date=birth_date,
            sex=sex,
            private_key=private_key
        )
        ri = conn.execute(ins)
        return '200'
    except Exception as e:
        print(e)
        return '501'


# Добавление новости
def add_news(header, description, award=None, image=None, event_date=None):
    try:
        ins = posts_table.insert().values(
            header=header,
            image=image,
            description=description,
            award=award,
            event_date=event_date
        )
        ri = conn.execute(ins)
        return '200'
    except Exception as e:
        print(e)
        return '501'


# Добавление мероприятия
def add_event(header, description, award, event_date, image=None):
    try:
        ins = posts_table.insert().values(
            header=header,
            image=image,
            description=description,
            award=award,
            event_date=event_date
        )
        ri = conn.execute(ins)
        return '200'
    except Exception as e:
        print(e)
        return '501'


# Получение информации о пользователе
def get_user_info(user_id):
    s = select([
        users_table.c.first_name,
        users_table.c.last_name,
        users_table.c.middle_name,
        users_table.c.login,
        users_table.c.email,
        users_table.c.hashed_password,
        users_table.c.wallet_addres,
        users_table.c.phone_number,
        users_table.c.last_seen,
        users_table.c.is_online,
        users_table.c.about,
        users_table.c.birth_date,
        users_table.c.sex,
        users_table.c.picture_photo
    ]).select_from(users_table).where(users_table.c.user_id == user_id)
    rs = conn.execute(s)
    return rs.fetchone()


# Получение id роли конкретного пользователя
def get_user_role_id(user_id):
    s = select([
        users_roles_table.c.role_id
    ]).select_from(users_roles_table).where(
        users_roles_table.c.user_id == user_id)
    rs = conn.execute(s)
    return rs.fetchone()


# Получение роли пользователя по её id
def get_user_role(role_id):
    s = select([
        roles_table.c.title
    ]).select_from(roles_table).where(roles_table.c.id == role_id)
    rs = conn.execute(s)
    return rs.fetchone()


# Получение приват ключа отправителя
def get_sender_private_key(sender_id):
    s = select([
        users_table.c.private_key
    ]).select_from(users_table).where(users_table.c.user_id == sender_id)
    rs = conn.execute(s)
    return rs.fetchone()


# Получение адреса кошелька получателя
def get_recipient_wallet(recipient_id):
    s = select([
        users_table.c.wallet_addres
    ]).select_from(users_table).where(users_table.c.user_id == recipient_id)
    rs = conn.execute(s)
    return rs.fetchone()


# Рейтинг пользователей по фамилии, по убыванию
def rating_user_name_desc():
    s = select([
        users_table.c.user_id,
        users_table.c.first_name,
        users_table.c.last_name,
        users_table.c.middle_name,
        users_table.c.wallet_addres,
        users_table.c.about,
        users_table.c.picture_photo
    ]).select_from(users_table).order_by(desc(users_table.c.last_name))
    rs = conn.execute(s)
    return rs.fetchall()


# Рейтинг пользователей по фамилии по возрастанию
def rating_user_name_asc():
    s = select([
        users_table.c.user_id,
        users_table.c.first_name,
        users_table.c.last_name,
        users_table.c.middle_name,
        users_table.c.wallet_addres,
        users_table.c.about,
        users_table.c.picture_photo
    ]).select_from(users_table).order_by(asc(users_table.c.last_name))
    rs = conn.execute(s)
    return rs.fetchall()


# Сбор информации для рейтинга пользователя с сортировкой по балансу
def rating_info_for_balance_sort():
    s = select([
        users_table.c.user_id,
        users_table.c.first_name,
        users_table.c.last_name,
        users_table.c.middle_name,
        users_table.c.wallet_addres,
        users_table.c.about,
        users_table.c.picture_photo
    ]).select_from(users_table)
    rs = conn.execute(s)
    return rs.fetchall()


# Запись на мероприятие
def event_sign_up(user_id, event_id):
    try:
        ins = user_posts.insert().values(
            user_id=user_id,
            post_id=event_id
        )
        ri = conn.execute(ins)
        return '200'
    except Exception as e:
        print(e)
        return '501'


# Получить данные для обновления
def get_info_to_update(user_id):
    s = select([
        users_table.c.first_name,
        users_table.c.last_name,
        users_table.c.middle_name,
        users_table.c.login,
        users_table.c.email,
        users_table.c.phone_number,
        users_table.c.birth_date
    ]).select_from(users_table).where(users_table.c.user_id == user_id)
    rs = conn.execute(s)
    return rs.fetchone()


# Обновить данные пользователя
def update_user_info(user_id, first_name, last_name, middle_name, login, email,
                     phone_number, birth_date):
    try:
        s = update(users_table).where(users_table.c.user_id == user_id).values(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            login=login,
            email=email,
            phone_number=phone_number,
            birth_date=birth_date
        )
        rs = conn.execute(s)
        return '200'
    except Exception as e:
        print(e)
        return '501'


def add_achievement(header, description, image=True):
    try:
        ins = achievments_table.insert().values(
            header=header,
            description=description,
            image=image
        )
        ri = conn.execute(ins)
        return '200'
    except Exception as e:
        print(e)
        return '501'


def get_achievement_id():
    s = select([
        achievments_table.c.achievment_id
    ]).select_from(achievments_table)
    rs = conn.execute(s)
    return rs.fetchall()


def upd_achievement_photo(achievement_id):
    s = update(achievments_table).where(
        achievments_table.c.achievment_id == achievement_id
    ).values(
        image=True
    )
    rs = conn.execute(s)
    return '200'


def create_nft(header, description):
    try:
        ins = nft_table.insert().values(
            header=header,
            description=description,
        )
        ri = conn.execute(ins)
        return '200'
    except Exception as e:
        print(e)
        return '501'


def get_public_key(user_id):
    s = select([
        users_table.c.wallet_addres
    ]).select_from(users_table).where(users_table.c.user_id == user_id)
    rs = conn.execute(s)
    return rs.fetchone()


def reward_user(user_id, achievement_id):
    try:
        ins = users_achievments_table.insert().values(
            user_id=user_id,
            achievment_id=achievement_id
        )
        ri = conn.execute(ins)
        return '200'
    except Exception as e:
        print(e)
        return '501'


def get_nfts():
    s = nft_table.select()
    rs = conn.execute(s)
    return rs.fetchall()

def get_nfts_id():
    s = select(nft_table.c.id).select_from(nft_table)
    rs = conn.execute(s)
    return rs.fetchall()
# --- +++ Выходцев Егор wf-game-acc@bk.ru ---
