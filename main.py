import os
import sys

import pygame as pg
import requests

pg.init()
screen = pg.display.set_mode((600, 450))
running = True

lon = 37.620070
lat = 55.753630
delta = 0.002

prev_lon = lon
prev_lat = lat
prev_delta = delta

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_PAGEUP:
                prev_delta = delta
                delta *= 2
            if event.key == pg.K_PAGEDOWN and delta != 0.0005:
                prev_delta = delta
                delta /= 2
            if event.key == pg.K_UP:
                prev_lat = lat
                lat += delta * 1.4
            if event.key == pg.K_DOWN:
                prev_lat = lat
                lat -= delta * 1.4
            if event.key == pg.K_LEFT:
                prev_lon = lon
                lon -= delta * 3
            if event.key == pg.K_RIGHT:
                prev_lon = lon
                lon += delta * 3
    api_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": "sat",
    }
    response = requests.get(api_server, params=params)

    if not response:
        lon = prev_lon
        lat = prev_lat
        delta = prev_delta
        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(delta), str(delta)]),
            "l": "sat",
        }
        response = requests.get(api_server, params=params)
        # print("Ошибка выполнения запроса:")
        # print("Http статус:", response.status_code, "(", response.reason, ")")
        # sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pg.image.load(map_file), (0, 0))
    os.remove(map_file)
    pg.display.flip()

pg.quit()
