# project/main.py
from utils.util_selenium import setup_logger, obtain_soup, get_soup, save_soup
from utils.util import to_sqlite3, dataframe, read_the_csv, data_cleaning, view

logger = setup_logger()
logger.info("The logger has started. . . ")

results = []

url = "https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaLQCiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBqAIDuAKCtO2sBsACAdICJGQ5YzRkMjZkLWY0Y2YtNDNhNC05MDkxLTVmY2E5NmU3OWU2MNgCBeACAQ&sid=1b32a53bf9957e29791ed0e41915c5bb&checkin_monthday=29&checkin_year_month=2024-01&checkout_monthday=31&checkout_year_month=2024-01&dest_id=20144123&dest_type=city&from_history=1&group_adults=2&no_rooms=1&order=popularity&sb_travel_purpose=leisure&si=ad&si=ai&si=ci&si=co&si=di&si=la&si=re&sh_position=1&auth_success=1"

url2 = "https://www.booking.com/searchresults.html?label=gen173rf-1FCAEoggI46AdIM1gDaLQCiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBogIKbWVkaXVtLmNvbagCA7gCqK32rAbAAgHSAiQ2NjllOWE5Mi03MWUxLTRhZmYtODk3YS1jZDc5YjE2MDY0NDbYAgXgAgE&aid=304142&ss=Leavenworth&ssne=Leavenworth&ssne_untouched=Leavenworth&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=20144123&dest_type=city&checkin=2024-01-29&checkout=2024-01-30&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset=0"
urls = [url, url2]
for index, url in enumerate(urls):
    if index == 0:
        filename = "data/html_for_soup.txt"
    if index == 1:
        filename = 'data/html_for_soup2.txt'
    soup = obtain_soup(url, filename)
    # save_soup(soup, filename)

    items = soup.find_all("div", {"data-testid": 'property-card'})
    logger.info(f"The index is {index}.")


    for item in items:
        try:
            rating = item.find('div', {'data-testid': 'review-score'}).find('div').text
            logger.info(f'the rating is {rating}.')
        except AttributeError:
            rating = '0.0'

        try: 
            temp = item.find('div', class_='abf093bdfe f45d8e4c32 d935416c47').text.split()[0].replace(',', '')
            reviews = temp

        except AttributeError:
            reviews = '0'

        result = {
        'title': item.find('div', {'data-testid': 'title'}).text,
        'address': item.find('span', {'data-testid': 'address'}).text.strip(),
        'description': item.find('h4', {'role': 'link'}).text,
        'rating': rating,
        'price': item.find('span', {'data-testid': "price-and-discounted-price"}).text[1:].strip().replace(',', ''),
        '#reviews': reviews,
        }
        logger.info(f"result is: {result}")
        results.append(result)



df = dataframe(results)

logger.info(f"The length of df is {len(df)}")

df = data_cleaning(df)
print(df.info())

to_sqlite3(df)
print(view())
