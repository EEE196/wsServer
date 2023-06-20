
import asyncio
import csv
import json
import websockets

async def send_sample_data(websocket, path):
    print("Client connected")
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = {
                "co2_ppm": float(row["CO2 ppm"]),
                "SO_ppm": float(row["SO2 ppm"]),
                "temperature": float(row["Temperature °"]),
                "relative_humidity": float(row["Relative Humidity"]),
                "pm2.5": float(row["MC2.5 #/cm^3"]),
                "pm10.0": float(row["MC10.0 #/cm^3"]),
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(.2)  # Wait for 3 seconds before sending the next data point

async def start_server():
    async with websockets.serve(send_sample_data, "localhost", 8080):
        await asyncio.Future()

asyncio.run(start_server())
