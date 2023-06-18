import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import websocket
import json
from multiprocessing import Process, Queue

# Define an empty array for time intervals


def plot_data(queue):

    # Initialize the plot

    time_intervals = []
    data_buffer = []
    fig = plt.figure(figsize=(10, 8))
    lines = init_figure(fig)

    def animate(frame):
        update_figure(frame, lines, queue, time_intervals, data_buffer)
        return lines
    
    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.show()


def update_figure(frame, lines, queue, time_intervals, data_buffer):
    # Retrieve data from the queue
    while not queue.empty():
        data = queue.get()
        rh_read = float(data["relative_humidity"])
        so2_read = int(data["SO_ppm"])
        co2_read = float(data["co2_ppm"])
        pm2_5_read = float(data["pm2.5"])
        pm10_0_read = float(data["pm10.0"])
        temperature = float(data["temperature"])

        # Append the current time to the time_intervals array
        time_intervals.append(time_intervals[-1] + 3 if len(time_intervals) > 0 else 0)

        # Append the data to the buffer
        data_buffer.append((temperature, rh_read, so2_read, co2_read, pm2_5_read, pm10_0_read))

    for i, line in enumerate(lines):
        line.set_data(time_intervals, [data[i] for data in data_buffer])

    # Adjust the x-axis limits to show a fixed interval of 30 seconds
    x_min = time_intervals[0]
    x_max = ((time_intervals[-1]//30) * 30) + 30
    for ax in plt.gcf().get_axes():
        ax.set_xlim(x_min, x_max)

    # Calculate y-axis limits based on the current data for each subplot
    for i, line in enumerate(lines):
        y_data = line.get_ydata()
        y_min = min(y_data)
        y_max = max(y_data)
        y_padding = 0.1 * (y_max - y_min)
        ax = line.axes
        ax.set_ylim(y_min - y_padding, y_max + y_padding)  # Update y-axis limits for the current subplot

    return lines


def init_figure(fig):
    plt.figure(fig.number)

    lines = []

    # Temperature subplot
    ax = plt.subplot(321)
    line, = ax.plot([], [])
    plt.xlabel("Time")
    plt.ylabel("Temperature") 
    plt.title("Temperature")
    lines.append(line)

    # Relative Humidity subplot
    ax = plt.subplot(322)
    line, = ax.plot([], [])
    plt.xlabel("Time")
    plt.ylabel("Relative Humidity")
    plt.title("RH")
    lines.append(line)

    # SO2 subplot
    ax = plt.subplot(323)
    line, = ax.plot([], [])
    plt.xlabel("Time")
    plt.ylabel("SO2 (ppm)")
    plt.title("SO2")
    lines.append(line)

    # CO2 subplot
    ax = plt.subplot(324)
    line, = ax.plot([], [])
    plt.xlabel("Time")
    plt.ylabel("CO2 (ppm)")
    plt.title("CO2")
    lines.append(line)

    # PM2.5 subplot
    ax = plt.subplot(325)
    line, = ax.plot([], [])
    plt.xlabel("Time")
    plt.ylabel("PM2.5")
    plt.title("PM2.5")
    lines.append(line)

    # PM10.0 subplot
    ax = plt.subplot(326)
    line, = ax.plot([], [])
    plt.xlabel("Time")
    plt.ylabel("PM10.0")
    plt.title("PM10.0")
    lines.append(line)

    plt.tight_layout()

    return lines


def on_message(ws, message, queue):
    # Parse the message
    data = json.loads(message)
    # Add the data to the queue
    queue.put(data)


def start_plotting():
    # Create a queue for inter-process communication
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
