import os, datetime
from apiclient import discovery
from google.oauth2 import service_account


class G_Service:
    def __init__(self,
                 api_service_name,
                 api_version,
                 scopes,
                 client_secret_file,
                 ):
        """
        Initialization of Google API Service

        Args:
            api_service_name (str): google api name
            api_version (str): google api version
            scopes (list): google api access types
            client_secret_file (str): google service account secret file
        """
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.scopes = scopes
        self.client_secret_file = os.path.join(os.getcwd(), client_secret_file)
        self.service = self.create_service()
    
    
    def create_service(self):
        """
        To create a service to access the Google API

        Returns:
            obj: api service
        """
        try:
            credentials = service_account\
                .Credentials\
                .from_service_account_file(self.client_secret_file, 
                                           scopes=self.scopes
                                           )
            service = discovery.build(self.api_service_name, 
                                      self.api_version, 
                                      credentials=credentials
                                      )
            print(f'{self.api_service_name} {self.api_version} service created successfully')
            return service
        
        except OSError as e:
            print(e)
            print('Failed to create service instance')
            return None
