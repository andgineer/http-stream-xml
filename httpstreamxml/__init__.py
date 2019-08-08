__version__ = '1.3.1'


def version():
    """ 'major.minor' without build number """
    return '.'.join(__version__.split('.')[:2])


if __name__ == '__main__':
    print(version())
