import json


def record_data(cat, data, ident=None):

    with open('test_file.json', 'r') as read_obj:
        current = json.load(read_obj)
        if cat == 'id':
            current['users'][data] = {"categories": [], "keywords": []}
        else:
            current['users'][str(ident)][cat].append(data)

    with open('test_file.json', 'w') as write_obj:
        json.dump(current, write_obj, ensure_ascii=False)

    print(current)


if __name__ == '__main__':
    #record_data('id', 1591)
    record_data('keywords', 'путин', 1591)
