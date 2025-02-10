import re
import time
import csv
from pathlib import Path
from typing import Any, Tuple

from soxm.Paths import Paths
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup

# Set the default sleep time (in seconds) used throughout the script.
sleep_time_sec = 3

# Output location: data/raw/meysam2020_original/tweets/
target_dir = Paths.data() / 'raw/meysam2020_original/tweets'
tweets_csv = target_dir / 'tweets.csv'   # for successfully scraped tweets: ['xhandle', 'xpostid', 'xposttext']
errors_csv = target_dir / 'errors.csv'   # for tweets that could not be scraped (header: 'xpostid')

# List of tweet IDs to scrape. # TODO: read these in from the meysam2020 dataset
tweet_ids = [
    '421303671155355648',
    '960292027241041920',
    '1039222190686789632',
    '903460559651315712',
    '843183003551645696',
    '919348117853687808',
]

class xScraper:
    def __init__(self, 
                 xuser: str, 
                 xpassword: str, 
                 sleep_time_sec: int = 3,
                 headless: bool = False,
                 tweet_any_url: str = 'https://x.com/anyuser/status/{}',
                 tweet_user_url: str = 'https://x.com/{}/status/{}'):
        self.xuser = xuser
        self.xpassword = xpassword
        self.tweet_any_url = tweet_any_url
        self.tweet_user_url = tweet_user_url
        self.sleep_time_sec = sleep_time_sec
        self.headless = headless
        self.driver = None

    def __enter__(self):
        # Create a Firefox session.
        try:
            firefox_options = FirefoxOptions()
            if self.headless:
                firefox_options.add_argument("--headless")
            service = FirefoxService()  # Assumes geckodriver is in PATH.
            self.driver = webdriver.Firefox(service=service, options=firefox_options)
        except WebDriverException as e:
            raise ConnectionError("Could not start Selenium session with Firefox.") from e

        # Begin login procedure.
        try:
            # Open the login page.
            self.driver.get("https://x.com/login")
            time.sleep(self.sleep_time_sec)

            # --- Step 1: Enter username ---
            username_field = self.driver.find_element("name", "text")
            username_field.clear()
            username_field.send_keys(self.xuser)
            time.sleep(self.sleep_time_sec)
            # Click the "Next" button.
            next_button = self.driver.find_element("xpath", "//button[div//span[text()='Next']]")
            next_button.click()
            time.sleep(self.sleep_time_sec)

            # --- Step 2: Enter password ---
            password_field = self.driver.find_element("name", "password")
            password_field.clear()
            password_field.send_keys(self.xpassword)
            time.sleep(self.sleep_time_sec)
            # Click the login button.
            login_button = self.driver.find_element("xpath", "//button[@data-testid='LoginForm_Login_Button' and .//span[text()='Log in']]")
            login_button.click()
            time.sleep(self.sleep_time_sec)
        except Exception as e:
            self.driver.quit()
            raise ConnectionError("Failed to log in with provided credentials.") from e

        return self

    def get_post(self, tweet_id: str) -> Tuple[str, str, str]:
        """
        Given a tweet_id, load the tweet page and return a tuple:
          (xhandle, tweet_id, tweet_text)
        xhandle is extracted from the redirected URL.
        tweet_text is scraped using BeautifulSoup.
        """
        try:
            url = self.tweet_any_url.format(tweet_id)
            self.driver.get(url)
            time.sleep(self.sleep_time_sec)
        except Exception as e:
            raise ConnectionError("Error accessing URL: " + url) from e

        current_url = self.driver.current_url
        m = re.search(r"https://x\.com/([^/]+)/status/", current_url)
        if m:
            xhandle = m.group(1)
        else:
            raise FileNotFoundError("Unable to extract xhandle from URL: " + current_url)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        tweet_div = soup.find("div", {"data-testid": "tweetText"})
        if tweet_div:
            xpost = tweet_div.get_text(separator=" ", strip=True)
        else:
            raise FileNotFoundError("Tweet text not found for tweet id " + tweet_id)

        return xhandle, tweet_id, xpost

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver is not None:
            self.driver.quit()

def main():
    # Load credentials from .env.
    config = dotenv_values(Paths.project() / ".env")
    xuser = config['XUSER']
    xpassword = config['XPASSWORD']

    # Ensure target directory exists.
    target_dir.mkdir(parents=True, exist_ok=True)

    # Always create new CSV files for tweets and errors.
    with tweets_csv.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # Wrap each value in double quotes.
        writer.writerow(['xhandle', 'xpostid', 'xposttext'])
    with errors_csv.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['xpostid'])

    # Open tweets.csv in append mode.
    with tweets_csv.open('a', newline='', encoding='utf-8') as tweets_out:
        tweets_writer = csv.writer(tweets_out, quoting=csv.QUOTE_ALL)
        # Open errors.csv in append mode.
        with errors_csv.open('a', newline='', encoding='utf-8') as errors_out:
            errors_writer = csv.writer(errors_out, quoting=csv.QUOTE_ALL)
            # Use xScraper with the provided credentials.
            with xScraper(xuser, xpassword, sleep_time_sec=sleep_time_sec, headless=False) as scraper:
                for tweet_id in tweet_ids:
                    tweet_id = tweet_id.strip()  # In case of extra spaces.
                    print("Processing tweet id:", tweet_id)
                    try:
                        xhandle, xpostid, xposttext = scraper.get_post(tweet_id)
                        tweets_writer.writerow([xhandle, xpostid, xposttext])
                        print(f"Successfully scraped tweet by {xhandle}.")
                    except Exception as e:
                        print(f"Error processing tweet {tweet_id}: {e}")
                        errors_writer.writerow([tweet_id])

if __name__ == '__main__':
    main()
    