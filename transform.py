def rel_file_path_to_os_abs_file_path(local_file_path):
    import os

    ROOT_DIR = os.path.dirname(__file__)

    abs_file_path = os.path.join(ROOT_DIR, local_file_path)
    abs_file_path = os.path.normpath(abs_file_path)

    return abs_file_path


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
        break_date = datetime.date(2013, 1, 1)

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
            if date < break_date:
                continue

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

        if date < break_date:
            continue

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

        if date < break_date:
            continue

        if d['tid'] == '12:00:00':
            time_series_dict[date] = {
                'wind_direction': d['vindriktning'],
                'wind_speed': d['vindhastighet']
            }

    return time_series_dict


def merge_data_sources():

    store_data = csv_timeseries_to_dict(file_path='data/revenue.csv')

    card_machine_data = csv_to_dict('data/kortautomat.csv')
    card_machine_data = convert_kortautomat_data_to_timeseries_dict(card_machine_data)

    rain_data = csv_timeseries_to_dict(file_path='data/smhi-regn.csv')

    temperature_data = csv_timeseries_to_dict(file_path='data/smhi-min-max-temp.csv')

    smhi_wind_data = csv_to_dict('data/smhi-vind.csv')
    smhi_wind_data = convert_smhi_wind_data_to_timeseries_dict(smhi_wind_data)

    dates_with_revenue_data = sorted(set(list(store_data) + list(card_machine_data)))

    #TODO: Loop over every date and combine data to a new big dict and or (list of lists)
    #TODO: Save to json/csv file so it can be easily loaded later
