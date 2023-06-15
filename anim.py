import json
import matplotlib.pyplot as plt
import websocket
import numpy as np

# Define an empty array for time intervals
time_intervals = np.array([])

def on_message(ws, message):
        print("message Reiceived")
        data = json.loads(message)
        print(data)

        rh_read = float(data["relative_humidity"])
        so2_read = int(data["SO_ppm"])
        co2_read = float(data["co2_ppm"])
        pm2_5_read = float(data["pm2.5"])
        pm10_0_read = float(data["pm10.0"])

        # Append the current time to the time_intervals array
        time_intervals = np.append(time_intervals, t_read)

        # Create separate subplots for each variable
        plt.figure(figsize=(10, 6))

        # Relative Humidity subplot
        plt.subplot(321)
        plt.scatter(time_intervals, rh_read, c='red')
        plt.xlabel("Time")
        plt.ylabel("Relative Humidity")
        plt.title("RH")

        # SO2 subplot
        plt.subplot(322)
        plt.scatter(time_intervals, so2_read, c='blue')
        plt.xlabel("Time")
        plt.ylabel("SO2 (ppm)")
        plt.title("SO2")

        # CO2 subplot
        plt.subplot(323)
        plt.scatter(time_intervals, co2_read, c='green')
        plt.xlabel("Time")
        plt.ylabel("CO2 (ppm)")
        plt.title("CO2")

        # PM2.5 subplot
        plt.subplot(324)
        plt.scatter(time_intervals, pm2_5_read, c='orange')
        plt.xlabel("Time")
        plt.ylabel("PM2.5")
        plt.title("PM2.5")
        # PM10.0 subplot
        plt.subplot(325)
        plt.scatter(time_intervals, pm10_0_read, c='purple')
        plt.xlabel("Time")
        plt.ylabel("PM10.0")
        plt.title("PM10.0")
        
        plt.tight_layout()
        plt.pause(0.01)
        print('mark');
        plt.show()

def start_plotting():
    # Initialize the plot
    plt.ion()
    plt.figure()

    # Connect to the Websocket server
    ws = websocket.WebSocketApp("ws://localhost:8080", on_message=on_message)

    # Start the WebSocket connection
    ws.run_forever()

if __name__ == "__main__":
    start_plotting()
