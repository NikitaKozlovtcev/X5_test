import asyncio
import logging
import os
from datetime import datetime

import aiohttp
from aiohttp import ClientTimeout

API_KEY_WEATHERAPI = os.getenv("API_KEY_WEATHERAPI")
API_KEY_WEATHERSTACK = os.getenv("API_KEY_WEATHERSTACK")
API_KEY_OPENWEATHERMAP = os.getenv("API_KEY_OPENWEATHERMAP")


log = logging.getLogger(__name__)


async def weatherapi_metod(response):
    """http://api.weatherapi.com"""
    resp = {
        'weatherapi': 'metod',
        'time': datetime.strptime(response['current']['last_updated'], '%Y-%m-%d %H:%M'),
        'temperature': response['current']['temp_c'],
    }
    return resp


async def weatherstack_metod(response):
    """http://api.weatherstack.com"""
    resp = {
        'weatherstack': 'metod',
        'time': datetime.strptime(response['location']['localtime'], '%Y-%m-%d %H:%M'),
        'temperature': response['current']['temperature'],
    }
    return resp


async def openweathermap_metod(response: dict):
    """api.openweathermap.org"""
    resp = {
        'openweathermap': 'metod',
        'time': datetime.utcfromtimestamp(response['dt']),
        'temperature': response['main']['temp'],
    }
    return resp


URLS = {
    'weatherapi.com': {
        'url': f'http://api.weatherapi.com/v1/current.json?'
               f'key={API_KEY_WEATHERAPI}&'
               f'q=Moscow'
               f'&aqi=yes',
        'parse_metod': weatherapi_metod,
    },
    'weatherstack.com': {
        'url': f'http://api.weatherstack.com/current?'
               f'access_key={API_KEY_WEATHERSTACK}&'
               f'query=moscow',
        'parse_metod': weatherstack_metod,
    },
    'openweathermap.org': {
        'url': f'http://api.openweathermap.org/data/2.5/weather?'
               f'lat=55.75&'
               f'lon=37.62&'
               f'appid={API_KEY_OPENWEATHERMAP}'
               f'&units=metric',
        'parse_metod': openweathermap_metod,
    }
}


async def fetch(session, api_name: str, params: dict):
    try:
        async with session.get(params['url']) as response:
            resp = await response.json()
            response = {
                'api': api_name,
                'response': await params['parse_metod'](resp),
            }
            return response
    except asyncio.TimeoutError:
        response = {
            'api': api_name,
            'error': TimeoutError,
        }
        log.warning(TimeoutError)
        return response
    except Exception as err:
        response = {
            'api': api_name,
        }
        return response


async def get_weather(timeout: float):
    resp = {}
    tasks = []
    time_errors = 0
    timeout = ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for api, params in URLS.items():
            tasks.append(fetch(session, api, params))
        responses = await asyncio.gather(*tasks)

        for response in responses:
            if response['api'] in URLS.keys():
                if 'response' in response:
                    resp['data'] = response['response']
                    return resp, time_errors
                elif 'error' in response:
                    time_errors += 1
        return resp, time_errors
