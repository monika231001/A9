import cv2
import numpy as np
import http.server
import socketserver
import socket
import os
import threading
import time

# Global variable for direction
current_direction = "Straight"

# Function to get Pi's IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

IP = get_ip_address()
PORT = 8080
SSID = "Airtel_2.4G"
PASSWORD = "SuperSpider@90"

# HTML content with buttons and direction display
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Pi Control</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #FF6F61, #FF8C00);
            color: white;
            text-align: center;
            padding: 50px;
        }}
        h1 {{ font-size: 2.5em; }}
        button {{
            padding: 15px 30px;
            margin: 10px;
            background-color: #FF6F61;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.2em;
        }}
        button:hover {{ background-color: #FF8C00; }}
        #direction {{ font-size: 1.5em; margin-top: 20px; }}
        #gameArea {{ display: none; margin-top: 20px; }}
        .cell {{
            width: 50px;
            height: 50px;
            border: 1px solid white;
            display: inline-block;
            font-size: 24px;
            line-height: 50px;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <h1>Raspberry Pi Control Panel</h1>
    <p>IP Address: {IP}</p>
    <button onclick="window.open('https://www.youtube.com/watch?v=BCBwmjX81Xc', '_blank')">About College</button>
    <button onclick="alert('Entertainment TBD - Add a link!')">Entertainment</button>
    <button onclick="window.open('https://www.youtube.com/watch?v=HkvVaj_28C8', '_blank')">Music</button>
    <button onclick="showGame()">Games (Tic-Tac-Toe)</button>
    <p id="direction">Direction: {current_direction}</p>
    <div id="gameArea"></div>

    <script>
        let currentPlayer = 'X';
        let gameBoard = ['', '', '', '', '', '', '', '', ''];
        function showGame() {{
            document.getElementById('gameArea').style.display = 'block';
            document.getElementById('gameArea').innerHTML = `
                <div>
                    <div class="cell" onclick="play(0)"></div>
                    <div class="cell" onclick="play(1)"></div>
                    <div class="cell" onclick="play(2)"></div>
                </div>
                <div>
                    <div class="cell" onclick="play(3)"></div>
                    <div class="cell" onclick="play(4)"></div>
                    <div class="cell" onclick="play(5)"></div>
                </div>
                <div>
                    <div class="cell" onclick="play(6)"></div>
                    <div class="cell" onclick="play(7)"></div>
                    <div class="cell" onclick="play(8)"></div>
                </div>
            `;
        }}
        function play(index) {{
            if (gameBoard[index] === '') {{
                gameBoard[index] = currentPlayer;
                document.getElementsByClassName('cell')[index].innerText = currentPlayer;
                currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
            }}
        }}
        // Update direction dynamically (polling placeholder)
        setInterval(() => {{
            document.getElementById('direction').innerText = "Direction: {current_direction}";
        }}, 1000);
    </script>
</body>
</html>
"""

# Custom HTTP handler
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        global current_direction
        html = html_content.replace("{current_direction}", current_direction)
        self.wfile.write(html.encode("utf-8"))

# Camera processing function
def camera_process():
    global current_direction
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open USB camera.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)