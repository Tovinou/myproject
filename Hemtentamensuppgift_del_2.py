import machine
import time
import socket
import network
import json

# Class for managing LED control
class LEDController:
    def __init__(self, pin_name="LED"):
        self.led = machine.Pin(pin_name, machine.Pin.OUT)

    def turn_on(self):
        self.led.value(1)

    def turn_off(self):
        self.led.value(0)

    def get_state(self):
        return 'on' if self.led.value() == 1 else 'off'


# Class for managing Wi-Fi connection
class WiFiManager:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wifi_status = network.WLAN(network.STA_IF)

    def connect(self):
        self.wifi_status.active(True)
        self.wifi_status.connect(self.ssid, self.password)
        
        while not self.wifi_status.isconnected():
            time.sleep(1)
            print('Connecting to Wi-Fi...')
        print('Wi-Fi connected successfully!')
        print('IP address:', self.wifi_status.ifconfig()[0])


# Class for managing the web server
class WebServer:
    def __init__(self, led_controller):
        self.led_controller = led_controller
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 80))
        self.sock.listen(5)

    def serve(self):
        try:
            while True:
                conn, addr = self.sock.accept()
                req = conn.recv(1024)
                req_str = str(req)
                print(f'Request: {req_str}')
                
                if '/api/led' in req_str:
                    self.handle_api_request(conn)
                else:
                    self.handle_html_request(req_str, conn)
        except Exception as e:
            print("Exception:", e)
            conn.close()
            self.sock.close()

    def handle_html_request(self, req_str, conn):
        led_on = '/?led=on' in req_str
        led_off = '/?led=off' in req_str
        
        if led_on:
            print('Turning LED on')
            self.led_controller.turn_on()
        elif led_off:
            print('Turning LED off')
            self.led_controller.turn_off()
        
        response = self.generate_html()
        self.send_response(conn, response, content_type='text/html')

    def handle_api_request(self, conn):
        led_state = self.led_controller.get_state()
        json_response = json.dumps({"led": led_state})
        self.send_response(conn, json_response, content_type='application/json')

    def generate_html(self):
        gpio_state = self.led_controller.get_state()
        html = f"""
        <html>
            <head>
                <title>Pico W Web Server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    html {{ font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center; }}
                    h1 {{ color: #0F3376; padding: 2vh; }}
                    button {{ display: inline-block; background-color: #4286f4; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer; }}
                </style>
            </head>
            <body>
                <h1>Pico W Web Server</h1>
                <p>GPIO state: <strong>{gpio_state}</strong></p>
                <p><a href="/?led=on"><button>Turn LED On</button></a></p>
                <p><a href="/?led=off"><button>Turn LED Off</button></a></p>
            </body>
        </html>
        """
        return html

    def send_response(self, conn, response, content_type='text/html'):
        conn.sendall('HTTP/1.1 200 OK\n')
        conn.sendall(f'Content-Type: {content_type}\n')
        conn.sendall('Connection: close\n\n')
        conn.sendall(response)
        conn.close()


# Main program
def main():
    ssid = '*******'           # Use your network
    password = '*********'

    wifi = WiFiManager(ssid, password)
    led_controller = LEDController()
    web_server = WebServer(led_controller)

    wifi.connect()
    web_server.serve()

if __name__ == "__main__":
    main()
