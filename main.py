import pygame
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

pygame.init()

# Screen setup
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("📈 Stock Price Prediction Tool")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 120, 215)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 100, 0)

# Fonts
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 36, bold=True)

# Input box and button
input_box = pygame.Rect(280, 80, 300, 40)
button_rect = pygame.Rect(600, 80, 120, 40)
input_text = ''
active = False
message = ''

# Data and scroll
results = []  # list of (ticker, mse, chart_path)
scroll_y = 0
MAX_SCROLL = 10000

# Function to fetch data and predict
def fetch_and_predict(symbols_input):
    tickers = [t.strip().upper() for t in symbols_input.split(',') if t.strip()]
    result_data = []

    for ticker in tickers:
        try:
            data = yf.download(ticker, start="2020-01-01", end="2024-12-31", auto_adjust=True)
            if data.empty:
                continue

            df = data.reset_index()
            df['Day'] = np.arange(len(df))
            X = df[['Day']]
            y = df['Close']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)

            mse = mean_squared_error(y_test, predictions)
            chart_path = f"{ticker}_chart.png"

            # Save chart
            plt.figure(figsize=(8, 4))
            plt.scatter(X_test, y_test, color='red', label='Actual Price')
            plt.plot(X_test, predictions, color='blue', label='Predicted Price')
            # plt.xlabel("Day Index")
            # plt.ylabel("Stock Price ($)")
            # plt.title(f"{ticker} Price Prediction")
            # plt.legend()
            # plt.grid(True)
            # plt.tight_layout()
            # plt.savefig(chart_path)
            # plt.close()

            result_data.append((ticker, mse, chart_path))
        except Exception as e:
            print(f"Error for {ticker}: {e}")
            continue

    return result_data

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Title and message (scrollable)
    title_surface = title_font.render("Stock Price Prediction Model", True, BLACK)
    screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 20 - scroll_y))

    label_surface = font.render("Enter Stock Symbols:", True, BLACK)
    screen.blit(label_surface, (80, 90 - scroll_y))

    msg_surface = font.render(message, True, BLACK)
    screen.blit(msg_surface, (100, 140 - scroll_y))

    # Input box (fixed)
    pygame.draw.rect(screen, BLUE if active else GRAY, input_box, 2)
    txt_surface = font.render(input_text, True, BLACK)
    screen.blit(txt_surface, (input_box.x + 10, input_box.y + 5))

    # Button (fixed)
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, LIGHT_BLUE if button_rect.collidepoint(mouse_pos) else DARK_GRAY, button_rect)
    button_text = font.render("Predict", True, BLACK)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    # Display charts (scrollable)
    y_offset = 180
    for ticker, mse, chart_path in results:
        if y_offset - scroll_y > screen.get_height():
            break  # Stop drawing off-screen

        try:
            chart_img = pygame.image.load(chart_path)
            chart_img = pygame.transform.scale(chart_img, (700, 300))
            screen.blit(chart_img, (100, y_offset - scroll_y))

            mse_text = font.render(f"{ticker}: MSE = {mse:.2f}", True, GREEN)
            screen.blit(mse_text, (100, y_offset + 310 - scroll_y))

            y_offset += 360
        except Exception as e:
            error_msg = font.render(f"Error loading chart for {ticker}", True, (255, 0, 0))
            screen.blit(error_msg, (100, y_offset - scroll_y))
            y_offset += 50

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False

            if button_rect.collidepoint(event.pos):
                symbols = input_text.upper().strip()
                if symbols == '':
                    message = "Please enter at least one stock symbol!"
                    results = []
                else:
                    message = "Fetching predictions..."
                    pygame.display.flip()
                    results = fetch_and_predict(symbols)
                    if results:
                        message = f"Loaded {len(results)} predictions."
                    else:
                        message = "No valid predictions found."

        elif event.type == pygame.MOUSEWHEEL:
            scroll_y -= event.y * 30
            scroll_y = max(0, min(scroll_y, MAX_SCROLL))

        elif event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode.upper()

    pygame.display.flip()

pygame.quit()
