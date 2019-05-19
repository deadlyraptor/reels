from dataclasses import dataclass
from datetime import date, timedelta
from typing import List
import dateutil.parser
import requests


@dataclass
class AgileEvent():
    """A class used to represent film events.

    Parameters
    ----------
    name: str
        The name of the event.
    showtimes : list
        A collection of instances of showtimes as datetime objects.

    """

    name: str
    showtimes: List

    def build_agile_payload(start_date, end_date):
        """Build the parameters for the WebSales URL requesst.

        Parameters
        ---------
        date : str
            The date for which to pull showtimes.

        Returns
        -------
        payload
            The parameters to send in the URL's query string as a dictionary.

        """
        payload = {'guid': '6ec0e98b-d23e-4240-acce-5ffa059e6887',
                   'showslist': 'true', 'format': 'json',
                   'startdate': start_date.strftime('%Y-%m-%d'),
                   'enddate': end_date.strftime('%Y-%m-%d')}

        return payload

    def from_agile_dict(event):
        """Instantiate both AgileEvent and AgileSchedule.

        The class parameters are pulled from a dictionary provided by the
        Agile WebSales Feed (JSON format).

        Parameters
        ----------
        event
            A dictionary (JSON) containing the info for an event in the Agile
            WebSales Feed.

            It includes a subdictionary called CurrentShowings that contains
            the showtimes for the event.

        Returns
        -------
        AgileEvent
            Instance of class AgileEvent.

        """
        name = event['Name']
        showtimes = []
        for showing in event['CurrentShowings']:
            showtime = dateutil.parser.parse(showing['StartDate'])
            showtimes.append(showtime)

        return AgileEvent(name, showtimes)

    def fetch_agile_events(payload):
        """Make a request to the Agile WebSales Feed and build a list of films.

        Parameters
        ----------
        payload : dict
            The parameters to send in the URL's query string as a dictionary.

        Returns
        -------
        films
            A list populated by instances of AgileEvent.

            The list is sorted by the showtimes otherwise they would be listed
            alphabetically.

        """
        base_agile_url = 'https://prod3.agileticketing.net/websales/feed.ashx?'
        response = requests.get(base_agile_url, params=payload)
        feed = response.json()
        films = []
        # the feed returns a truncated dictionary if the venue has no events so
        # this conditional statement checks that the required data exists
        if len(feed) == 3:
            pass
        else:
            events = feed['ArrayOfShows']
            for event in events:
                film = AgileEvent.from_agile_dict(event)
                films.append(film)

        films.sort(key=lambda film: film.showtimes)

        return films


def print_script():
    """Print the data collected in the script to the terminal."""
    period = input('Select (1) for weekend dates or (2) for weekdays: ')

    start_date = date.today()

    if period.lower() == '1':
        end_date = start_date + timedelta(days=3)
        period = 'weekend'
    elif period.lower() == '2':
        end_date = start_date + timedelta(days=4)
        period = 'weekdays'

    payload = AgileEvent.build_agile_payload(start_date, end_date)
    films = AgileEvent.fetch_agile_events(payload)

    script = (
              f'\n'
              f'Thank you for calling the Coral Gables Art Cinema.\n'
              f'\n'
              f'For movie showtimes, please stay on the line. Our office is '
              f'open Monday to Friday from 9:00 am to 5:00 pm and can be '
              f'reached at 786.472.2249.\n'
              f'\n'
              f'Showtimes for the {period} are:\n'
             )

    print(script)

    for film in films:
        print(film.name)
        for showtime in film.showtimes:
            print(f'{showtime.strftime("%A, %-m/%-d")}: '
                  f'{showtime.strftime("%-I:%M%p").lower()}')

    input('Press enter to exit: ')  # keeps window open


print_script()
