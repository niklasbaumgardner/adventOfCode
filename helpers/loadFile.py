def read_file(filename):
    fp = open(filename)
    file = fp.read().strip()
    return file
