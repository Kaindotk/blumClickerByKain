import time
import random

import pyautogui
from loguru import logger

from config import settings

logger.info("Ищем окно блюма...")

blumWindow = (0, 0)

for iteration in range(0, settings.retray_find_blum):
    try:
        blumWindow = pyautogui.locateOnScreen(settings.blumWindowPath, confidence=0.7)
        pyautogui.moveTo(blumWindow)

        logger.success(
            f"Окно успешно найдено! Координаты: x: {blumWindow.left}, y: {blumWindow.top}"
        )

        break

    except Exception as e:
        logger.error(
            f"Не удалось найти окно! Попытка: {iteration}/{settings.retray_find_blum}. Спим и пробуем ещё раз."
        )

        if iteration == settings.retray_find_blum - 1:
            logger.error(
                f"С {settings.retray_find_blum} попыток не удалось найти окно. Перезапусти скрипт и попробуй ещё раз."
            )
            break
        time.sleep(3)

logger.info(
    "Проверяем возможность клейма награды..."
)

try:
    claimButton = pyautogui.locateOnScreen(settings.claimButtonPath, confidence=0.4, region=blumWindow)
    pyautogui.click(claimButton)

    logger.success(
        "Забрали награду!"
    )

    time.sleep(2)
except:
    logger.info(
        "Награда уже забрана..."
    )

try:
    startFarmingButton = pyautogui.locateOnScreen(settings.farmingButtonPath, confidence=0.7, region=blumWindow)
    pyautogui.click(startFarmingButton)

    logger.success(
        "Начали фарм."
    )
except:
    logger.info(
        "Фарминг уже идет..."
    )


playGameButton = pyautogui.locateOnScreen(settings.playGameButtonPath, confidence=0.8, region=blumWindow)
pyautogui.click(playGameButton)

userTickets = settings.tickets - 1

logger.info(
    f"Начинаем играть... Тикетов: {userTickets}"
)

threwError = False
while userTickets != 0:
    time.sleep(3)
    for iteration in range(0, settings.retray_find_blumes):
        while True:
            try:
                allBlumes = list(pyautogui.locateAllOnScreen(settings.blumesPath, confidence=0.73, region=blumWindow))
                blumes = random.choice(allBlumes)

                pyautogui.click(blumes)
            except Exception as e:
                logger.info(
                    f"Не смогли найти блюмы... Попопробуем найти их ещё раз. Попытка {iteration}/{settings.retray_find_blumes}"
                )
                time.sleep(3)
                break

    logger.error(
        f"Блюмы не были найдены. Пробуем найти кнопку новой игры..."
    )

    for iteration in range(0, settings.retray_find_newgame_button):
        try:
            playAgainButton = pyautogui.locateOnScreen(settings.playAgainPath, confidence=0.2,
                                                       region=blumWindow)
            pyautogui.click(playAgainButton)
            logger.success(
                "Кнопка успешно найдена!. Играем дальше."
            )
            break
        except Exception as e:
            logger.error(
                f"Не удалось найти кнопку новой игры. Попытка {iteration}/{settings.retray_find_newgame_button}."
            )
            if iteration == settings.retray_find_newgame_button - 1:
                logger.error(
                    f"Не удалось за {settings.retray_find_newgame_button} попыток найти кнопку."
                )
                threwError = True
                break



    userTickets -= 1
    logger.success(
        f"Тикетов осталось: {userTickets}"
    )

if threwError:
    logger.error(
        f"Скрипт завершился с ошибкой... Не смог найти кнопку новой игры. Попробуй перезапустить скрипт."
    )
else:
    logger.success(
        "Успешно! Все тикеты протыкались. Запустите скрипт для повторной отработки тикетов."
    )