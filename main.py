import transform
# transform.merge_data_sources()    # create new data.json file

data = transform.json_to_dict('data/data.json')
print(len(data), data)
transform.plot_data(data, 'rain', 'bensin')
