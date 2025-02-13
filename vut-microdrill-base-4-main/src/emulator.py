import asyncio as aio
import logging
import random
import paho.mqtt.client as mqtt

logging.basicConfig(filename="base_emulator.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BaseEmulator:
    def __init__(self):
        self.running = True
        self.status_data = []

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT broker.")
            client.subscribe("udrill/base/#")
        else:
            logging.error(f"Failed to connect to MQTT broker. Code {rc}")

    def on_message(self, client, userdata, msg):
        logging.info(f"Received MQTT message: {msg.topic} -> {msg.payload.decode()}")
        if msg.topic == "udrill/base/status":
            aio.create_task(self.print_status())
        elif msg.topic == "udrill/base/test":
            aio.create_task(self.run_system_test())

    async def start_mqtt(self):
        self.mqtt_client.connect("localhost", 1883, 60)
        self.mqtt_client.loop_start()

    async def print_status(self):
        print("\n-- System Status --")
        for value in self.status_data:
            print(value)
        logging.info("Status checked.")
        
        self.mqtt_client.publish("udrill/base/status", str(self.status_data))

    async def print_log(self):
        print("\n-- base_emulator.log --")
        try:
            with open("base_emulator.log", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("Log file is empty.")
        print("------ End of File ------")

    async def run_system_test(self):
        print("\nRunning system test...")

    async def config_menu(self):
        print("\n-- Configuration Menu --")
        print("1. Change Log Level")
        print("2. Exit Configuration")
        choice = input("Enter choice: ")
        if choice == "1":
            level = input("Enter log level (DEBUG, INFO, WARNING, ERROR): ").upper()
            logging.getLogger().setLevel(getattr(logging, level, logging.INFO))
            print(f"Log level set to {level}")
            logging.info(f"Log level changed to {level}")
        elif choice == "2":
            return

    async def main_menu(self):
        while self.running:
            print("\n-- Main Menu --")
            print("1. Status")
            print("2. Configuration")
            print("3. Test Menu")
            print("4. Print Log")
            print("5. Exit")

            choice = input("Enter choice: ")
            if choice == "1":
                await self.print_status()
            elif choice == "2":
                await self.config_menu()
            elif choice == "3":
                await self.run_system_test()
            elif choice == "4":
                await self.print_log()
            elif choice == "5":
                print("\nExiting system...")
                self.running = False
            else:
                print("\nInvalid choice! Try again.")

    async def run(self):
        print("Starting nav-base hardware emulator with MQTT...")
        logging.info("Emulator started.")
        await self.start_mqtt()
        await self.main_menu()

if __name__ == "__main__":
    emulator = BaseEmulator()
    aio.run(emulator.run())
