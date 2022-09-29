import common, constants
from g_service import G_Service


class G_Cal(G_Service):
    """
    Inherit Google service for getting google calendar events

    Args:
        G_Service (obj): google service to access google api
    """    
    def __init__(self,
                 cal_id, 
                 api_service_name,
                 api_version,
                 scopes,
                 client_secret_file
                 ):
        """
        Initialisation of google calendar obj

        Args:
            cal_id (str): google calendar id
            api_service_name (str): google api service name
            api_version (str): google api version
            scopes (list): google api access
            client_secret_file (str): filename for token
                secret file
        """
        self.cal_id = cal_id
        self.weekly_events = {}
        super().__init__(api_service_name,
                         api_version,
                         scopes,
                         client_secret_file
                         )
        
        
    def get_all_calendar_events(self):
        """
        To get all calendar events

        Returns:
            dict: calendar events
        """
        self.events = self.service.events().list(calendarId=self.cal_id).execute()


    def get_workweek_calendar_events_from_google(self, dt):
        """
        To get all google calendar events in work week of the datetime

        Args:
            dt (obj): datetime obj

        Returns:
            list: google calendar events in the work week 
        """
        week_events = list()
        start_date, end_date = common.get_workweek_dates(dt)
        page_token = None
        
        while True:
            _events = self.service.events().list(
                calendarId=self.cal_id, 
                timeMin=start_date.strftime(constants.REG_EXP.DATE_STRING_FORMAT)+'T00:00:00+08:00', 
                timeMax=end_date.strftime(constants.REG_EXP.DATE_STRING_FORMAT)+'T23:59:59+08:00', 
                pageToken=page_token
                ).execute()
            for event in _events['items']:
                week_events.append(event)
            page_token = _events.get('nextPageToken')
            if not page_token:
                break
        return week_events


    def construct_event(self, day, _event):
        """
        To construct a single event and append to weekly events dict

        Args:
            day (str): day of the week, eg. Mon, Tue etc
            google_event (dict): single event from google calendar
        """
        event = {}
        if 'summary' in _event:
            event['title'] = _event['summary']
        else:
            event['title'] = 'No title'
            
        if 'date' in _event['start']:
            event['time'] = 'all-day'
        else:
            start = common.get_time_only(_event['start']['dateTime'])
            end = common.get_time_only(_event['end']['dateTime'])
            event['time'] = f"{start} to {end}"
        self.weekly_events[day]['events'].append(event)
    

    def construct_workweek_events(self, dt):
        """
        To construct all events in that workweek based on the datetime
        """
        events = self.get_workweek_calendar_events_from_google(dt)
        self.weekly_events = common.prepare_json_schema(dt)
        
        for event in events:
            if 'dateTime' in event['start']:
                datetime_str = event['start']['dateTime']
            else:
                datetime_str = event['start']['date']

            if common.is_multidays_event(event) > 1:
                n = common.is_multidays_event(event)
            else:
                n = 1

            for i in range(n):
                day = common.get_day_of_week(datetime_str, i)
                self.construct_event(day, event)
