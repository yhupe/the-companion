import requests
from bs4 import BeautifulSoup

class EventScraper:


    def __init__(self):
        self.event_list = []

    def get_events(self):
        # URL of the webpage to scrape
        url = "https://www.mittelhof.org/angebote/altere-menschen/?q=&zeit=heute"
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()
        except requests.RequestException as e:
            # Print an error message and return an empty list if the request failed
            print(f"Failed to retrieve the webpage. Error: {e}")
            return []

        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all event elements on the page (limit to the first 4)
        events = soup.find_all('li', class_='offer-card')[:4]
        self.event_list = []

        # Iterate over each event element
        for event in events:
            # Extract the event title
            title = event.find('h3').text.strip() if event.find('h3') else 'No title'
            # Extract the date, time, and location information
            offer_date_location = event.find('div', class_='offer-date-location')
            # Extract the event description
            offer_description = event.find('div', class_='richtext-block').text.strip() if event.find('div', class_='richtext-block') else 'No description'

            # Initialize date, time, and location with default values
            date, time, location = 'No date', 'No time', 'No location'
            if offer_date_location:
                # Extract the date and time
                date_div = offer_date_location.find('div', class_='pe-3')
                if date_div:
                    date = date_div.find('div', class_='bold-italic').text.strip() if date_div.find('div', class_='bold-italic') else 'No date'
                    time = date_div.contents[-1].strip() if date_div.contents else 'No time'
                # Extract the location
                location_div = offer_date_location.find('div')
                if location_div:
                    location = location_div.find_next_sibling('div').text.strip() if location_div.find_next_sibling('div') else 'No location'

            # Create a dictionary with the event information
            event_info = {
                "title": title,
                "date": date,
                "time": time,
                "location": location,
                "description": offer_description
            }
            # Add the event information to the list
            self.event_list.append(event_info)


    def display_events(self):
        # Check if there are no events
        if not self.event_list:
            return "Sorry, there are no events for today. Please check back later or tomorrow. Have a nice day."

        # Initialize a string to hold the event information
        event_str = "Here are the events for today:\n"
        for event in self.event_list:
            # Append each event's details to the string
            event_str += "-" * 3 + "\n"
            event_str += f"Event: {event['title']}\n"
            event_str += f"When: {event['date']}\n"
            event_str += f"Time: {event['time']}\n"
            event_str += f"Where: {event['location']}\n"
            event_str += f"Description: {event['description']}\n"
            event_str += "-" * 3 + "\n"

        return event_str

    def main(self):
        # Get the list of events
        self.get_events()
        # Display the events (currently commented out)
        response = self.display_events()
        return response



if __name__ == '__main__':
    ws = EventScraper()
    events = ws.main()
    print(events)
    print(type(events))
