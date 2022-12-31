from sqlalchemy import create_engine, MetaData, Table, VARCHAR, INTEGER, \
    Column, TIME, BOOLEAN, DATE, ForeignKey
from DataBase.Settings import *

# +++ Духно Михаил misha.duhno@mail.ru +++
engine = create_engine(
    f'postgresql+psycopg2://{user}:{password}@{connection}/{database}')
metadata = MetaData()

roles_table = Table('roles_table', metadata,
                    Column('id', INTEGER(), primary_key=True,
                           autoincrement=True),
                    Column('title', VARCHAR(15), nullable=False, unique=True))

users_table = Table('users_table', metadata,
                    Column('user_id', INTEGER(), primary_key=True,
                           autoincrement=True, unique=True),
                    Column('first_name', VARCHAR(70), nullable=False),
                    Column('last_name', VARCHAR(70), nullable=False),
                    Column('middle_name', VARCHAR(50), nullable=True),
                    Column('login', VARCHAR(50), nullable=True, unique=True),
                    Column('email', VARCHAR(100), nullable=False, unique=True),
                    Column('hashed_password', VARCHAR(256), nullable=False),
                    Column('wallet_addres', VARCHAR(100)),
                    Column('phone_number', VARCHAR(20), nullable=False,
                           unique=True),
                    Column('last_seen', TIME(), nullable=True),
                    Column('is_online', BOOLEAN, nullable=True),
                    Column('about', VARCHAR(100), nullable=True),
                    Column('birth_date', DATE(), nullable=False),
                    Column('sex', VARCHAR(10), nullable=False),
                    Column('picture_photo', VARCHAR(8000), nullable=True),
                    Column('private_key', VARCHAR(70), nullable=True))

users_roles_table = Table('users_roles_table', metadata,
                          Column('id', INTEGER(), primary_key=True,
                                 autoincrement=True),
                          Column('user_id', INTEGER(),
                                 ForeignKey(users_table.c.user_id)),
                          Column('role_id', INTEGER(),
                                 ForeignKey(roles_table.c.id)))

achievments_table = Table('achievments_table', metadata,
                          Column('achievment_id', INTEGER(), primary_key=True,
                                 autoincrement=True),
                          Column('header', VARCHAR(50), nullable=False),
                          Column('description', VARCHAR(50), nullable=False),
                          Column('image', VARCHAR(8000), nullable=True))

users_achievments_table = Table('users_achievments_table', metadata,
                                Column('id', INTEGER(), primary_key=True,
                                       autoincrement=True),
                                Column('user_id', INTEGER(),
                                       ForeignKey(users_table.c.user_id)),
                                Column('achievment_id', INTEGER(), ForeignKey(
                                    achievments_table.c.achievment_id)))

posts_table = Table('posts_table', metadata,
                    Column('post_id', INTEGER(), primary_key=True,
                           autoincrement=True),
                    Column('header', VARCHAR(50), nullable=False),
                    Column('image', VARCHAR(8000), nullable=True),
                    Column('description', VARCHAR(400), nullable=False),
                    Column('award', INTEGER(), nullable=True),
                    Column('event_date', DATE()))

user_posts = Table('user_posts', metadata,
                   Column('id', INTEGER(), primary_key=True,
                          autoincrement=True),
                   Column('user_id', INTEGER(),
                          ForeignKey(users_table.c.user_id)),
                   Column('post_id', INTEGER(),
                          ForeignKey(posts_table.c.post_id)))

nft_table = Table('nft_table', metadata,
                  Column('id', INTEGER(), primary_key=True,
                         autoincrement=True),
                  Column('image', VARCHAR(8000), nullable=True),
                  Column('header', VARCHAR(100), nullable=False),
                  Column('description', VARCHAR(50), nullable=True))

item_table = Table('item_table', metadata,
                   Column('item_id', INTEGER(), primary_key=True,
                          autoincrement=True),
                   Column('name', VARCHAR(50), nullable=False),
                   Column('image', VARCHAR(8000), nullable=False),
                   Column('price', INTEGER(), nullable=False),
                   Column('add_date', DATE(), nullable=False),
                   Column('purchases_amount', INTEGER(), nullable=False),
                   Column('amount', INTEGER(), nullable=True),
                   Column('nft_id', INTEGER(), ForeignKey(nft_table.c.id)))

metadata.create_all(engine)
# ---Духно Михаил misha.duhno@mail.ru---
