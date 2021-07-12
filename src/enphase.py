import requests
import os

class enphase: 
    '''
    Class to wrap the enphase api
    '''
    def __init__(self, user_id, key):
        '''
        Initialise system_id from api key and user_id.
        '''
        if user_id == '' or key == '':
            return

        self.user_id = user_id
        self.key = key

        try:
            system_json = requests.get(f'https://api.enphaseenergy.com/api/v2/systems?key={self.key}&user_id={self.user_id}').json()
            self.system_id = system_json['systems'][0]['system_id']
        except:
            self.system_id = 0

    def summary(self):
        '''
        Gets the summary information for the system and returns 
        a dictionary of results.
        '''
        try:
            summary_json = requests.get(f'https://api.enphaseenergy.com/api/v2/systems/{self.system_id}/summary?key={self.key}&user_id={self.user_id}').json()
        except:
            summary_json = {}
        return summary_json

#Example usage
solar = enphase(os.getenv('USER_ID'),os.getenv('KEY'))
summary = solar.summary()
print(summary)