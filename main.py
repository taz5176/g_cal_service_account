import datetime

from g_cal import G_Cal


CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']
CAL_ID = 'c3b3f42148063a80992611545e9799a098ecd1ee0ca3ed478cea36c90a638b9d@group.calendar.google.com'

g_cal = G_Cal(CAL_ID,
              API_SERVICE_NAME,
              API_VERSION,
              SCOPES,
              CLIENT_SECRET_FILE
              )
g_cal.construct_workweek_events(datetime.datetime.now())
events = g_cal.weekly_events
print(events)
