import sys

import requests


# Получение первого топонима из ответа геокодера.
def geocoder(params: dict):
    url = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json"}

    for k, v in params.items():
        geocoder_params[k] = v

    response = requests.get(url, params=geocoder_params)

    if not response:
        return response.reason

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym


def get_toponym_ll_and_span(toponym):
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = "{dx},{dy}".format(**locals())

    return ll, span


def get_image(ll, spn, my_map):
    ll = ','.join(list(map(str, ll)))
    spn = ','.join(list(map(str, spn)))
    params = {
        "ll": ll,
        "l": my_map,
        'spn': spn,
        'size': '450,450'
    }
    url = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(url, params=params)
    return response.content
