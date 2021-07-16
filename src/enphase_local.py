import requests
import os
import csv
import datetime as datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import pandas as pd

class enphaseAPIReading: 
    '''
    Class to wrap the enphase api
    '''
    readings_dict = []
    payment_rate = 0.05
    city_name = 'Empire Bay'
    now   = datetime.datetime.now()
    zone  = pytz.timezone("Europe/London")
    now   = zone.localize(now)
    today = now.strftime("%Y-%m-%d")

    def __init__(self):
        '''
        Initialise system_id from api key and user_id.
        '''

        try:
            self.readings_dict = requests.get('http://envoy.local/production.json').json()
        except:
            pass

    def get_filename(self):
        return f'{self.today}.csv'

    def get_png_filename(self):
        return f'{self.today}.png'   

    def to_csv(self):
        
        reading_types = ['production', 'consumption']
        
        for reading_type in reading_types:
            headers = []
            for key in self.readings_dict[reading_type][0]:
                headers.append(key)

            filename = f'/enphase/data/{reading_type}/{self.get_filename()}'
            file_exists = os.path.isfile(filename)
            dir_exists = os.path.isdir(os.path.dirname(filename))

            if not dir_exists:
                os.makedirs(os.path.dirname(filename))

            with open (filename, 'a') as f:
                writer = csv.DictWriter(f, delimiter=',', lineterminator='\n',fieldnames=headers)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(self.readings_dict[reading_type][0])

    def to_graph(self, csv_file=''):
        
        if csv_file == '':
            csv_file = f'/enphase/data/production/{self.get_filename()}'

        df = pd.read_csv(csv_file)
        df = df.drop(['type', 'activeCount', 'whLifetime'], axis=1)
        df['time'] = pd.to_datetime(df['readingTime'], unit='s') 
        df['wNow'] = df['wNow'].map(lambda x: x if x>0 else 0 )

        total_kwh = round((df['wNow'].sum(axis=0)/60/1000), 2)
        money = '${:.2f}'.format((round((total_kwh * self.payment_rate),2)))

        print(df.to_string())

        #df.plot(x='time', y='wNow', kind='line')
        
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.bar(df['time'],
        df['wNow'],
        color='purple')

        ax.set(
            xlabel=self.today,
            ylabel="Generated Electricity (Watts)",
            title='Solar Panels (' + self.city_name + ')\nGenerated ' + str(total_kwh) + 'kWh - Earned ' + money)

        date_form = DateFormatter("%H:%I")
        ax.xaxis.set_major_formatter(date_form)

        fig.autofmt_xdate()

        plt.savefig(f"/enphase/data/{self.today}_graph.png")
        
    def post_tweet():
        pass
            
#Example usage
if __name__ == "__main__":
    solar = enphaseAPIReading()
    solar.to_csv()
    solar.to_graph()