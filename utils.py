def parse_list(values, message, recursion_level, verbose):
    '''parse list to protobuf message'''
    if isinstance(values[0], dict):  # value needs to be further parsed
        for v in values:
            cmd = message.add()
            parse_dict_to_protobuf_message(v, cmd, recursion_level, verbose)
    else:  # value can be set
        message.extend(values)


def parse_dict_to_protobuf_message(values, message, recursion_level, verbose=False):
    for k, v in values.items():

        if verbose:
            tab_str = "\t" * recursion_level
            print("{}Parsing {} -> {}".format(tab_str, k, v))

        if isinstance(v, dict):  # value needs to be further parsed
            print("{}  - isinstance(v, dict)".format(tab_str))
            parse_dict_to_protobuf_message(v, getattr(message, k), recursion_level + 1, verbose)

        elif isinstance(v, list):
            print("{}  - isinstance(v, list)".format(tab_str))
            parse_list(v, getattr(message, k), recursion_level + 1, verbose)

        else:  # value can be set
            print("{}  - else".format(tab_str))

            try:
                setattr(message, k, v)

            except Exception as e:
                print(tab_str + str(e))
                try:
                    setattr(message, k, bytes(v))
                except Exception as e:
                    print(tab_str + str(e))
                    try:
                        new_value = dict(dict(message.DESCRIPTOR.fields_by_name)[k].enum_type.values_by_name)[v].number
                        setattr(message, k, new_value)
                    except Exception as e:
                        print(tab_str + str(e))
                        pass