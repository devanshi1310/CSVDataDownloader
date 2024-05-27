from playwright.sync_api import Playwright, sync_playwright
import logging
import os
import time

# Configure logging
logging.basicConfig(filename='progress.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(message: str) -> None:
    logging.info(message)
    print(message)

def search_in_page(playwright: Playwright, url: str, search_bar_selector: str, search_text: str, str_select_option: str, str_select_max: str, str_select_download: str,strDownloadPath: str) -> None:
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
    page.goto(url, timeout=100000)
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

    # Wait for the new page to load
    time.sleep(5)  # Adjust the sleep time as needed

    log_message(f"Clicking on Max Option: {str_select_max}")
    page.click(str_select_max)
    log_message("Max clicked")

    # Wait for the option to be processed
    time.sleep(5)  # Adjust the sleep time as needed

    log_message(f"Clicking on Download Option: {str_select_download}")

    with page.expect_download() as download_info:
        page.click(str_select_download)
        download = download_info.value

    log_message("Download clicked")

    # Save the downloaded file
    download_path = download.path()
    strDownloadPath = os.path.join(strDownloadPath, "Downloads" ,search_text,f'{search_text}.csv')
    download.save_as(strDownloadPath)
    log_message(f"Successfully downloaded data for {search_text} to {download_path}")

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
            'body > div.dialog-off-canvas-main-canvas > div > main > div.page__content > article > div > div.nsdq-bento-layout__main.nsdq-c-band.nsdq-c-band--white.nsdq-u-padding-top-sm2.nsdq-u-padding-bottom-sm2.nsdq-c-band__overflow_hidden > div > div.nsdq-bento-ma-layout__qd-center.nsdq-sticky-container > div.ma-qd-symbol-info > div.layout__region.ma-qd-breadcrumb > div:nth-child(3) > div > div.historical-data-container > div.historical-controls > div.historical-download-container > button',r'D:\Devanshi\Self study\USStockDownloder')

if __name__ == '__main__':
    ls = ['AMD','TSLA','META','AAPL','MSFT']
    for i in range(len(ls)):
        run(ls[i])
