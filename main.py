#  ____  _          _  ____          _
# |  _ \(_)_  _____| |/ ___|__ _ ___| |_
# | |_) | \ \/ / _ \ | |   / _` / __| __|
# |  __/| |>  <  __/ | |__| (_| \__ \ |_
# |_|   |_/_/\_\___|_|\____\__,_|___/\__|

# By @Paylicier under the MIT License
# GitHub: https://github.com/Paylicier/PixelCast  
# Made for neon ysws

import time
import board
import displayio
import terminalio
import framebufferio
import rgbmatrix
from adafruit_display_text import label
import requests
import json

# Todo - init wifi

# API endpoints (change them if needed)
REALTIME_URL = "https://pixelcast.notri1.workers.dev/weather/realtime"
FORECAST_URL = "https://pixelcast.notri1.workers.dev/weather/forecast"
NEWS_URL = "https://pixelcast.notri1.workers.dev/news?lang=en-US"

# Coordinates for weather things
LAT = "48.86"  # Paris
LON = "2.34"

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

litlnb = {
    '0': [
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1]
    ],
    '1': [
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0]
    ],
    '2': [
        [1, 1, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 1, 1]
    ],
    '3': [
        [1, 1, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 1, 1]
    ],
    '4': [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [0, 0, 0, 1]
    ],
    '5': [
        [1, 1, 1, 1],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [1, 1, 1, 1]
    ],
    '6': [
        [1, 1, 1, 1],
        [1, 1, 0, 0],
        [1, 0, 1, 1],
        [1, 1, 1, 1]
    ],
    '7': [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0]
    ],
    '8': [
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1]
    ],
    '9': [
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [0, 0, 0, 1]
    ],
    'minus': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0]
    ]
}

mini_font = {
    'A': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    'B': [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0]
    ],
    'C': [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 1, 1]
    ],
    'D': [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0]
    ],
    'E': [
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1]
    ],
    'F': [
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0]
    ],
    'G': [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1]
    ],
    'H': [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    'I': [
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 1, 0]
    ],
    'J': [
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    'K': [
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 0],
        [1, 0, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    'L': [
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1]
    ],
    'M': [
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    'N': [
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [1, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    'O': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    'P': [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0]
    ],
    'Q': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 1, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1]
    ],
    'R': [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    'S': [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [1, 1, 1, 0]
    ],
    'T': [
        [1, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ],
    'U': [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    'V': [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 0]
    ],
    'W': [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1]
    ],
    'X': [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    'Y': [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ],
    'Z': [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1]
    ],
    '0': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    '1': [
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 1]
    ],
    '2': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1]
    ],
    '3': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    '4': [
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1]
    ],
    '5': [
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [1, 1, 1, 0]
    ],
    '6': [
        [0, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    '7': [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ],
    '8': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    '9': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    '.': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0]
    ],
    ',': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]
    ],
    '!': [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0]
    ],
    '?': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0]
    ],
    ':': [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    '-': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    '+': [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    ' ': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
}

font = terminalio.FONT

group = displayio.Group()

progress_palette = displayio.Palette(1)

current_news_index = 0
display_cycle = 0

def create_label(text, color, x, y, scale=1):
    return label.Label(font, text=text, color=color, x=x, y=y, scale=scale)

def draw_mini_text(text, x, y, color):
    text_group = displayio.Group()
    for i, char in enumerate(text.upper()):
        if char in mini_font:
            for row in range(6):
                for col in range(4):
                    if mini_font[char][row][col]:
                        pixel_bitmap = displayio.Bitmap(1, 1, 1)
                        pixel_palette = displayio.Palette(1)
                        pixel_palette[0] = color
                        pixel_tile = displayio.TileGrid(pixel_bitmap, pixel_shader=pixel_palette, x=x + i * 4 + col, y=y + row)
                        text_group.append(pixel_tile)
    return text_group

def clear_group(group):
    while len(group) > 0:
        group.pop()

def get_weather_data():
    try:
        realtime_params = {"lat": LAT, "lon": LON}
        realtime_response = requests.get(REALTIME_URL, params=realtime_params)
        realtime_data = realtime_response.json()

        forecast_params = {"lat": LAT, "lon": LON}
        forecast_response = requests.get(FORECAST_URL, params=forecast_params)
        forecast_data = forecast_response.json()

        return realtime_data, forecast_data
    except Exception as e:
        print("broken weather", e)
        return None, None
        
def get_news_data():
    try:
        news_response = requests.get(NEWS_URL)
        news_data = news_response.json()
        return news_data
    except Exception as e:
        print("broken news", e)
        return None
        
def format_date(date_str):
    year, month, day = date_str.split('-')
    return f"{day}"

def create_weather_card(x, y, date, temp_max, temp_min, bitmap):
    card = displayio.Group()

    image_bitmap = displayio.Bitmap(16, 16, 16)
    image_palette = displayio.Palette(16)

    image_palette[0] = 0x000000
    image_palette[1] = 0x404040
    image_palette[2] = 0x808080
    image_palette[3] = 0xC0C0C0
    image_palette[4] = 0xFFFFFF
    image_palette[5] = 0xFF0000
    image_palette[6] = 0x00FF00
    image_palette[7] = 0x0000FF
    image_palette[8] = 0xFFFF00
    image_palette[9] = 0xFF00FF
    image_palette[10] = 0x4BA3F5
    image_palette[11] = 0x800000
    image_palette[12] = 0x008000
    image_palette[13] = 0x000080
    image_palette[14] = 0x808000
    image_palette[15] = 0x008080

    for y_pos in range(16):
        for x_pos in range(16):
            image_bitmap[x_pos, y_pos] = bitmap[y_pos][x_pos]
    
    image_tile = displayio.TileGrid(image_bitmap, pixel_shader=image_palette, x=x, y=y + 8)
    card.append(image_tile)

    date_label = create_label(format_date(date), 0xFFFFFF, x+3, y+4)
    card.append(date_label)
    
    temp_max_str = f"{round(temp_max)}"
    temp_min_str = f"{round(temp_min)}"

    def draw_number(number_str, start_x, start_y, color):
        x_offset = 0
        for i, char in enumerate(number_str):
            if i > 0 and number_str[i-1] == '1':
                x_offset -= 5
            for row in range(4):
                for col in range(4):
                    if litlnb[char][row][col]:
                        pixel_bitmap = displayio.Bitmap(1, 1, 1)
                        pixel_palette = displayio.Palette(1)
                        pixel_palette[0] = color
                        pixel_tile = displayio.TileGrid(pixel_bitmap, pixel_shader=pixel_palette, x=start_x + x_offset + i * 4 + col, y=start_y + row)
                        card.append(pixel_tile)
            x_offset += 4
    
    draw_number(temp_min_str, x+6, y + 21, 0xFFFFFF)

    draw_number(temp_max_str, x+6, y + 21 +5, 0x4BA3F5)
    
    return card

scroll_offset = 0
news_title = ""
last_scroll_update = time.monotonic()
SCROLL_DELAY = 0.1

def wrap_text(text, max_width):
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        word_width = len(word) * 4
        if current_width + word_width + 4 <= max_width:
            current_line.append(word)
            current_width += word_width + 4
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def draw_scrolling_text():
    global scroll_offset, news_title, current_news_index
    text_group = displayio.Group()

    display_width = 64
    display_height = 32
    middle_y = display_height // 2
    
    if isinstance(news_title, list) and len(news_title) > 0:
        current_title = news_title[current_news_index % len(news_title)]
    else:
        current_title = "No news available :/"
    
    lines = wrap_text(current_title, display_width)

    line_height = 8
    total_height = len(lines) * line_height

    if scroll_offset <= -(total_height + display_height):
        scroll_offset = middle_y
        current_news_index = (current_news_index + 1) % len(news_title)
    
    current_y = middle_y + scroll_offset
    
    for line in lines:
        if current_y > -line_height and current_y < display_height:
            line_width = len(line) * 4
            start_x = (display_width - line_width) // 2
            
            for i, char in enumerate(line.upper()):
                if char in mini_font:
                    for row in range(6):
                        for col in range(4):
                            if mini_font[char][row][col]:
                                pixel_bitmap = displayio.Bitmap(1, 1, 1)
                                pixel_palette = displayio.Palette(1)
                                pixel_palette[0] = 0xFFFFFF
                                pixel_tile = displayio.TileGrid(
                                    pixel_bitmap,
                                    pixel_shader=pixel_palette,
                                    x=start_x + (i * 4) + col,
                                    y=current_y + row
                                )
                                text_group.append(pixel_tile)
        
        current_y += line_height
    
    return text_group

def update_display(screen_index, update_all=True):
    global scroll_offset, news_title, group, current_news_index
    
    if update_all and screen_index % 3 == 2:
        scroll_offset = 16
    
    if update_all:
        clear_group(group)
        
        try:
            realtime_data, forecast_data = get_weather_data()
            news_data = get_news_data()
            
            if realtime_data and forecast_data and news_data:
                current_weather = realtime_data["current_weather"]
                news_title = [article["title"] for article in news_data["articles"]]
                
                screens = [
                    # Main screen (the one with time, temp, wind and weather icon)
                    {
                        "setup": lambda: [
                            create_label(time.strftime("%H:%M", time.localtime()), 0xFF0000, 5, 5),
                            create_label(f"{current_weather['temperature']}°C", 0x4BA3F5, 5, 15),
                            create_label(f"{current_weather['windspeed']}km/h", 0xFFFFFF, 5, 25)
                        ],
                        "color": 0xFF0000,
                        "image": realtime_data["current_weather"]["weather_bitmap"]
                    },
                    # Weather forecast screen
                    {
                        "setup": lambda: [
                            create_weather_card(2, 0, 
                                             forecast_data["daily"]["time"][0],
                                             forecast_data["daily"]["temperature_2m_max"][0],
                                             forecast_data["daily"]["temperature_2m_min"][0],
                                             forecast_data["daily"]["weather_bitmaps"][0]),
                            create_weather_card(23, 0,
                                             forecast_data["daily"]["time"][1],
                                             forecast_data["daily"]["temperature_2m_max"][1],
                                             forecast_data["daily"]["temperature_2m_min"][1],
                                             forecast_data["daily"]["weather_bitmaps"][1]),
                            create_weather_card(44, 0,
                                             forecast_data["daily"]["time"][2],
                                             forecast_data["daily"]["temperature_2m_max"][2],
                                             forecast_data["daily"]["temperature_2m_min"][2],
                                             forecast_data["daily"]["weather_bitmaps"][2])
                        ],
                        "color": 0xFFFFFF,
                        "image": None
                    },
                    # News
                    {
                        "setup": lambda: [draw_scrolling_text()],
                        "color": 0x00FF00,
                        "image": None
                    }
                ]
                
                screen = screens[screen_index % len(screens)]

                if screen["image"]:
                    try:
                        image_bitmap = displayio.Bitmap(16, 16, 16)
                        image_palette = displayio.Palette(16)

                        image_palette[0] = 0x000000
                        image_palette[1] = 0x404040
                        image_palette[2] = 0x808080
                        image_palette[3] = 0xC0C0C0
                        image_palette[4] = 0xFFFFFF
                        image_palette[5] = 0xFF0000
                        image_palette[6] = 0x00FF00
                        image_palette[7] = 0x0000FF
                        image_palette[8] = 0xFFFF00
                        image_palette[9] = 0xFF00FF
                        image_palette[10] = 0x4BA3F5
                        image_palette[11] = 0x800000
                        image_palette[12] = 0x008000
                        image_palette[13] = 0x000080
                        image_palette[14] = 0x808000
                        image_palette[15] = 0x008080

                        for y in range(16):
                            for x in range(16):
                                image_bitmap[x, y] = screen["image"][y][x]

                        image_tile = displayio.TileGrid(
                            image_bitmap,
                            pixel_shader=image_palette,
                            x=42,
                            y=5
                        )
                        group.append(image_tile)
                    except Exception as e:
                        print("broken image", e)
                
                for element in screen["setup"]():
                    group.append(element)

                progress_palette[0] = screen["color"]
                
            else:
                error_label = create_label("Error", 0xFF0000, 5, 5)
                group.append(error_label)
                
        except Exception as e:
            print("couldn't update display", e)
            error_label = create_label("Error", 0xFF0000, 5, 5)
            group.append(error_label)
    
    elif screen_index % 3 == 2:
        for i in range(len(group)):
            if isinstance(group[i], displayio.Group):
                group.pop(i)
                break
        group.append(draw_scrolling_text())

    elapsed_time = time.monotonic() - last_update
    progress = max(1, int((elapsed_time / 5) * 64))
    progress_bar = displayio.Bitmap(progress, 1, 1)
    progress_tile = displayio.TileGrid(progress_bar, pixel_shader=progress_palette, x=0, y=31)
    
    if len(group) >= 1:
        if isinstance(group[-1], displayio.TileGrid):
            group.pop()
    group.append(progress_tile)
    
    display.root_group = group

screen_index = 0
last_update = time.monotonic()
last_weather_update = time.monotonic()
last_news_update = time.monotonic()

# Main loop
while True:
    current_time = time.monotonic()

    if current_time - last_scroll_update > SCROLL_DELAY:
        if screen_index % 3 == 2:
            scroll_offset -= 1
            update_display(screen_index, update_all=False)
        last_scroll_update = current_time

    if current_time - last_update >= 5:
        if screen_index % 3 == 2: 
            if current_time - last_update >= 12:
                screen_index = 0
                display_cycle += 1
                last_update = current_time
                scroll_offset = 16
                update_display(screen_index, update_all=True)
        else:
            screen_index += 1
            if screen_index % 3 == 2:
                current_news_index = display_cycle % 3
            last_update = current_time
            scroll_offset = 0
            update_display(screen_index, update_all=True)

    if current_time - last_weather_update >= 300:
        last_weather_update = current_time
        update_display(screen_index)

    if current_time - last_news_update >= 600:
        last_news_update = current_time
        update_display(screen_index)

    if current_time - last_update >= 5:
        if screen_index % 3 == 2:
            if current_time - last_update >= 12:
                screen_index += 1
                last_update = current_time
                scroll_offset = 0
                update_display(screen_index, update_all=True)
        else:
            screen_index += 1
            last_update = current_time
            scroll_offset = 0
            update_display(screen_index, update_all=True)

    elapsed_time = current_time - last_update
    if screen_index % 3 == 2:
        progress = max(1, int((elapsed_time / 12) * 64))
    else:
        progress = max(1, int((elapsed_time / 5) * 64))

    progress_bar = displayio.Bitmap(progress, 1, 1)
    progress_tile = displayio.TileGrid(progress_bar, pixel_shader=progress_palette, x=0, y=31)
    
    if len(group) >= 3:
        group[-1] = progress_tile
    else:
        group.append(progress_tile)

    display.refresh()
    time.sleep(0.05)
