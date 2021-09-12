REMOVED = 'removed'
ADDED = 'added'
UPDATED = 'updated'
UNCHANGED = 'unchanged'

CHAR_BY_DIFF = {
    REMOVED: '-',
    ADDED: '+',
    UPDATED: '-',
    UNCHANGED: ' ',
}


def to_json(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return str(value)


def to_plain(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, str):
        return f'\'{value}\''
    return to_json(value)
