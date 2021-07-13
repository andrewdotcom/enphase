import requests
import os
import csv
import datetime
import pytz

class enphaseAPIReading: 
    '''
    Class to wrap the enphase api
    '''
    readings_dict = []

    def __init__(self):
        '''
        Initialise system_id from api key and user_id.
        '''

        try:
            self.readings_dict = requests.get('http://envoy.local/production.json').json()
        except:
            pass

    def get_filename(self):
        now   = datetime.datetime.now()
        zone  = pytz.timezone("Europe/London")
        now   = zone.localize(now)
        today = now.strftime("%Y-%m-%d")
        return today+".csv"    

    def to_csv(self, path='./'):
        
        reading_types = ['production', 'consumption']
        
        for reading_type in reading_types:
            headers = []
            for key in self.readings_dict[reading_type][0]:
                headers.append(key)

            filename = path+reading_type+"/"+self.get_filename()
            file_exists = os.path.isfile(filename)
            dir_exists = os.path.isdir(os.path.dirname(filename))

            if not dir_exists:
                os.makedirs(os.path.dirname(filename))

            with open (filename, 'a') as f:
                writer = csv.DictWriter(f, delimiter=',', lineterminator='\n',fieldnames=headers)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(self.readings_dict[reading_type][0])

    def drawGraph():
        pass

    def post_tweet():
        pass
            
#Example usage
if __name__ == "__main__":
    solar = enphaseAPIReading()
    solar.to_csv("/enphase/data/")