import websockets

import asyncio

import json

import time

import matplotlib.pyplot as plt

from settings import URL_BTC

import ssl

import logging


logging.basicConfig(level=logging.INFO)


ssl_context = ssl.SSLContext()
ssl_context.verify_mode = ssl.CERT_NONE

fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()

time_data = []
cost_data = []


def update_graph() -> None:
    ax.plot(time_data, cost_data, color='b')
    ax.legend([f"Last price: {cost_data[-1]}$"])

    fig.canvas.draw()
    plt.pause(0.1)


async def write_in_file(time_data_list: list, cost_data_list: list) -> None:
    with open('data.txt', 'w+') as file:
        file.write(f" Время {time_data_list} курс {cost_data_list}")


async def main():
    async with websockets.connect(URL_BTC, ssl=ssl_context) as client:
        while True:
            data = json.loads(await client.recv())['data']
            event_time = time.localtime(data['E'] // 1000)
            logging.info(data)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"
            time_data.append(event_time)
            cost_data.append(int(float(data['c'])))
            update_graph()
            await write_in_file(time_data, cost_data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
