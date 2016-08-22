# -*- coding: utf-8 -*-

'''
Nested Key Retriever (nkr - 'nuker') is a library for quickly finding adn bubbling up keys in deeply nested structures. Whereas you generally need knowledge of a complex structure to properly find/reference an item, this allows you to just search for a key anywhere in the structure without having knowledge of the structure's nesting levels

The initial object provided must be a dictionary, but the dictionary can contain any combination of dictionaries and lists nested within it.

The find_nested_key_value() function will return the first (or only) appearance of a key inside a nested dictionary structure
The find_nested_key_values() function is a generator that will yield a list of all values for the key should more than one instance exist in the nested dictionary
'''

def find_nested_key_value(target_dictionary, requested_key):
    try: #confirm the input is a dictionary
        target_dictionary.keys()
    except AttributeError:
        return None
    except Exception:
        raise
    for key in target_dictionary.keys():
            if key == requested_key: #Check if the current key being tested is our value and bubble it up
                return target_dictionary[key]
            try: #If this isn't our key, is its value a dictionary? If so, check all those keys
                target_dictionary[key].keys()
                value = find_nested_key_value(target_dictionary[key], requested_key)
                if value is not None:
                    return value
            except AttributeError:
                pass
            except Exception:
                raise
            try: #If not our key and not a dictionary, is the value a list? If so, check each index for additional dictionaries and check those keys
                target_dictionary[key][0]
                i = len(target_dictionary[key])
                while i > 0:
                        value = None
                        i -= 1
                        value = find_nested_key_value(target_dictionary[key][i], requested_key)
                        if value is not None:
                                return value
            except KeyError:
                pass
            except IndexError:
                pass
            except AttributeError:
                pass
            except TypeError:
                pass
            except Exception:
                raise

def find_nested_key_values(target_dictionary, requested_key):
    values = []
    try: #confirm the input is a dictionary
        for key in target_dictionary.keys():
                if key == requested_key: #check if the current key being tested is our value and bubble it up
                    values.append(target_dictionary[key])
                try: #If this isn't our key, is its value a dictionary? If so check all those keys for values
                    target_dictionary[key].keys()
                    dict_values = list(find_nested_key_values(target_dictionary[key], requested_key))
                    if len(dict_values) > 0:
                        for value in dict_values:
                            if not (isinstance(value, list) and len(value) == 0):
                                values.append(value)
                except AttributeError:
                    pass
                except Exception:
                    raise
                try: #if not our key and not a dictionary, is the value a list? If so, check each index for additional dictionaries and check those keys for values 
                    assert isinstance(target_dictionary[key], list)
                    i = len(target_dictionary[key])
                    while i > 0:
                        i -= 1
                        list_values = list(find_nested_key_values(target_dictionary[key][i], requested_key))
                        if len(list_values) > 0:
                            for value in list_values:
                                if not (isinstance(value, list) and len(value) == 0)
                                    values.append(value)
                except KeyError:
                    pass
                except IndexError:
                    pass
                except AttributeError:
                    pass
                except TypeError:
                    pass
                except AssertionError:
                    pass
                except Exception:
                    raise
    except AttributeError:
        yield []
    except Exception:
        raise
    for value in values: #Yield up all the valid returns
        yield value
