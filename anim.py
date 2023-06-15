import json
import matplotlib.pyplot as plt
import websocket
import numpy as np
from multiprocessing import Process, Queue

# Define an empty array for time intervals
time_intervals = np.array([])
data_buffer = []

def plot_data(queue):
    global time_intervals, data_buffer

    # Initialize the plot
    plt.ion()
    fig = plt.figure(figsize=(10, 8))

    while True:
        if not queue.empty():
            data = queue.get()
            if data is None:
                break

            rh_read = float(data["relative_humidity"])
            so2_read = int(data["SO_ppm"])
            co2_read = float(data["co2_ppm"])
            pm2_5_read = float(data["pm2.5"])
            pm10_0_read = float(data["pm10.0"])
            temperature = float(data["temperature"])

            # Append the current time to the time_intervals array
            time_intervals = np.append(time_intervals, time_intervals[-1] + 3 if time_intervals.size > 0 else 0)

            # Append the data to the buffer
            data_buffer.append((rh_read, so2_read, co2_read, pm2_5_read, pm10_0_read, temperature))

            # Update the figure
            update_figure(fig)

    plt.close(fig)

def update_figure(fig):
    global time_intervals, data_buffer

    plt.figure(fig.number)
    plt.clf()  # Clear the previous plot

    # Temperature subplot
    plt.subplot(321)
    temperature_values = [data[5] for data in data_buffer]
    plt.scatter(time_intervals, temperature_values, c='magenta')
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.title("Temperature")

    # Relative Humidity subplot
    plt.subplot(322)
    rh_values = [data[0] for data in data_buffer]
    plt.scatter(time_intervals, rh_values, c='red')
    plt.xlabel("Time")
    plt.ylabel("Relative Humidity")
    plt.title("RH")

    
    # SO2 subplot
    plt.subplot(323)
    so2_values = [data[1] for data in data_buffer]
    plt.scatter(time_intervals, so2_values, c='blue')
    plt.xlabel("Time")
    plt.ylabel("SO2 (ppm)")
    plt.title("SO2")

    # CO2 subplot
    plt.subplot(324)
    co2_values = [data[2] for data in data_buffer]
    plt.scatter(time_intervals, co2_values, c='green')
    plt.xlabel("Time")
    plt.ylabel("CO2 (ppm)")
    plt.title("CO2")

    # PM2.5 subplot
    plt.subplot(325)
    pm2_5_values = [data[3] for data in data_buffer]
    plt.scatter(time_intervals, pm2_5_values, c='orange')
    plt.xlabel("Time")
    plt.ylabel("PM2.5")
    plt.title("PM2.5")

    # PM10.0 subplot
    plt.subplot(326)
    pm10_0_values = [data[4] for data in data_buffer]
    plt.scatter(time_intervals, pm10_0_values, c='purple')
    plt.xlabel("Time")
    plt.ylabel("PM10.0")
    plt.title("PM10.0")

    plt.tight_layout()
    plt.pause(0.01)

def on_message(ws, message, queue):
    data = json.loads(message)
    print("Message Received:", data)
    queue.put(data)

def start_plotting():
    queue = Queue()

    # Start the plotting process
    plotting_process = Process(target=plot_data, args=(queue,))
    plotting_process.start()

    # Connect to the WebSocket server
    ws = websocket.WebSocketApp("ws://localhost:8080", on_message=lambda ws, msg: on_message(ws, msg, queue))

    # Start the WebSocket connection
    ws.run_forever()

    # Signal the plotting process to exit
    queue.put(None)
    plotting_process.join()

if __name__ == "__main__":
    start_plotting()
