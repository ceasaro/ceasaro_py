INFO = 'info'
ERROR = 'error'


def error(msg):
    log(msg, ERROR)


def log(msg, level=INFO):
    if level==ERROR:
        print "ERROR> {0}".format(msg)
    else:
        print msg