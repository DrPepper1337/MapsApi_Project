import os
import sys

import pygame as pg
import requests


pg.init()
screen = pg.display.set_mode((600, 450))
running = True

lon = "133.795393"
lat = "-25.694776"
delta = 0.00

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_PAGEUP:
                delta += 0.02
            if event.key == pg.K_PAGEDOWN and delta != 0:
                delta -= 0.02
    api_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": "sat"
    }
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pg.image.load(map_file), (0, 0))
    os.remove(map_file)
    pg.display.flip()

pg.quit()