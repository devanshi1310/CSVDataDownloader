from playwright.sync_api import Playwright, sync_playwright
import logging

# Configure logging
logging.basicConfig(filename='progress.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(message: str) -> None:
    logging.info(message)
    print(message)

def search_in_page(playwright: Playwright, url: str, search_bar_selector: str, search_text: str,str_Select_Option: str,str_Select_Max :str,str_Select_download:str) -> None:
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
    page.goto(url,timeout=100000)
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

    log_message(f"Clicking on Searched Option: {str_Select_Option}")
    page.click(str_Select_Option)
    log_message("Option to select clicked")

    # log_message("Closing the browser")
    # browser.close()
    # log_message("Browser closed")

    log_message(f"Clicking on Searched Option: {str_Select_Max}")
    page.click(str_Select_Max)
    log_message("Max clicked")

    log_message(f"Clicking on Searched Option: {str_Select_download}")
    page.click(str_Select_download)
    log_message("Download clicked")

    log_message(f"Sucessfully Downloaded Data For {search_text}")

def run(SearchTerm):
    with sync_playwright() as playwright:
        search_in_page(playwright,
         'https://www.nasdaq.com/market-activity/quotes/historical', '#find-symbol-input-dark',SearchTerm,'#resultsDark > a:nth-child(1)','body > div.dialog-off-canvas-main-canvas > div > main > div.page__content > article > div > div.nsdq-bento-layout__main.nsdq-c-band.nsdq-c-band--white.nsdq-u-padding-top-sm2.nsdq-u-padding-bottom-sm2.nsdq-c-band__overflow_hidden > div > div.nsdq-bento-ma-layout__qd-center.nsdq-sticky-container > div.ma-qd-symbol-info > div.layout__region.ma-qd-breadcrumb > div:nth-child(3) > div > div.historical-data-container > div.historical-controls > div.historical-tabs > div > button:nth-child(6)','body > div.dialog-off-canvas-main-canvas > div > main > div.page__content > article > div > div.nsdq-bento-layout__main.nsdq-c-band.nsdq-c-band--white.nsdq-u-padding-top-sm2.nsdq-u-padding-bottom-sm2.nsdq-c-band__overflow_hidden > div > div.nsdq-bento-ma-layout__qd-center.nsdq-sticky-container > div.ma-qd-symbol-info > div.layout__region.ma-qd-breadcrumb > div:nth-child(3) > div > div.historical-data-container > div.historical-controls > div.historical-download-container > button')

if __name__ == '__main__':
    ls = ['AMD','TSLA','META','AAPL','MSFT']
    for i in range(len(ls)):
        run(ls[i])

# from playwright.sync_api import Playwright, sync_playwright

# def search_in_page(playwright: Playwright, url: str, search_bar_selector: str, search_text: str) -> None:
#     # Launch a browser (Chromium, Firefox, or Webkit)
#     browser = playwright.chromium.launch(headless=False)
#     # Create a new browser context
#     context = browser.new_context()
#     # Open a new page
#     page = context.new_page()
#     # Navigate to the specified URL
#     page.goto(url)
#     # Wait for the page to load completely
#     # page.wait_for_load_state('load',timeout=5000000)
#     page.click('#onetrust-accept-btn-handler')
#     print("AcceptCookie")
#     # Click on the search bar
#     page.click(search_bar_selector,timeout=5000000)
#     # Type text into the search bar
#     page.fill(search_bar_selector, search_text)
#     # Optionally, press Enter to search
#     page.press(search_bar_selector, 'Enter')
#     # Close the browser
#     # browser.close()

# def run():
#     with sync_playwright() as playwright:
#         search_in_page(playwright, 'https://www.nasdaq.com/market-activity/quotes/historical', '#find-symbol-input-dark', 'AAPL')

# if __name__ == '__main__':
#     run()
