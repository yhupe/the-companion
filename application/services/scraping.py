import requests
from bs4 import BeautifulSoup

def get_events():
    url = "https://www.mittelhof.org/angebote/altere-menschen/?q=&zeit=heute"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage. Error: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    events = soup.find_all('li', class_='offer-card')[:4]
    event_list = []

    for event in events:
        title = event.find('h3').text.strip() if event.find('h3') else 'No title'
        offer_date_location = event.find('div', class_='offer-date-location')
        offer_description = event.find('div', class_='richtext-block').text.strip() if event.find('div', class_='richtext-block') else 'No description'

        date, time, location = 'No date', 'No time', 'No location'
        if offer_date_location:
            date_div = offer_date_location.find('div', class_='pe-3')
            if date_div:
                date = date_div.find('div', class_='bold-italic').text.strip() if date_div.find('div', class_='bold-italic') else 'No date'
                time = date_div.contents[-1].strip() if date_div.contents else 'No time'
            location_div = offer_date_location.find('div')
            if location_div:
                location = location_div.find_next_sibling('div').text.strip() if location_div.find_next_sibling('div') else 'No location'

        event_info = {
            "title": title,
            "date": date,
            "time": time,
            "location": location,
            "description": offer_description
        }
        event_list.append(event_info)
    return event_list


def display_events(events):
    if not events:
        return "Sorry, there are no events for today. Please check back later or tomorrow. Have a nice day."

    event_str = "Here are the events for today:\n"
    for event in events:
        event_str += "-" * 40 + "\n"
        event_str += f"Event: {event['title']}\n"
        event_str += f"When: {event['date']}\n"
        event_str += f"Time: {event['time']}\n"
        event_str += f"Where: {event['location']}\n"
        event_str += f"Description: {event['description']}\n"
        event_str += "-" * 40 + "\n"

    return event_str

def main():
    events = get_events()
    display_events(events)
    #print(display_events(events)) #remove, was just to see that is working
if __name__ == "__main__":
    main()