from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from app.models import BinType
from utils import setup_driver, parse_date
    

def get_collections(collection_url: str) -> list[dict]:
    """ 
    Scrapes the Wakefield Council website for bin collection dates
    
    :param collection_url: The URL to scrape
        -> example (Town Hall): https://www.wakefield.gov.uk/where-i-live/?uprn=63156908&a=Town%20Hall%20Wood%20Street%20Wakefield%20WF1%202HQ&usrn=41804559&e=433018&n=420931&p=WF1%202HQ
    :return: A list of dictionaries containing the bin type and collection dates
    """
    driver = setup_driver()
    
    driver.get(collection_url)
    assert "Where" in driver.title
    
    bin_collections = driver.find_element(By.CSS_SELECTOR, "div.c-content-section_body")
    collections_by_type = bin_collections.find_elements(By.CSS_SELECTOR, "div.u-mb-8")
    
    collections: list[dict] = []
    
    for section in collections_by_type:
        try:
            collection_dates_link = section.find_element(By.CSS_SELECTOR, "a.futurecolldates")
        except NoSuchElementException:
            continue
        
        bin_type = section.find_element(By.CSS_SELECTOR, "div.u-mb-4").text
        
        if bin_type == "Household waste":
            bin_type = BinType.HOUSEHOLD_WASTE
        elif bin_type == "Mixed recycling":
            bin_type = BinType.RECYCLING
        elif bin_type == "Garden waste recycling":
            bin_type = BinType.GARDEN_WASTE
        else:
            raise ValueError(f"Unknown bin type: {bin_type}")
        
        parsed_collection_dates: list[str] = []
        
        # ------- Get the last collection date -------
        last_and_next_collections = section.find_elements(By.CSS_SELECTOR, "div.u-mb-2")
        next_collection = last_and_next_collections[1]
        
        _, next_collection_date = next_collection.text.split(" - ")
        _, next_collection_date = next_collection_date.strip().split(", ")
        parsed_collection_dates.append(parse_date(next_collection_date))        
        
        # ------- Get the future collection dates -------
        # Using JS to click the link as the element is not clickable
        driver.execute_script("arguments[0].click();", collection_dates_link)
        collection_dates = section.find_element(By.CSS_SELECTOR, "div.colldates")
        
        collection_list = collection_dates.find_element(By.CSS_SELECTOR, "ul.u-mt-4") 
        
        for collection in collection_list.find_elements(By.TAG_NAME, "li"):
            # The date is in the format "Day, DD Month YYYY"
            _, date = collection.text.split(", ")           
            parsed_date = parse_date(date)
            
            # For some reason, the same date is repeated twice BUT only with household waste?
            if parsed_date not in parsed_collection_dates:
                parsed_collection_dates.append(parsed_date)
            else:
                continue
            
        collections.append({
            "bin_type": bin_type,
            "collection_dates": parsed_collection_dates
        })        
    
    return collections


def get_addresses(postcode: str) -> list[str]:
    """ 
    Scrapes the Wakefield Council website for addresses at a given postcode
    
    :param postcode: The postcode to search for
    :return: A list of addresses at the given postcode 
    """
    driver = setup_driver()
    
    driver.get("https://www.wakefield.gov.uk/where-i-live/")
    assert "Where" in driver.title
    
    elem = driver.find_element(By.ID, "where-i-live")
    elem.clear()
    elem.send_keys(postcode)
    elem.send_keys(Keys.RETURN)
    assert "Pick" in driver.title

    address_list = driver.find_elements(By.CSS_SELECTOR, "div.u-mb-6")
    if len(address_list) == 0:
        driver.quit()
        return []

    addresses = []
    for address in address_list:
        ul = address.find_element(By.TAG_NAME, "ul")
        li = ul.find_elements(By.TAG_NAME, "li")
        a = li[0].find_element(By.TAG_NAME, "a")
        
        addresses.append({
            "address": a.text,
            "url": f"https://www.wakefield.gov.uk{a.get_attribute('href')}"
        })
        

    driver.quit()
    return addresses