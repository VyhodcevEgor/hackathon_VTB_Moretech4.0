import requests
from flask import Flask, jsonify, request, abort
from flask_mail import Mail, Message
import config
from DataBase import Requests
import hashlib
from random import choice
from string import ascii_letters, digits

app = Flask(__name__)

app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

mail = Mail(app)


# +++ Духно Михаил misha.duhno@mail.ru
@app.route('/api/get/roles', methods=['GET'])
def get_roles():
    users = Requests.get_roles()
    result = []
    for user in users:
        result.append({
            'id': user[0],
            'title': user[1]
        })
    return jsonify({'resp': result})


@app.route('/api/get/news', methods=['GET'])
def get_news():
    news_query = Requests.get_news()
    result = []
    i = 0
    for news in news_query:
        result.append({
            'id': i,
            'header': news[0],
            'image': news[1],
            'description': news[2],
            'award': news[3],
            'event_date': news[4]
        })
    return jsonify({'resp': result})


@app.route('/api/get/events', methods=['GET'])
def get_events():
    events_query = Requests.get_events()
    result = []
    i = 0
    for event in events_query:
        if event[3] is not None:
            result.append({
                'id': i,
                'header': event[0],
                'image': event[1],
                'description': event[2],
                'award': event[3],
                'event_date': event[4]
            })
        i += 1
    return jsonify({'resp': result})
@app.route('/api/get/achievments/user', methods=['POST'])
def get_user_achievments():
    if not request.json or 'userId' not in request.json:
        abort(400)

    user_achievments = Requests.get_user_achievments(request.json['userId'])
    all_achievments = Requests.get_achievments()
    if len(all_achievments) > 0:
        user_result = []
        i = 0
        text = 'data'
        for achiev in user_achievments:
            user_result.append({
                'id': i,
                'header': achiev[0],
                'description': achiev[1],
                'image': text
            })
            i += 1
        all_result = []
        i = 0
        for achiev in all_achievments:
            all_result.append({
                'id': i,
                'header': achiev[0],
                'description': achiev[1],
                'image': text
            })
            i += 1
        return jsonify({'resp': {'user_achievments': user_result,
                                 'all_achievments': all_result}})
    else:
        return jsonify({'resp': [{'name': 'name name', 'description': 'descr',
                                  'image': 'asdfadsf'}]})
@app.route('/api/add/achievement', methods=['POST'])
def add_and_send_achievement():
    if not request.json or 'header' not in request.json \
            or 'description' not in request.json \
            or 'image' not in request.json:
        abort(400)

    status = Requests.add_achievement(request.json["header"],
                                      request.json["description"],
                                      )
    if status == '200':
        achievement_ids = Requests.get_achievement_id()
        print(achievement_ids[-1])
        return jsonify({'status': status,
                        'achievement_id': achievement_ids[-1][0]})

    return jsonify({'status': status})


@app.route('/api/create/nft', methods=['POST'])
def create_nft():
    if not request.json or 'description' not in request.json:
        abort(400)

    status = Requests.create_nft(request.json["header"],
                                 request.json["description"])
    if status == '200':
        nft_ids = Requests.get_nfts_id()
        return jsonify({'status': status,
                        'achievement_id': nft_ids[-1][0]})
    return jsonify({'status': status})


@app.route('/api/generate/nft', methods=['POST'])
def generate_nft():
    if not request.json or 'user_id' not in request.json \
            or 'nft_id' not in request.json:
        abort(400)
    #  получаем id пользователя
    #  получаем id nft
    public_key = Requests.get_public_key(request.json["user_id"])
    nft_id = request.json["nft_id"]
    body = {
        "toPublicKey": f"{public_key}",
        "uri": f"{nft_id}",
        "nftCount": 1
    }
    response = requests.post("https://hackathon.lsp.team/hk/v1/nft/generate",
                             data=body)
    print(response.json())
    if response.json()['transaction_hash']:
        return jsonify({
            'status': '200',
            'transactionHash': response.json()['transaction_hash']
        })
    else:
        return jsonify({'status': '501'})


@app.route('/api/login', methods=['POST'])
def send_answer():
    if not request.json or 'login' not in request.json \
            or 'password' not in request.json:
        abort(400)

    user_id = Requests.get_user(request.json['login'], hashlib.sha256(
        request.json['password'].encode('utf-8')).hexdigest())
    print(hashlib.sha256(
        request.json['password'].encode('utf-8')).hexdigest())
    print(user_id)
    if user_id:
        try:
            user_data = {'user_id': user_id[0], 'hash': hashlib.sha256(
                (user_id[1] + user_id[2]).encode('utf-8')).hexdigest()}
            return jsonify({'resp': user_data})
        except Exception as e:
            print(f'Something gone wrong in time of request response\n'
                  f'Error: {e}')
            abort(500)
    else:
        print(f'User is not exists or hash of password is incorrect\n'
              f'login: {request.json["login"]}\n'
              f'password: {request.json["password"]}\n')
        abort(500)


# --- Духно Михаил misha.duhno@mail.ru

# +++ Выходцев Егор wf-game-acc@bk.ru +++
@app.route('/api/validation', methods=['POST'])
def validate():
    if not request.json or 'user_id' not in request.json \
            or 'token' not in request.json:
        abort(400)
    user_data = Requests.get_user_logpass(request.json["user_id"])
    print(user_data)
    compare_token = hashlib.sha256(
        (user_data[0] + user_data[1]).encode('utf-8')).hexdigest()
    print(compare_token)
    if compare_token == request.json['token']:
        return jsonify({'is_valid': True})
    else:
        return jsonify({'is_valid': False})


@app.route('/api/filter', methods=['POST'])
def filter_items():
    print(request.json)
    if not request.json or 'popularSort' not in request.json \
            or 'newnessSort' not in request.json \
            or 'priceSort' not in request.json or 'Amount' not in request.json:
        abort(400)

    result = []
    if request.json["newnessSort"] == "DECREASE":
        items = Requests.filter_date_desc(request.json["Amount"])
        print(items)
        if request.json["Amount"]:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                    'amount': item[4]
                })
            return jsonify({'resp': result})
        else:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                })
            return jsonify({'resp': result})

    if request.json["newnessSort"] == "INCREASE":
        items = Requests.filter_date_asc(request.json["Amount"])
        print(items)
        if request.json["Amount"]:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                    'amount': item[4]
                })
            return jsonify({'resp': result})
        else:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                })
            return jsonify({'resp': result})

    if request.json["priceSort"] == "DECREASE":
        items = Requests.filter_price_desc(request.json["Amount"])
        print(items)
        if request.json["Amount"]:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                    'amount': item[4]
                })
            return jsonify({'resp': result})
        else:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                })
            return jsonify({'resp': result})

    if request.json["priceSort"] == "INCREASE":
        items = Requests.filter_price_asc(request.json["Amount"])
        print(items)
        if request.json["Amount"]:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                    'amount': item[4]
                })
            return jsonify({'resp': result})
        else:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                })
            return jsonify({'resp': result})

    if request.json["popularSort"] == "DECREASE":
        items = Requests.filter_popularity_desc(request.json["Amount"])
        print(items)
        if request.json["Amount"]:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                    'amount': item[4]
                })
            return jsonify({'resp': result})
        else:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                })
            return jsonify({'resp': result})

    if request.json["popularSort"] == "INCREASE":
        items = Requests.filter_popularity_asc(request.json["Amount"])
        print(items)
        if request.json["Amount"]:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                    'amount': item[4]
                })
            return jsonify({'resp': result})
        else:
            for item in items:
                result.append({
                    'id': item[0],
                    'name': item[1],
                    'image': item[2],
                    'price': item[3],
                })
            return jsonify({'resp': result})


@app.route('/api/add/item', methods=['POST'])
def add_item():
    if not request.json or 'name' not in request.json \
            or 'image' not in request.json or 'price' not in request.json \
            or 'amount' not in request.json:
        abort(400)

    status = Requests.add_item(request.json["name"], request.json["image"],
                               request.json["price"], request.json["amount"])
    return jsonify({'status': status})


@app.route('/api/delete/item', methods=['POST'])
def delete_item():
    if not request.json or 'item_id' not in request.json:
        abort(400)
    status = Requests.delete_item(request.json["item_id"])
    return jsonify({'status': status})


@app.route('/api/add/user', methods=['POST'])
def add_user():
    if not request.json or 'first_name' not in request.json \
            or 'last_name' not in request.json \
            or 'birth_date' not in request.json or 'sex' not in request.json \
            or 'email' not in request.json \
            or 'phone_number' not in request.json:
        abort(400)

    chars = ascii_letters + digits + '_'
    pass_length = 8
    password = ''.join(choice(chars) for _ in range(pass_length))
    print(password)
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(hashed_password)

    wallet_response = requests.post(
        'https://hackathon.lsp.team/hk/v1/wallets/new')
    print(wallet_response.json())
    print(type(wallet_response.json()))
    print(wallet_response.json()['publicKey'])
    print(wallet_response.json()['privateKey'])
    mail_addr = request.json["email"]
    status = Requests.add_user(request.json["first_name"],
                               request.json["last_name"],
                               request.json["birth_date"], request.json["sex"],
                               mail_addr,
                               request.json["phone_number"],
                               hashed_password,
                               wallet_response.json()['publicKey'],
                               wallet_response.json()['privateKey'])

    if status == '200':
        msg = Message('Регистрация на платформе ВТБ',
                      recipients=[request.json["email"]])
        msg.body = f"Ваш логин: {mail_addr} \n" \
                   f"Ваш пароль: {password}"
        mail.send(msg)

    return jsonify({'status': status})


@app.route('/api/add/news', methods=['POST'])
def add_news():
    if not request.json or 'header' not in request.json \
            or 'image' not in request.json \
            or 'description' not in request.json:
        abort(400)
    status = Requests.add_news(request.json["header"],
                               request.json["description"],
                               image=request.json["image"],
                               )
    return jsonify({'status': status})


@app.route('/api/add/event', methods=['POST'])
def add_event():
    if not request.json or 'header' not in request.json \
            or 'image' not in request.json \
            or 'description' not in request.json \
            or 'event_date' not in request.json or 'award' not in request.json:
        abort(400)
    status = Requests.add_event(request.json["header"],
                                request.json["description"],
                                request.json["award"],
                                request.json["event_date"],
                                image=request.json["image"])
    return jsonify({'status': status})


@app.route('/api/user/info', methods=['POST'])
def get_user_info():
    if not request.json or 'user_id' not in request.json:
        abort(400)
    result = []
    user_info = Requests.get_user_info(request.json["user_id"])
    user_role_id = Requests.get_user_role_id(request.json["user_id"])
    user_role = Requests.get_user_role(user_role_id[0])
    print(user_info)
    print(user_role)
    pub_key = user_info[6]
    balance_response = requests.get(
        f'https://hackathon.lsp.team/hk/v1/wallets/{pub_key}/balance')
    print(balance_response.json())
    mt_amount = balance_response.json()["maticAmount"]
    coins_amount = balance_response.json()["coinsAmount"]
    result.append({
        'first_name': user_info[0],
        'last_name': user_info[1],
        'middle_name': user_info[2],
        'login': user_info[3],
        'email': user_info[4],
        'hashed_password': user_info[5],
        'wallet_addres': pub_key,
        'phone_number': user_info[7],
        'last_seen': user_info[8],
        'is_online': user_info[9],
        'about': user_info[10],
        'birth_date': user_info[11],
        'sex': user_info[12],
        'picture_photo': user_info[13],
        'user_role': user_role[0],
        'maticAmount': mt_amount,
        'coinsAmount': coins_amount
    })
    return jsonify({'resp': result})


@app.route('/api/send/ruble', methods=['POST'])
def send_ruble():
    if not request.json or 'sender_id' not in request.json \
            or 'recipient_id' not in request.json \
            or 'amount' not in request.json:
        abort(400)

    sender_pk = Requests.get_sender_private_key(request.json["sender_id"])
    print(sender_pk[0])
    recipient_wallet = Requests.get_recipient_wallet(
        request.json["recipient_id"]
    )
    amount = request.json["amount"]
    print(recipient_wallet[0])
    obj = {
        "fromPrivateKey": str(sender_pk[0]),
        "toPublicKey": str(recipient_wallet[0]),
        "amount": float(amount)

    }
    res = requests.post('https://hackathon.lsp.team/hk/v1/transfers/ruble',
                        json=obj)
    print(res.json())
    if res.json()['transaction']:
        return jsonify({
            'status': '200', 'transactionHash': res.json()['transaction']
        })
    else:
        return jsonify({'status': '501'})


@app.route('/api/rating', methods=['POST'])
def get_rating():
    if not request.json or 'userBalanceSort' not in request.json \
            or 'userNameSort' not in request.json:
        abort(400)
    result = []
    if request.json["userNameSort"] == "INCREASE":
        items = Requests.rating_user_name_asc()
        print(items)
        for item in items:
            balance_response = requests.get(
                f'https://hackathon.lsp.team/hk/v1/wallets/{item[4]}/balance')
            print(balance_response.json())
            coins_amount = balance_response.json()["coinsAmount"]
            result.append({
                'id': item[0],
                'first_name': item[1],
                'last_name': item[2],
                'middle_name': item[3],
                'wallet_addres': item[4],
                'shorten_wallet_addres': f"{item[4][:4]}...{item[4][len(item[4]) - 5:]}",
                'about': item[5],
                'picture_photo': item[6],
                'user_balance': coins_amount
            })
        return jsonify({'resp': result})

    if request.json["userNameSort"] == "DECREASE":
        items = Requests.rating_user_name_desc()
        print(items)
        for item in items:
            balance_response = requests.get(
                f'https://hackathon.lsp.team/hk/v1/wallets/{item[4]}/balance')
            print(balance_response.json())
            coins_amount = balance_response.json()["coinsAmount"]
            result.append({
                'id': item[0],
                'first_name': item[1],
                'last_name': item[2],
                'middle_name': item[3],
                'wallet_addres': item[4],
                'shorten_wallet_addres': f"{item[4][:4]}...{item[4][len(item[4]) - 5:]}",
                'about': item[5],
                'picture_photo': item[6],
                'user_balance': coins_amount
            })
        return jsonify({'resp': result})

    if request.json["userBalanceSort"] == "INCREASE":
        items = Requests.rating_info_for_balance_sort()
        print(items)
        for item in items:
            balance_response = requests.get(
                f'https://hackathon.lsp.team/hk/v1/wallets/{item[4]}/balance')
            print(balance_response.json())
            coins_amount = balance_response.json()["coinsAmount"]
            result.append({
                'id': item[0],
                'first_name': item[1],
                'last_name': item[2],
                'middle_name': item[3],
                'wallet_addres': item[4],
                'shorten_wallet_addres': f"{item[4][:4]}...{item[4][len(item[4]) - 5:]}",
                'about': item[5],
                'picture_photo': item[6],
                'user_balance': coins_amount
            })
        result.sort(key=lambda balance: balance.get('user_balance', ''))
        return jsonify({'resp': result})

    if request.json["userBalanceSort"] == "DECREASE":
        items = Requests.rating_info_for_balance_sort()
        print(items)
        for item in items:
            balance_response = requests.get(
                f'https://hackathon.lsp.team/hk/v1/wallets/{item[4]}/balance')
            print(balance_response.json())
            coins_amount = balance_response.json()["coinsAmount"]
            result.append({
                'id': item[0],
                'first_name': item[1],
                'last_name': item[2],
                'middle_name': item[3],
                'wallet_addres': item[4],
                'shorten_wallet_addres': f"{item[4][:4]}...{item[4][len(item[4]) - 5:]}",
                'about': item[5],
                'picture_photo': item[6],
                'user_balance': coins_amount
            })
        result.sort(
            key=lambda balance: balance.get('user_balance', ''), reverse=True
        )
        return jsonify({'resp': result})


@app.route('/api/sign/event', methods=['POST'])
def sign_up_for_the_event():
    if not request.json or 'user_id' not in request.json \
            or 'event_id' not in request.json:
        abort(400)

    status = Requests.event_sign_up(
        request.json["user_id"],
        request.json["event_id"]
    )
    return jsonify({'status': status})

@app.route('/api/reward/user', methods=['POST'])
def reward_user():
    if not request.json or 'user_id' not in request.json \
            or 'achievement_id' not in request.json:
        abort(400)

    status = Requests.reward_user(
        request.json["user_id"],
        request.json["achievement_id"]
    )
    return jsonify({'status': status})


@app.route('/api/get/nfts', methods=['GET'])
def get_nfts():
    result = []
    nfts = Requests.get_nfts()
    print(nfts)
    text = 'data'
    for nft in nfts:
        result.append({
            'id': nft[0],
            'image': text,
            'header': nft[2],
            'description': nft[3]
        })

    return jsonify({'resp': result})
@app.route('/api/update/user', methods=['POST'])
def update_user_info():
    if not request.json or 'user_id' not in request.json \
            or 'first_name' not in request.json \
            or 'last_name' not in request.json \
            or 'middle_name' not in request.json \
            or 'email' not in request.json \
            or 'birth_date' not in request.json \
            or 'phone_number' not in request.json:
        abort(400)

    user_info = Requests.get_info_to_update(request.json["user_id"])
    print(user_info)
    email_old = user_info[3]
    if request.json["first_name"]:
        first_name = request.json["first_name"]
    else:
        first_name = user_info[0]
    if request.json["last_name"]:
        last_name = request.json["last_name"]
    else:
        last_name = user_info[1]
    if request.json["middle_name"]:
        middle_name = request.json["middle_name"]
    else:
        middle_name = user_info[2]
    if request.json["email"]:
        email = request.json["email"]
        login = request.json["email"]
    else:
        email = user_info[3]
        login = user_info[4]
    if request.json["birth_date"]:
        birth_date = request.json["birth_date"]
    else:
        birth_date = user_info[6]
    if request.json["phone_number"]:
        phone_number = request.json["phone_number"]
    else:
        phone_number = user_info[5]

    status = Requests.update_user_info(request.json["user_id"], first_name,
                                       last_name, middle_name, login, email,
                                       phone_number, birth_date
                                       )
    if status == '200' and not request.json["email"]:
        msg = Message('Изменение данных пользователя на платформе ВТБ',
                      recipients=[email])
        msg.body = "Данные вашего аккаунта на платформе ВТБ были изменены!"
        mail.send(msg)
    if status == '200' and request.json["email"]:
        msg = Message('Изменение данных пользователя на платформе ВТБ',
                      recipients=[email_old])
        msg.body = "Данные вашего аккаунта на платформе ВТБ были изменены! " \
                   f"В том числе - новый логин для входа: {email}"
        mail.send(msg)

        msg = Message('Изменение данных пользователя на платформе ВТБ',
                      recipients=[email])
        msg.body = "Данные вашего аккаунта на платформе ВТБ были изменены! " \
                   "Вы получили это письмо, так как данный " \
                   "адрес электронной почты был указан в качестве " \
                   "нового логина для входа."
        mail.send(msg)
    return jsonify({'resp': status})


# --- +++ Выходцев Егор wf-game-acc@bk.ru ---

"""Дальнейшие изменения производить после этого комментария
При начале работы этот комментарий удалить и выделить участки своего кода по 
примеру выше
Когда будет полностью готов код убрать режим дебага поставив False вместо 
True"""
if __name__ == '__main__':
    app.run(debug=True)
