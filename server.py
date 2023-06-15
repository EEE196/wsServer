import asyncio
import json
import random
import websockets

async def send_sample_data(websocket, path):
    print("Client connected")
    while True:
        data = {
            "relative_humidity": random.uniform(30, 70),
            "SO_ppm": random.randint(0, 10),
            "co2_ppm": random.uniform(400, 1000),
            "pm2.5": random.uniform(10, 50),
            "pm10.0": random.uniform(20, 100)
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(3)  # Wait for 3 seconds before sending the next data point

async def start_server():
    async with websockets.serve(send_sample_data, "localhost", 8080):
        await asyncio.Future()

asyncio.run(start_server())
