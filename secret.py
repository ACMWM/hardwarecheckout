def get(name):
    with open(name) as f:
        return f.read().split()
