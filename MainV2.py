import os
import logging
from datetime import datetime
import pandas as pd
from playwright.sync_api import Playwright, sync_playwright
import time

# Dynamically set the download path based on the script location
script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script
strDownloadPath = script_dir  # Set download path to the script's directory

# Create the "Logs" directory inside the download path if it doesn't exist
logs_dir = os.path.join(strDownloadPath, "Logs")
os.makedirs(logs_dir, exist_ok=True)

# Generate a timestamp for the log file
log_filename = os.path.join(logs_dir, f"progress_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log")

# Configure logging to include a timestamp in the log filename
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y_%H-%M-%S')

def log_message(message: str) -> None:
    logging.info(message)
    print(message)

def format_csv_columns(file_path: str, symbol: str) -> None:
    """Format the columns in the CSV: ensure proper order, format date, remove dollar symbols, add 'Symbol' column, and save without header."""
    try:
        # Load the CSV into a DataFrame
        df = pd.read_csv(file_path)
        
        # Remove dollar symbols and convert columns to float with 2 decimal places
        for col in ['Close/Last', 'Open', 'High', 'Low']:
            if col in df.columns:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float).round(2)
        
        # Ensure the 'Date' column is in YYYYMMDD format
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y%m%d')
        
        # Add a new column 'Symbol' with the value of the search term
        df['Symbol'] = symbol
        
        # Rearrange columns
        desired_order = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close/Last', 'Volume']
        df = df.reindex(columns=desired_order, fill_value=None)
        
        # Rename 'Close/Last' to 'Close' for consistency
        df.rename(columns={'Close/Last': 'Close'}, inplace=True)
        
        # Save the DataFrame to the CSV without headers
        df.to_csv(file_path, index=False, header=False)
        log_message(f"CSV formatted, headers removed, and saved at {file_path}")
    except Exception as e:
        log_message(f"Error formatting CSV: {e}")


def search_in_page(playwright: Playwright, symbol: str, str_select_max: str, str_select_download: str, str_download_path: str) -> None:
    log_message(f"Launching browser for symbol: {symbol}")
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    url = f"https://www.nasdaq.com/market-activity/stocks/{symbol.lower()}/historical"
    log_message(f"Navigating to {url}")
    page.goto(url, timeout=100000, wait_until="domcontentloaded")

    log_message("Clicking on Max Option to view all data")
    page.click(str_select_max)
    log_message("Max clicked")

    log_message("Clicking on Download Option")

    with page.expect_download() as download_info:
        page.click(str_select_download)
        download = download_info.value

    log_message("Download started")

    # Save downloaded file with timestamp and symbol
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{symbol}_{timestamp}.csv"
    download_path = os.path.join(str_download_path, "Downloads", filename)
    download.save_as(download_path)
    log_message(f"Downloaded CSV for {symbol} saved to {download_path}")

    # Format the CSV
    format_csv_columns(download_path, symbol)

    browser.close()
    log_message(f"Browser closed for {symbol}")

def run(symbol: str):
    with sync_playwright() as playwright:
        search_in_page(
            playwright,
            symbol,
            'body > div.dialog-off-canvas-main-canvas > div > main > div.page__content > article > div > div.nsdq-bento-layout__main.nsdq-c-band.nsdq-c-band--white.nsdq-u-padding-top-sm2.nsdq-u-padding-bottom-sm2.nsdq-c-band__overflow_hidden > div > div.nsdq-bento-ma-layout__qd-center.nsdq-sticky-container > div.ma-qd-symbol-info > div.layout__region.ma-qd-breadcrumb > div:nth-child(3) > div > div.historical-data-container > div.historical-controls > div.historical-tabs > div > button:nth-child(6)',
            'body > div.dialog-off-canvas-main-canvas > div > main > div.page__content > article > div > div.nsdq-bento-layout__main.nsdq-c-band.nsdq-c-band--white.nsdq-u-padding-top-sm2.nsdq-u-padding-bottom-sm2.nsdq-c-band__overflow_hidden > div > div.nsdq-bento-ma-layout__qd-center.nsdq-sticky-container > div.ma-qd-symbol-info > div.layout__region.ma-qd-breadcrumb > div:nth-child(3) > div > div.historical-data-container > div.historical-controls > div.historical-download-container > button',
            strDownloadPath
        )

if __name__ == '__main__':
    symbols = ['AMD', 'META', 'AAPL', 'MSFT']
    for symbol in symbols:
        run(symbol)