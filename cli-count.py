from datetime import datetime
import logging
import sys

FILE = "cli-count.txt"
UNIT = 1
log = logging.getLogger('cli-count')
ACTION_NEW = "new"
ACTION_ADD = "add"
ACTION_TOTAL = "total"
ACTION_LIST = "list"
OPTION_ALL = "all"


def help():
    print """
    cli-count ACTION TAG_NAME VALUE             :: general format
    cli-count new tag_name (start_value)        :: default start_value is 0
    cli-count add tag_name (value)              :: default value is 1
    cli-count total tag_name (start_date)       :: date format: dd.mm.year
    cli-count list (tag_name) (start_date)      :: date format: dd.mm.year
    cli-count tags (all)                        :: show tags (with all info)
    cli-count help                              :: examples on github
    """


def write(line):
    """ Append given line to FILE
    """
    with open(FILE, "a") as f:
        f.write(line)


def now():
    """ Return formatted now time. Example: Sun/17.09.2017/09:00:22
    """
    return datetime.now().strftime("%a/%d.%m.%Y/%H:%M:%S")


def new(action=None, tag_name=None, start_value=None):
    """ Create new tag and assign a start value
    """
    if tag_name is None:
        log.error("Missing tag name")
        return
    if start_value is None:
        start_value = 0
    line = '{} {} {} {} \n'.format(
        now(), ACTION_NEW, tag_name, str(start_value))
    write(line)
    log.info('{} {}'.format(ACTION_NEW, line))


def add(action=None, tag_name=None, value=None):
    """ Add value for given tag
    """
    if value is None:
        value = UNIT
    if tag_name is None:
        log.error("Missing tag name.")
        return

    # [TODO] Check if tag exist or it must be created.

    line = '{} {} {} {} \n'.format(now(), ACTION_ADD, tag_name, str(value))
    write(line)
    log.info('{} {}'.format(ACTION_ADD, line))


def total(action=None, tag_name=None, start_date=None):
    """ Show total value for a given tag
    """
    log.info("The total is...")


def list(action=None, tag_name=None, start_date=None):
    """ List records for a given tag (optional: starting from a given date)
    """
    log.info("Listing records...")
    if tag_name is not None:
        log.warning("[TODO] Implement tag filter.")
    if start_date is not None:
        log.warning("[TODO] Implement date filter.")
    with open(FILE, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            print line


def tags(option=None):
    """ Show existing tag names. If show_all is True: show all details
    """
    log.info("Listing tags...")
    tags = []
    show_all = True if option == OPTION_ALL else False

    with open(FILE, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            parts = line.split(" ")
            if parts[1] == ACTION_NEW:
                if show_all is True:
                    print line
                tags.append(parts[2])
    print tags


def create_file_if_missing():
    """ All records are added in this file. Make sure it exists.
    """
    try:
        f = open(FILE, 'r')
    except IOError:
        log.warning("Missing {} file.".format(FILE))
        f = open(FILE, 'w')
        log.info("Created {} file used to store everything.".format(FILE))

    f.close()


def do_operations(val1=None, val2=None, val3=None):
    """ Redirect to complete an action
    """
    if val1 == "new":
        new(action=val1, tag_name=val2, start_value=val3)
    elif val1 == "add":
        add(action=val1, tag_name=val2, value=val3)
    elif val1 == "total":
        total(action=val1, tag_name=val2, start_date=val3)
    elif val1 == "list":
        list(action=val1, tag_name=val2, start_date=val3)
    elif val1 == "tags":
        tags(option=val2)
    else:
        help()


def set_log():
    """ Settings related to logging
    """
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)


def init():
    """ Initialize first.
    """
    set_log()
    create_file_if_missing()


if __name__ == "__main__":
    """ Check for ACTION, TAG_NAME and VALUE as vals
        then do related operations
    """
    try:
        val1 = sys.argv[1]
    except Exception:
        val1 = None
    try:
        val2 = sys.argv[2]
    except Exception:
        val2 = None
    try:
        val3 = sys.argv[3]
    except Exception:
        val3 = None

    init()
    do_operations(val1=val1, val2=val2, val3=val3)
