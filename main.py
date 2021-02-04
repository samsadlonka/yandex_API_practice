import os
import sys
from func import get_map

import pygame
import requests

params = {'ll': [37.530887, 55.703118], 'spn': [0.002, 0.002], 'l': 'map'}
# Запишем полученное изображение в файл.
response = get_map(params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                params['spn'][0] += 0.002
                params['spn'][1] += 0.002
            elif event.key == pygame.K_PAGEDOWN:
                params['spn'][0] -= 0.002
                params['spn'][1] -= 0.002
            with open(map_file, 'wb') as file:
                file.write(get_map(params))


    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
