import machine
import time
import socket
import network
import json  # Import json module

# Class for controlling the LED
class LEDController:
    def __init__(self, pin_name):
        self.led = machine.Pin(pin_name, machine.Pin.OUT)

    def turn_on(self):
        self.led.value(1)

    def turn_off(self):
        self.led.value(0)

    def get_state(self):
        return 'On' if self.led.value() == 1 else 'Off'

# Class for managing the Wi-Fi connection
class WiFiManager:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        while not self.wlan.isconnected():
            time.sleep(1)
            print('Connecting to Wi-Fi...')

        print('Wi-Fi connected successfully!')
        print('Network config:', self.wlan.ifconfig())

    def disconnect(self):
        self.wlan.disconnect()

# Class for running the web server and controlling LED through web interface
class WebServer:
    def __init__(self, led_controller):
        self.led_controller = led_controller
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 80))
        self.socket.listen(5)

    def start(self):
        try:
            while True:
                conn, addr = self.socket.accept()
                request = conn.recv(1024).decode()
                print(f"Received request: {request}")
                self._handle_request(request, conn)  # Pass conn to handle_request
        except Exception as e:
            print("Exception -", e)
        finally:
            self.socket.close()

    def _handle_request(self, request, conn):
        if '/?led=on' in request:
            self.led_controller.turn_on()
            print('LED ON')
            self._send_response(conn, self._generate_webpage())
        elif '/?led=off' in request:
            self.led_controller.turn_off()
            print('LED OFF')
            self._send_response(conn, self._generate_webpage())
        elif '/api/led' in request:  # Check for JSON API request
            self.handle_api_request(conn)

    def handle_api_request(self, conn):
        led_state = self.led_controller.get_state()  # Get the state of the LED
        json_response = json.dumps({"led": led_state})  # Create a JSON response
        self._send_response(conn, json_response, content_type='application/json')

    def _generate_webpage(self):
        led_state = self.led_controller.get_state()
        html = f"""
        <html>
        <head>
            <title>Pico W Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                html{{font-family: Helvetica; text-align: center; margin: 0 auto; padding: 20px;}}
                h1{{color: #0F3376;}}
                p{{font-size: 1.5rem;}}
                button{{padding: 16px 40px; font-size: 30px; margin: 10px; border: none; color: white; background-color: #4286f4; border-radius: 5px; cursor: pointer;}}
            </style>
        </head>
        <body>
            <h1>Pico W Web Server</h1>
            <p>GPIO state: <strong>{led_state}</strong></p>
            <p><a href="/?led=on"><button>ON</button></a></p>
            <p><a href="/?led=off"><button>OFF</button></a></p>
        </body>
        </html>
        """
        return html

    def _send_response(self, conn, content, content_type='text/html'):
        conn.sendall(f'HTTP/1.1 200 OK\nContent-Type: {content_type}\nConnection: close\n\n{content}'.encode())
        conn.close()

# main
def main():
    # Initialize components
    wifi_manager = WiFiManager(ssid='*******', password='********')
    led_controller = LEDController(pin_name='LED')
    web_server = WebServer(led_controller)

    # Connect to Wi-Fi
    wifi_manager.connect()

    # Start the web server
    try:
        web_server.start()
    except Exception as e:
        print("Exception -", e)

if __name__ == "__main__":
    main()
