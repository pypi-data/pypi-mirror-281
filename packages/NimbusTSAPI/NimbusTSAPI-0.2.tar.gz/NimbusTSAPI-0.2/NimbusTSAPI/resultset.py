import pandas as pd

class ResultSet(dict):
    def DataFrame(self):
        df = pd.DataFrame()

        for _,ts in enumerate(self['data']['tss']):
            stedict = {
                'datetimes':[],
                'values':[],
            }
            for i,values in enumerate(ts['values']):
                stedict['datetimes'].append(values['datetime'])
                stedict['values'].append(values['value'])
            df['datetimes'] = stedict['datetimes']
            df[ts['name']] = stedict['values']
        return df