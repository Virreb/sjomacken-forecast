def rel_file_path_to_os_abs_file_path(local_file_path):
    import os

    ROOT_DIR = os.path.dirname(__file__)

    abs_file_path = os.path.join(ROOT_DIR, local_file_path)
    abs_file_path = os.path.normpath(abs_file_path)

    return abs_file_path


def json_to_dict(file_path):
    import json
    #from bson import json_util

    if file_path[-5:] != '.json':
        file_path += '.json'

    # Get abs file path acc. to OS
    abs_file_path = rel_file_path_to_os_abs_file_path(file_path)

    # Dump to file
    with open(abs_file_path, 'r+', newline="\n", encoding="utf8") as json_file:
        json_dict = json.load(json_file)#, object_hook=json_util.object_hook)

    return json_dict


def dict_to_json(dict_data, file_path):
    """Writes dict or list of dict to json file with indent=2"""
    import json
    #from bson import json_util

    if file_path[-5:] != '.json':
        file_path += '.json'

    # Get abs file path acc. to OS
    abs_file_path = rel_file_path_to_os_abs_file_path(file_path)

    # Dump to file
    with open(abs_file_path, 'w+', newline="\n", encoding="utf8") as json_file:
        json.dump(dict_data, json_file, indent=2)#, default=json_util.default)


def csv_to_dict(file_path):
    import csv

    abs_file_path = rel_file_path_to_os_abs_file_path(file_path)

    dict_list = []
    with open(abs_file_path, 'r+', encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict_list.append(row)

    return dict_list


def csv_timeseries_to_dict(file_path=None, list_of_lists=None, break_date=None):
    import csv, datetime, help_functions as hf

    if break_date is None:
        break_date = datetime.date(2013, 1, 1)  # Only use data after the break date

    time_series_dict = dict()
    if file_path is not None:
        abs_file_path = rel_file_path_to_os_abs_file_path(file_path)
        csvfile = open(abs_file_path, 'r+', encoding="UTF-8")
        data = csv.reader(csvfile, quotechar="'")

    elif list_of_lists is not None:
        data = list_of_lists

    for row_nbr, row in enumerate(data):

        if row_nbr == 0:
            headers = row
        else:

            date = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
            if date < break_date:   # skip if date before break date
                continue

            date = date.toordinal()

            for col_nbr, cell in enumerate(row):

                if col_nbr > 0:
                    if '-' in cell or ':' in cell:
                        val = cell
                    elif len(cell) == 0:
                        val = 0.0
                    else:
                        val = float(cell)

                    hf.safe_write_to_dict(time_series_dict, [date, headers[col_nbr]], value=val)

    if file_path is not None:
        csvfile.close()

    return time_series_dict


def convert_kortautomat_data_to_timeseries_dict(list_of_dicts, break_date=None):
    import help_functions as hf, datetime

    if break_date is None:
        break_date = datetime.date(2013, 1, 1)

    time_series_dict = dict()
    for d in list_of_dicts:
        date = datetime.datetime.strptime(d['datum'], '%Y-%m-%d %H:%M').date()

        if date < break_date:   # skip if date before break date
            continue

        date = date.toordinal()

        if d['produkt'] == 'Diesel':
            produkt = 'diesel'
        elif d['produkt'] == '95-oktan':
            produkt = 'bensin'

        val = d['belopp']
        if ',' in val:
            val = val.replace(',', '')
        val = round(float(val), 1)

        hf.safe_write_to_dict(time_series_dict, [date, produkt], val, write_mode='+')

    return time_series_dict


def convert_smhi_wind_data_to_timeseries_dict(list_of_dicts, break_date=None):
    import datetime

    if break_date is None:
        break_date = datetime.date(2013, 1, 1)

    time_series_dict = dict()
    for d in list_of_dicts:
        date = datetime.datetime.strptime(d['datum'], '%Y-%m-%d').date()

        if date < break_date:   # skip if date before break date
            continue

        date = date.toordinal()

        if d['tid'] == '12:00:00':
            time_series_dict[date] = {
                'wind_direction': d['vindriktning'],
                'wind_speed': d['vindhastighet']
            }

    return time_series_dict


def merge_data_sources():
    import help_functions as hf

    store_data = csv_timeseries_to_dict(file_path='data/revenue.csv')

    card_machine_data = csv_to_dict('data/kortautomat.csv')
    card_machine_data = convert_kortautomat_data_to_timeseries_dict(card_machine_data)

    rain_data = csv_timeseries_to_dict(file_path='data/smhi-regn.csv')

    temperature_data = csv_timeseries_to_dict(file_path='data/smhi-min-max-temp.csv')

    smhi_wind_data = csv_to_dict('data/smhi-vind.csv')
    smhi_wind_data = convert_smhi_wind_data_to_timeseries_dict(smhi_wind_data)

    # create init dict with every product set to 0.0 for the store data (uthyrning, kiosk, etc)
    store_groups = store_data[list(store_data.keys())[0]].keys()
    init_dict = dict()
    for g in store_groups:
        init_dict[g] = 0

    data = dict()
    data = hf.merge_dicts(data, store_data)
    data = hf.merge_dicts(data, card_machine_data)
    for date in data:

        data[date]['date'] = date

        if date in rain_data:
            data[date]['rain'] = rain_data[date]['rain']

        if date in temperature_data:
            data[date]['min_temp'] = temperature_data[date]['min_temp']
            data[date]['max_temp'] = temperature_data[date]['max_temp']

        if date in smhi_wind_data:
            data[date]['wind_direction'] = smhi_wind_data[date]['wind_direction']
            data[date]['wind_speed'] = smhi_wind_data[date]['wind_speed']

    dict_to_json(data, 'data/data.json')


def plot_data(data, x_key, y_key):
    import matplotlib.pylab as plt
    import datetime

    x, y = list(), list()
    for key, d in sorted(data.items()):
        if x_key in d:
            if x_key == 'date':
                x.append(datetime.date.fromordinal(d['date']))
            else:
                x.append(d[x_key])
        else:
            x.append(None)

        if y_key in d:
            y.append(d[y_key])
        else:
            y.append(None)

    plt.plot(x, y, 'o')
    plt.show()
