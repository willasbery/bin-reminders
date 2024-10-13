from datetime import datetime
from selenium import webdriver

def setup_driver() -> webdriver.Chrome:
    """ Helper function to setup the Chrome driver """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=options)

def parse_date(date: str) -> datetime:
    """ Helper function to parse the date from the website """
    date = date.strip()
    try:
        date_object = datetime.strptime(date, "%d %B %Y")
    except ValueError:
        raise ValueError(f"Unknown date format: {date}")
    
    return date_object.strftime('%d/%m/%Y')