# -*- coding: utf-8 -*-

def parse_file(path):
    if path is None:
        return 
    data = read_data_from_file(path)
    results = []
    for elem in data:
        results.append(average(elem))
    print_results(results)
    

def read_data_from_file(path=None):
    features, test, time = [], [], []
    f = open(path, 'r', encoding='utf-8')
    for line in f:
        new_line = line.replace('\n', '')
        new_line = new_line.replace(',', '.')
        new_line = new_line.replace('\ufeff', '')
        if "Признаки: " in new_line:
            features.append(int(new_line.replace("Признаки: ", '')))
        elif "Тест: " in new_line:
            test.append(float(new_line.replace("Тест: ", '')))
        elif "Время: " in new_line:
            time.append(float(new_line.replace("Время: ", '')))
    f.close()
    return (features, test, time)


def print_results(results):
    print('Признаки:\t{0}'.format(results[0]))
    print('Тест:\t{0}'.format(results[1]))
    print('Время:\t{0}'.format(results[2]))


def average(struct):
    return round(sum(struct)/len(struct), 2)
