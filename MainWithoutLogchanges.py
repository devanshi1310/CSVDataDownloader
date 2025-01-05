from playwright.sync_api import Playwright, sync_playwright
import logging
import os
import time
from datetime import datetime
import pandas as pd

# Generate a timestamp for the log file
log_filename = f"progress_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log"

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


def search_in_page(playwright: Playwright, url: str, search_bar_selector: str, search_text: str, str_select_option: str, str_select_max: str, str_select_download: str, strDownloadPath: str) -> None:
    log_message("Launching browser")
    browser = playwright.chromium.launch(headless=False)
    log_message("Browser launched")

    log_message("Creating a new browser context")
    context = browser.new_context()
    log_message("Browser context created")

    log_message("Opening a new page")
    page = context.new_page()
    log_message("New page opened")

    log_message(f"Navigating to URL: {url}")
    page.goto(url, timeout=100000,wait_until="domcontentloaded")
    log_message("Page loaded")

    log_message(f"Clicking on the search bar: {search_bar_selector}")
    page.click(search_bar_selector)
    log_message("Search bar clicked")

    log_message(f"Typing text into the search bar: {search_text}")
    page.fill(search_bar_selector, search_text)
    log_message("Text typed into the search bar")

    # Verify if the text was typed correctly
    typed_text = page.input_value(search_bar_selector)
    if typed_text == search_text:
        log_message("Verification successful: Text correctly typed in the search bar")
    else:
        log_message(f"Verification failed: Expected '{search_text}', but found '{typed_text}'")

    # Optionally, press Enter to search
    log_message("Pressing Enter to search")
    page.press(search_bar_selector, 'Enter')
    log_message("Enter key pressed")

    log_message(f"Clicking on Searched Option: {str_select_option}")
    page.click(str_select_option)
    log_message("Option to select clicked")

    log_message(f"Clicking on Max Option: {str_select_max}")
    page.click(str_select_max)
    log_message("Max clicked")

    log_message(f"Clicking on Download Option: {str_select_download}")

    with page.expect_download() as download_info:
        page.click(str_select_download)
        download = download_info.value

    log_message("Download clicked")

    # Save the downloaded file with timestamp in the file name
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    download_path = os.path.join(strDownloadPath, "Downloads", search_text, f'{search_text}_{timestamp}.csv')
    download.save_as(download_path)
    log_message(f"Successfully downloaded data for {search_text} to {download_path}")

    # Format the CSV and add Symbol column
    format_csv_columns(download_path, search_text)

    # Close the browser
    log_message("Closing the browser")
    browser.close()
    log_message("Browser closed")

def run(SearchTerm):
    with sync_playwright() as playwright:
        search_in_page(
            playwright,
            'https://www.nasdaq.com/market-activity/quotes/historical',
            '#find-symbol-input-dark',
            SearchTerm,
            '#resultsDark > a:nth-child(1)',
            'body > div.dialog-off-canvas-main-canvas > div > main > div.page__content > article > div > div.nsdq-bento-layout__main.nsdq-c-band.nsdq-c-band--white.nsdq-u-padding-top-sm2.nsdq-u-padding-bottom-sm2.nsdq-c-band__overflow_hidden > div > div.nsdq-bento-ma-layout__qd-center.nsdq-sticky-container > div.ma-qd-symbol-info > div.layout__region.ma-qd-breadcrumb > div:nth-child(3) > div > div.historical-data-container > div.historical-controls > div.historical-tabs > div > button:nth-child(6)',
            'body > div.dialog-off-canvas-main-canvas > div > main > div.page__content > article > div > div.nsdq-bento-layout__main.nsdq-c-band.nsdq-c-band--white.nsdq-u-padding-top-sm2.nsdq-u-padding-bottom-sm2.nsdq-c-band__overflow_hidden > div > div.nsdq-bento-ma-layout__qd-center.nsdq-sticky-container > div.ma-qd-symbol-info > div.layout__region.ma-qd-breadcrumb > div:nth-child(3) > div > div.historical-data-container > div.historical-controls > div.historical-download-container > button',
            r'D:\Devanshi\Self study\USStockDownloder')

if __name__ == '__main__':
    ls = ['AMD','TSLA', 'META', 'AAPL', 'MSFT']
    #['TSLA', 'META', 'AAPL', 'MSFT']
    for i in range(len(ls)):
        run(ls[i])
