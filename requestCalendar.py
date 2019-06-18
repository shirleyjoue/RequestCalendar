from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


#+++++++++Get datetime++++++++++
today=datetime.date.today().isoformat()

def trans_time(time):
    import pytz, datetime
    local = pytz.timezone ("Japan")
    naive = datetime.datetime.strptime (time, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc).isoformat()[:19]+'.000000Z'
    return utc_dt

class Day(object):
    def __init__(self, today):
        self.today = today
    
    def get_startime(self):
        self.time = self.today+' 07:00:00'
        return self.time
    
    def get_endtime(self):
        time = self.today+' 19:00:00'
        return time



def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('time,events')
    events_result = service.events().list(calendarId='primary', timeMin=trans_time(Day(today).get_startime()),
                                        timeMax=trans_time(Day(today).get_endtime()), singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))[11:16]
        end = event['end'].get('dateTime', event['end'].get('date'))[11:16]

        print(start+'-'+end+','+event['summary'])

if __name__ == '__main__':
    main()
