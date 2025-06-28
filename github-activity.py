import sys, requests

def parse_events(events: list):
    for event in events:
        log: str = ''
        if event['type'] == 'PushEvent':
            log = f'Pushed {len(event['payload']['commits'])} commit(s) to {event['repo']['name']}'
        elif event['type'] == 'IssuesEvent':
            log = f'Opened a new issue in {event['repo']['name']}'
        elif event['type'] == 'WatchEvent':
            log = f'Starred {event['repo']['name']}'
        elif event['type'] == 'ForkEvent':
            log = f'Forked {event['repo']['name']}'
        elif event['type'] == 'CreateEvent':
            log = f'Created {event['payload']['ref_type']} in {event['repo']['name']}'
        else:
            log = f'{event['type'].replace('Event', '')} in {event['repo']['name']}'

        print(f'- {log}')

def make_request(username: str) -> list:
    response = requests.get(f"https://api.github.com/users/{username}/events")

    if not response.ok:
        if response.status_code == 404:
            raise Exception("User not found, please check username")
        else:
            raise Exception(f"Failed fetching data: {response.status_code}")
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) < 2: raise ValueError("No argument passed!")

    events = make_request(sys.argv[1])
    parse_events(events)


