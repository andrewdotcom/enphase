import requests
import os
import csv
import datetime
import pytz

class enphaseAPIReading: 
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

    def get_filename(self):
        now   = datetime.datetime.now()
        zone  = pytz.timezone("Europe/London")
        now   = zone.localize(now)
        today = now.strftime("%Y-%m-%d")
        return today+".csv"    

    def to_csv(self, path='./'):
        summaryJSON = self.summary()
        headers = []
        readings = []
        for key in summaryJSON:
            headers.append(key)

        filename = path+self.get_filename()
        file_exists = os.path.isfile(filename)

        with open (filename, 'a') as f:
            writer = csv.DictWriter(f, delimiter=',', lineterminator='\n',fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(summaryJSON)
            
#Example usage
if __name__ == "__main__":
    solar = enphaseAPIReading(os.getenv('USER_ID'),os.getenv('KEY'))
    solar.to_csv("./data/")