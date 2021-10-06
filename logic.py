"""this is functions of logic of my app"""
import pandas as pd


def get_df_columns(data_frame):
    '''this functions get data frame and returning his column names'''

    return list(data_frame.columns)


def checking_if_some_data_is_empty(data_frame, some = 0):
    '''this functions get data frame and return empty element id,
    if some = 0 it returns true/false, else index'''

    index_of_empty_column = []
    ind_of_emp = []
    colums = get_df_columns(data_frame)

    for index, row in data_frame.iterrows():
        yes_or_no = 0

        for i in colums:
            if pd.isna(row[i]):
                index_of_empty_column.append(False)
                ind_of_emp.append(index)
                yes_or_no = 1
                break

        if yes_or_no == 0:
            index_of_empty_column.append(True)

    if some == 0:
        return index_of_empty_column

    else:
        return ind_of_emp


def from_df_to_dict(data_frame):
    '''this functions get data frame and returning dictionary'''

    dict_1 = {}
    colums = get_df_columns(data_frame)
    index_of_empty_column = checking_if_some_data_is_empty(data_frame)

    for index, row in data_frame.iterrows():
        list_1 = []
        if index_of_empty_column[index]:
            for i in range(1,len(colums)):
                list_1.append(str(row[i]))
            dict_1[str(row[str(colums[0])])] = list_1

    return dict_1


def geting_elements_that_are_and_arent_in_base(base_dict, update_dict):
    '''this functions get 2 dicts and returning that elements of second
    that are in base and that arent in base'''

    are_dict = {}
    arent_dict = {}

    for i in update_dict:
        if i in base_dict:
            are_dict[i] = update_dict[i]

        else:
            arent_dict[i] = update_dict[i]

    return are_dict, arent_dict


def from_base_and_are_dict_get_dict(base_dict, are_dict):
    '''this functions get 2 dicts and returning combine of 2 dicts, 1 dict'''

    new_dict = {}

    for i in are_dict:
        list_1 = []
        list_1.append(i)

        for j in are_dict[i]:
            list_1.append(j)

        new_dict[base_dict[i][0]] = list_1

    return new_dict


def update_base_price(base_dict, are_dict):
    '''getting base and are dict and updateing base price'''

    return base_dict, are_dict


def add_data_to_base(base_dict, new_dict):
    '''this functions get 2 dicts and returning marge of 2 dicts, 1 dict'''

    res = base_dict | new_dict

    return res


def getting_image_ids_and_formats(file_names):
    '''this functions get file names and returnd ids and formats'''

    image_ids = []
    image_formats = []

    for file_name in file_names:
        image_ids.append(file_name[file_name.rindex("/")+1:file_name.rindex('.')])
        image_formats.append(file_name[file_name.rindex('.'):])

    return image_ids, image_formats


def from_dict_to_list(dict1):
    """this function is get dictionary and return list"""

    list_2 = []

    for i in dict1:
        list_1 = []
        list_1.append(i)

        for j in dict1[i]:
            list_1.append(j)
        list_2.append(list_1)

    return list_2
