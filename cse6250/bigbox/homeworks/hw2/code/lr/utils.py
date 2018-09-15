to_float_tuple = lambda x: (int(x[0]), float(x[1]))


def parse_svm_light_data(input):

    for line in input:
        yield parse_svm_light_line(line)


def parse_svm_light_line(line):
    splits = line.split()

    y = float(splits[0])
    X = []
    if len(splits) > 1:
        X = [to_float_tuple(kv.split(':')) for kv in splits[1:]]
    else:
        X = []
    return (X, y)
