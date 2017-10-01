def safe_write_to_dict(my_dict, key_list, value, write_mode='w'):
    """
    Safely writes value to my_dict located in the keys specified in key list
    Does not assume my_dict to be completely initialized with the keys.

    Write modes
        w  Creating new value (overwriting existing value) (default)
        a  appending a list (creates a list if it does not exist)
        +  adding (to 0 if it does not exist)
        - subtracting (to 0 if it does not exist

    Example:
         > my_dict = {'student': {'name': 'Joe'}}

         > my_dict = safe_write_to_dict(my_dict, ['student', 'phone','swedish', 'home'], '77777777')
         > my_dict = safe_write_to_dict(my_dict, ['student', 'phone','swedish', 'mobile'], '12345678')
         > my_dict = safe_write_to_dict(my_dict, ['student', 'adress','home'], 'Magasinsgatan')

    Produces the following result:

        my_dict = {student': {'adress': {'home': 'Magasinsgatan'},
                              'name': 'Joe',
                              'phone': {'swedish': {'home': '77777777',
                                                    'mobile': '12345678'}
                                       }
                              }
        }

    Author: Fredrik Elofsson

    """

    # Base case
    if len(key_list) == 1:

        if write_mode == '+' or write_mode == '-':
            sign = 1 if write_mode == '+' else -1

            if key_list[0] not in my_dict:
                my_dict[key_list[0]] = value
            else:
                my_dict[key_list[0]] += sign * value

        elif write_mode == 'a':

            if key_list[0] not in my_dict:
                my_dict[key_list[0]] = list()

            if type(my_dict[key_list[0]]) is not list:  # Make it a list if its not
                my_dict[key_list[0]] = [my_dict[key_list[0]]]

            my_dict[key_list[0]].append(value)

        elif write_mode == 'w':  # this is write mode 'w'
            my_dict[key_list[0]] = value
        else:
            print("Incorrect write mode submitted to safe_write_to_dict")

    else:  # We have a longer key_list, we need to dig deeper...
        if key_list[0] not in my_dict:
            my_dict[key_list[0]] = dict()  # initialize if it does not exist

        # Recursive call
        my_dict[key_list[0]] = safe_write_to_dict(my_dict[key_list[0]], key_list[1:], value, write_mode)

    return my_dict


def invert_list_of_dicts_by_key(list_of_dicts, key_to_invert_by='_id', dict_entries_as_lists=False, keys=None):
    """ 'Flips' a sequence (list) of dicts, creating a new dict by the provided key name. E. g.

            list_of_dicts = [{'_id': 2,      'name': John},
                             {'_id': 'ae5f', 'name': Jane}]

        will produce output

            new_dict = {'2':    {'name': John},
                        'ae5f': {'name': Jane}}

        If key_to_invert_by exists in several dicts in the list, the resulting dict will have a
        list at corresponding dict key.

        If dict_entries_as_lists = True, all entries in the resulting dict will be lists, even if they
        only contain one element.

        keys -- a list of keys that should be force-written to the outputed dict,
                       where each entry will be None if dict_entries_as_lists = False, an empty list otherwise

        Complexity: O(n * m) where n is the number of elements (dicts) in list_of_dicts
                                   m is the number of key entries in each dict ^

    @author: felofsson
    Last updated: 2017-03-01
    """

    # Parse input
    if type(list_of_dicts) is not list:
        list_of_dicts = [list_of_dicts]

    new_dict = dict()

    for tmp_dict in list_of_dicts:

        if tmp_dict[key_to_invert_by] in new_dict:
            append = True
            if type(new_dict[tmp_dict[key_to_invert_by]]) is not list:
                new_dict[tmp_dict[key_to_invert_by]] = [new_dict[tmp_dict[key_to_invert_by]]]
        else:

            if dict_entries_as_lists is True:
                new_dict[tmp_dict[key_to_invert_by]] = []
                append = True
            else:
                new_dict[tmp_dict[key_to_invert_by]] = dict()
                append = False

        dict_to_add = {}

        for tmp_dict_key in tmp_dict:
            if tmp_dict_key not in key_to_invert_by:
                dict_to_add[tmp_dict_key] = tmp_dict[tmp_dict_key]

        if append:
            new_dict[tmp_dict[key_to_invert_by]].append(dict_to_add)
        else:
            new_dict[tmp_dict[key_to_invert_by]] = dict_to_add

    # Parse the output, add extra keys if they are not present already
    if keys is not None:
        if dict_entries_as_lists is True:
            default_value = []
        else:
            default_value = None

        if type(keys) is not list:
            keys = [keys]

        for tmp_key in keys:
            if tmp_key not in new_dict:
                new_dict[tmp_key] = default_value  # add a new key field

    return new_dict


def merge_dicts(a, b):
    """merges dict b into dict a and return merged result recursively

        NB: b is merged into a -- and dicts are immutable objects => the following would lead to undesired behaviour

        b = dict( .. )
        a = dict(.. )

        tmp = a

        a = merge_dicts(a, b)
        print(a)
        print(tmp) <--- tmp is now merged aswell!

        Solution: use copy.deepcopy in the input to merge_dicts

    NOTE: tuples and arbitrary objects are not handled as it is totally ambiguous what should happen"""

    key = None

    if isinstance(a, int) or isinstance(a, float):
        # add dict values together
        if b is not None:
            a += b
    elif a is None or isinstance(a, str):
        # If it's a string, overwrite
        a = b
    elif isinstance(a, list):
        # lists can be only appended
        if isinstance(b, list):
            # merge lists
            a.extend(b)
        else:
            # append to list
            a.append(b)
    elif isinstance(a, dict):
        # dicts must be merged recursively
        if isinstance(b, dict):
            for key in b:
                if key in a:
                    a[key] = merge_dicts(a[key], b[key])
                else:
                    a[key] = b[key]
    return a
