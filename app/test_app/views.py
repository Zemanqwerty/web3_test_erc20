from ctypes.wintypes import RECT
import errno
from multiprocessing.spawn import prepare
from pydoc import cli
from socket import socket
from tkinter.tix import Tree
from aiohttp import web
import json
import aiohttp
import jinja2
from loguru import logger
from app.settings import BASE_DIR
import psycopg
import hashlib
from .. import settings
import asyncio
from aiohttp_auth import auth
from datetime import datetime as dt
from aiohttp import ClientSession
from typing import List, Union
import aiohttp_jinja2
import asyncio
import json
import time
import requests
import websockets as ws

# from ..settings import debug_settings as setup_debug


# setup_debug()


# убрать соин прайс в транзакциях в приницпе, пофиксить интеджер в коин прайс, пофиксить одинаковые имена проектов в создании проектов

# формируем файл логов
logger.add(f'{BASE_DIR}/logs/info.json', format='{time} {level} {message}',
           level='INFO', rotation='100 KB', compression='zip', serialize=True)


# декоратор для аутентификации пользователя
def api_authentication_check(function):
    async def wrapped(request: web.Request) -> web.Response:
        # получаем данные пользователя
        user = await auth.get_auth(request)
        # если пользователь не авторизован
        if user is None:
            # формируем json
            # response_obj = {
            #     'status': 'failed',
            #     'message': 'user is not authenticated'
            # }

            # редирект на страницу авторизации
            location = request.app.router['autz'].url_for()
            raise web.HTTPFound(location=location)
            # return web.Response(text=json.dumps(response_obj), status=400)
        # если пользователь авторизован
        else:
            return await function(request)
    return wrapped


# декоратор для аутентификации пользователя
def api_admin_authentication_check(function):
    async def wrapped(request: web.Request) -> web.Response:
        # получаем данные пользователя
        user = await auth.get_auth(request)
        # если пользователь не авторизован
        if user is None:
            # формируем json
            # response_obj = {
            #     'status': 'failed',
            #     'message': 'user is not authenticated'
            # }

            # редирект на страницу авторизации
            location = request.app.router['autz'].url_for()
            raise web.HTTPFound(location=location)
            # return web.Response(text=json.dumps(response_obj), status=400)
        # если пользователь авторизован
        else:
            try:
                async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn: 
                    async with conn.cursor() as cur:
                        await cur.execute(
                            f"SELECT is_admin FROM users WHERE username = '{user}';"
                        )

                        user_status = await cur.fetchone()

                        if user_status == False:

                            await cur.close()
                            await conn.close()

                            location = request.app.router['autz'].url_for()
                            raise web.HTTPFound(location=location)

                        else:
                            return await function(request)
            except psycopg.Error as error:
                print(error)

                location = request.app.router['autz'].url_for()
                raise web.HTTPFound(location=location)
            
    return wrapped



@logger.catch()
@api_authentication_check
async def api_logout(request):
    try:
        # выводим пользователя из сети
        await auth.forget(request)
        location = request.app.router['main'].url_for()
        return web.HTTPFound(location=location)
    except:
        # формируем json
        response_obj = {
            'status': 'failed',
            'message': "logout failed"
        }
        return web.Response(text=json.dumps(response_obj), status=500)


# функция регистрации пользователя
@logger.catch()
async def api_registration(request: web.Request) -> web.Response:
    try:
        # получаем json и сохраняем в переменную
        json_data = await request.json()

        # обращаемся к словарю по ключу
        username = json_data['username']
        password = json_data['password']
        print(username, password)
    
        # соединение с БД
        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn: 
            async with conn.cursor() as cur:
                logger.info('REGISTRATION DB connection open')
                # проверяем наличие пользователя
                await cur.execute(
                    f"SELECT * FROM USERS WHERE username = '{username}';"
                )

                db_response = await cur.fetchone()

                if db_response is None:
                    # хешируем пароль пользователя
                    hash_password = hashlib.sha256(password.encode()).hexdigest()
                        
                    await cur.execute(
                        f"INSERT INTO users (username, password) VALUES (%s, %s);",
                        (username, hash_password)
                    )

                    logger.info(f'NEW USER --- {username}')

                    # сохраняем изменения и закрываем подключение к БД
                    await cur.close()
                    await conn.commit()
                    await conn.close()

                    logger.info(f'REGISTRATION DB connection closed')

                    # формируем json
                    json_response = {
                        'status': 'success',
                        'message': f'account {username} has been created succesfully'
                    }
                    return web.Response(text=json.dumps(json_response), status=200)
                        
                else:
                    # закрываем соединение с БД
                    await cur.close()
                    await conn.close()

                    logger.info(f'REGISTRATION DB connection closed')

                    # формируем json
                    json_response = {
                        'status': 'failed',
                        'message': f'user {username} already created'
                    }
                    return web.Response(text=json.dumps(json_response), status=200)
    # исключение при подключении к БД
    except psycopg.Error as error:
        logger.info(f'REGISTRATION DB connection failed')

        print(error)

        json_response = {
            'status': 'failed',
            'message': 'connection to DataBase failed'
        }
        return web.Response(text=json.dumps(json_response), status=500)
    # исключение при работе с json
    except json.JSONDecodeError as error:
        logger.info(f'REGISTRATION get data failed')

        json_response = {
            'status': 'failed',
            'message': 'get data failed'
        }
        return web.Response(text=json.dumps(json_response), status=500)


# функция регистрации пользователя
@logger.catch()
async def api_authorization(request: web.Request) -> web.Response:
    try:
        # получаем json и сохраняем в переменную
        json_data = await request.json()

        # обращаемся к словарю по ключу
        username = json_data['username']
        password = json_data['password']

        # соединение с БД
        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:

                logger.info('AUTHORIZATION DB connection open')

                # проверяем наличие пользователя с таким именем
                await cur.execute(
                    f"SELECT username FROM users WHERE username = '{username}';"
                )

                db_user_response = await cur.fetchone()
                    
                logger.info(f'AUTHORIZATION DB get username {username}')

                # если пользователь не найден
                if db_user_response is None:
                        
                # закрывем соединение с БД
                    await cur.close()
                    await conn.close()

                    logger.info('AUTHORIZATION DB connection closed')

                    json_response = {
                        'status': 'failed',
                        'message': f'user with username {username} not found'
                    }

                    return web.Response(text=json.dumps(json_response), status=200)
                    
                # если пользователь существует
                else:
                    # хешируем пароль для сравнения
                    hash_password = hashlib.sha256(password.encode()).hexdigest()

                    # получаем из БД хэшированый пароль пользователя
                    await cur.execute(
                        f"SELECT password FROM users WHERE username = '{username}';"
                    )

                    db_password_response = (await cur.fetchone())[0]

                    logger.info(f'AUTHORIZATION DB get password for user {username}')

                    # если введённый пароль и пароль из БД совпадают
                    if db_password_response == hash_password:
                            
                        # авторизуем и запоминаем пользователя
                        await auth.remember(request, username)

                        logger.info(f'user {username} has logged in')
                            
                        # закрываем соединение с БД
                        await cur.close()
                        await conn.close()

                        logger.info('AUTHORIZATION DB connection closed')

                        json_response = {
                            'status': 'success',
                            'message': f'user {username} has logged in'
                        }

                        return web.Response(text=json.dumps(json_response), status=200)
                        
                    # если пароли не совпадают
                    else:
                        # закрываем соединение с БД
                        await cur.close()
                        await conn.close()

                        logger.info('AUTHORIZATION DB connection closed')

                        json_response = {
                            'status': 'failed',
                            'message': 'incorrect password',
                        }

                        return web.Response(text=json.dumps(json_response), status=200)
        
    # исключение при подключении к БД
    except psycopg.Error:

        logger.info('AUTHORIZATION DB connection failed')

        json_response = {
            'status': 'failed',
            'message': 'connection to DataBase failed'
        }

        return web.Response(text=json.dumps(json_response), status=500)
    # исключение при работе с json
    except json.JSONDecodeError:

        logger.info('AUTHORIZATION get data failed')

        json_response = {
            'status': 'failed',
            'message': 'get data failed'
        }

        return web.Response(text=json.dumps(json_response), status=500)


@api_authentication_check
async def api_create_new_project(request: web.Request) -> web.Response:
    try:
        user = await auth.get_auth(request)

        json_data = await request.json()

        project_name = json_data['project_name']
        project_site = json_data['project_site']
        project_owner = str(user)
        coin_address = json_data['smart_contract']
        coin_count = json_data['coin_count']
        coin_price = json_data['coin_price']

        
        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:
                
                await cur.execute(
                    f"SELECT * FROM projects WHERE project_name = '{project_name}';"
                )
                
                if await cur.fetchone() != None:
                    json_response = {
                        'status': 'failed',
                        'message': f'Project with name {project_name} already registered'
                    }
                    
                    return web.Response(text=json.dumps(json_response), status=500)
                
                await cur.execute(
                    f"SELECT id_user FROM users WHERE username = '{project_owner}';"
                )
                
                p_owner_user_id = (await cur.fetchone())[0]

                await cur.execute(
                    f"INSERT INTO projects (project_name, project_site, project_owner) VALUES (%s, %s, %s)",
                    (project_name, project_site, p_owner_user_id)
                )

                await cur.execute(
                    f"SELECT id_project FROM projects WHERE project_name = '{project_name}';"
                )
                
                project_id = (await cur.fetchone())[0]
                
                await cur.execute(
                    f"INSERT INTO coins (id_coin, smart_contract, start_coin_count, act_coin_count, coin_price) VALUES (%s, %s, %s, %s, %s)",
                    (project_id, coin_address, coin_count, coin_count, coin_price)
                )

                await cur.close()
            await conn.commit()
            await conn.close()
        
        json_response = {
            'status': 'success',
            'message': 'project will be send to moderation',
        }
        
        return web.Response(text=json.dumps(json_response), status=200)

    except psycopg.Error:

        json_response = {
            'status': 'failed',
            'message': 'connection to DataBase failed'
        }

        return web.Response(text=json.dumps(json_response), status=500)

    except json.JSONDecodeError:

        json_response = {
            'status': 'failed',
            'message': 'get data failed'
        }

        return web.Response(text=json.dumps(json_response), status=500)


@api_authentication_check
async def api_create_new_transaction(request: web.Request) -> web.Response:
    try:
        json_data = await request.json()

        t_user = await auth.get_auth(request)
        t_project = json_data['project_name']
        t_address = json_data['project_address']
        count_coin = int(json_data['coins_count'])
        user_wallet = json_data['wallet']

        print(json_data)
        
        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:
                    
                await cur.execute(
                    f"SELECT id_user FROM users WHERE username = '{t_user}';"
                )
                    
                t_id_user = (await cur.fetchone())[0]
                    
                await cur.execute(
                    f"SELECT id_project FROM projects WHERE project_name = '{t_project}';"
                )
                    
                t_id_project = (await cur.fetchone())[0]
                
                await cur.execute(
                    f"INSERT INTO trnsactions (transaction_user, transaction_project, transaction_coin_count, transaction_wallet) VALUES (%s, %s, %s, %s)",
                    (t_id_user, t_id_project, count_coin, user_wallet)
                )

                await cur.execute(
                    f"UPDATE coins SET act_coin_count = act_coin_count - {count_coin} WHERE smart_contract = '{t_address}';"
                )
                    
                await cur.close()
            await conn.commit()
            await conn.close()

        json_response = {
            'status': 'success',
            'message': 'transaction created successfuly'
        }

        return web.Response(text=json.dumps(json_response), status=200)
        
    except psycopg.Error as error:
        print(error)

        json_response = {
            'status': 'failed',
            'message': f'connection to DataBase failed: {error}'
        }

        return web.Response(text=json.dumps(json_response), status=500)
        
    except json.JSONDecodeError:
        json_response = {
            'status': 'failed',
            'message': 'get data failed'
        }

        return web.Response(text=json.dumps(json_response), status=500)


async def to_consider(request: web.Request) -> web.Response:
    try:
        json_data = await request.json()

        id_project = json_data['id_project']
        project_status = json_data["project_status"]

        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:

                await cur.execute(
                    f"UPDATE projects SET project_status = {project_status} WHERE id_project = {id_project};"
                )

                await cur.close()
            await conn.commit()
            await conn.close()

        return web.Response(text=json.dumps({'status': 'success'}), status=200)
            
    except json.JSONDecodeError as error:
        print(error)
    except psycopg.Error as error:
        print(error)


async def to_finish(request: web.Request) -> web.Response:
    try:
        json_data = await request.json()

        id_project = json_data['id_project']

        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:

                await cur.execute(
                    f"UPDATE projects SET project_status = 3 WHERE id_project = {id_project};"
                )

                await cur.close()
            await conn.commit()
            await conn.close()

        return web.Response(text=json.dumps({'status': 'success'}), status=200)
            
    except json.JSONDecodeError as error:
        return web.Response(text=json.dumps({'status': 'failed'}), status=500)
    except psycopg.Error as error:
        return web.Response(text=json.dumps({'status': 'failed'}), status=500)


@api_admin_authentication_check
async def send_transaction_to_user(request: web.Request) -> web.Response:
    try:
        json_data = await request.json()

        id_transaction = json_data['transaction_id']

        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:

                await cur.execute(
                    f"UPDATE trnsactions SET transaction_status = 2 WHERE id_transaction = {id_transaction};"
                )

                await cur.close()
            await conn.commit()
            await conn.close()

        return web.Response(text=json.dumps({'status': 'success'}), status=200)
            
    except json.JSONDecodeError as error:
        return web.Response(text=json.dumps({'status': 'failed'}), status=500)
    except psycopg.Error as error:
        return web.Response(text=json.dumps({'status': 'failed'}), status=500)



# ----------CLIENT USERS VIEWS----------

@aiohttp_jinja2.template('client/registration_page.html')
async def registration_page(requset):
    return {}

@aiohttp_jinja2.template('client/authorization_page.html')
async def authorization_page(requset):
    return {}

@aiohttp_jinja2.template('client/projects_page.html')
async def main_page(request):
    project_information = ''

    try:
        try:
            get_request = request.query['search']
            print(get_request)

            async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
                async with conn.cursor() as cur:

                    try:
                        await cur.execute(
                            f"SELECT id_project, project_name, project_site, smart_contract, coin_price, start_coin_count, act_coin_count FROM projects, coins WHERE (project_name = '{get_request}') and (id_project = id_coin);"
                        )
                        print(1)
                        projects_list = await cur.fetchall()
                        print(2)
                        print(projects_list)
                        project_information = projects_list
                    except:
                        print('get_projects_error')
                        project_information = None

                    await cur.close()
                    await conn.close()
        except:
            async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
                async with conn.cursor() as cur:

                    try:
                        await cur.execute(
                            f"SELECT id_project, project_name, project_site, smart_contract, coin_price, start_coin_count, act_coin_count FROM projects, coins WHERE (project_status = 2) and (id_project = id_coin);"
                        )
                        
                        projects_list = await cur.fetchall()
                        
                        print(projects_list)
                        project_information = projects_list
                    except:
                        print('get_projects_error')
                        project_information = None

                    await cur.close()
                    await conn.close()
    

        user = await auth.get_auth(request)
        print(user)

        procents_list = []

        for item in project_information:
            procent = int(item[6]) / (int(item[5]) / 100)
            procents_list.append({'id': item[0], 'procent': procent})

        response_btc_price = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
        btc_data = response_btc_price.json()
        btc_price = btc_data["data"]["amount"]

        response_eth_price = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot")
        eth_data = response_eth_price.json()
        eth_price = eth_data["data"]["amount"]
                    
        response_sol_price = requests.get("https://api.coinbase.com/v2/prices/SOL-USD/spot")
        sol_data = response_sol_price.json()
        sol_price = sol_data["data"]["amount"]

        return {
            'projects': project_information,
            'procents': procents_list,
            'btc_price': btc_price,
            'eth_price': eth_price,
            'sol_price': sol_price,
            'user': user
        }
                    
    except:
        return {
            'message': 'sorry, we have a little troubles :('
        }


@api_authentication_check
@aiohttp_jinja2.template('client/account_page.html')
async def account_page(request: web.Request) -> web.Response:
    user = await auth.get_auth(request)

    async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
        async with conn.cursor() as cur:
            
            await cur.execute(
                f"SELECT id_user FROM users WHERE username = '{user}';"
            )

            user_id = (await cur.fetchone())[0]

            await cur.execute(
                f"SELECT project_name, transaction_coin_count FROM projects, trnsactions WHERE (transaction_user = '{user_id}') AND (transaction_project = id_project);"
            )

            transaction_list = await cur.fetchall()
            print(transaction_list)
        
        await cur.close()
        await conn.close()

    return {'username': user,
            'transactions_list': transaction_list}

@api_authentication_check
@aiohttp_jinja2.template('client/create_project_page.html')
async def create_new_project(request):
    return {}

@api_authentication_check
@aiohttp_jinja2.template('client/cur_project.html')
async def cur_project(request):
    try:
        project_name = request.url.raw_path.split('/')[1]
        print(project_name)

        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:

                await cur.execute(
                    f"SELECT project_name, project_site, project_status, smart_contract, act_coin_count, coin_price FROM projects, coins WHERE (project_name = '{project_name}') AND (id_project = id_coin);"
                )

                project_full_information = await cur.fetchone()
                print(project_full_information)

                response_eth_price = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot")
                eth_data = response_eth_price.json()
                eth_price = eth_data["data"]["amount"]

                return {'project': project_full_information, 'eth_price': eth_price}
    except psycopg.Error as error:
        return print(error)
    except:
        print('error')
        # location = request.app.router['main'].url_for()
        # raise web.HTTPFound(location=location)




# ----------CLIENT ADMINS VIEWS----------

@api_admin_authentication_check
@aiohttp_jinja2.template('admin/admin_main_page.html')
async def main_admin_page(request):
    try:
        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:
                
                await cur.execute(
                    f"SELECT id_project, project_name, project_site, smart_contract, start_coin_count, coin_price FROM projects, coins WHERE (project_status = 1) AND (id_project = id_coin);"
                )

                projects_list = await cur.fetchall()
                print(projects_list)
        
                await cur.close()
            await conn.close()

        return {'projects_list': projects_list}

    except psycopg.Error as error:
        return {'error': 'DataBase error'}


@api_admin_authentication_check
@aiohttp_jinja2.template('admin/admin_active_page.html')
async def acive_project_page(request):
    try:
        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:

                await cur.execute(
                    f"SELECT id_project, project_name, project_site, smart_contract, act_coin_count, coin_price FROM projects, coins WHERE (project_status = 2) AND (id_project = id_coin);"
                )

                project_list = await cur.fetchall()
                print(project_list)

                await cur.close()
            await conn.close()

        return {'project_list': project_list}

    except psycopg.Error:
        return {'error': 'DataBase error'}


@api_admin_authentication_check
@aiohttp_jinja2.template('admin/admin_send_tocen_page.html')
async def send_tocken_page(request):
    try:
        async with await psycopg.AsyncConnection.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, port=settings.DB_PORT, host=settings.DB_HOST) as conn:
            async with conn.cursor() as cur:

                await cur.execute(
                    f"SELECT coin_price, transaction_coin_count, transaction_wallet, id_transaction FROM coins, trnsactions WHERE (transaction_status = 1) AND (id_coin = transaction_project);"
                )

                project_list = await cur.fetchall()
                print(project_list)

                await cur.close()
            await conn.close()

        response_eth_price = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot")
        eth_data = response_eth_price.json()
        eth_price = eth_data["data"]["amount"]

        return {'project_list': project_list, 'cur_eth_price': eth_price}

    except psycopg.Error:
        return {'error': 'DataBase error'}