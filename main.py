import transform

#print(transform.csv_timeseries_to_dict(file_path='data/revenue.csv'))
#print(transform.csv_timeseries_to_dict(list_of_lists=[['datum', 'a', 'b'], ['2017-09-01', '1', 'ssfs-']]))
#smhi_wind_data = transform.csv_to_dict('data/smhi-vind.csv')
#print(transform.convert_smhi_wind_data_to_timeseries_dict(smhi_wind_data))

#transform.merge_data_sources()

data = transform.json_to_dict('data/data.json')
print(type(data))
print(data)
transform.plot_data(data, 'rain', 'bensin')
