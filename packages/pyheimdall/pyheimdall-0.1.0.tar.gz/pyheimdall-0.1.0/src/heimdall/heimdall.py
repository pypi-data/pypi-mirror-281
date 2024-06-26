#! /usr/bin/env python
# -*- coding: utf-8 -*-
from . import hera

MODULES = {
    'xml:hera': hera,
    }


def getDatabase(db):
    get = getattr(MODULES[db.format], 'getDatabase')
    tree = get(db)
    return tree


def getItems(tree, filter=None):
    items = tree.findall('.//item')
    if filter:
        return [item for item in items if filter(item)]
    return items


def getItem(tree, filter=None):
    items = getItems(tree, filter)
    if len(items) == 0:
        return None
    if len(items) == 1:
        return items[0]
    raise IndexError("Too many items ({count})".format(count=len(items)))


def getMetadata(item, pid=None):
    if pid:
      xpath = './/metadata[@pid="{pid}"]'.format(pid=pid)
      return item.findall(xpath)
    return item.findall('.//metadata')


def getValues(item, pid):
    xpath = './/metadata[@pid="{pid}"]'.format(pid=pid)
    values = []
    for metadata in item.findall(xpath):
        values.append(metadata.text)
    return values


def getValue(item, pid):
    values = getValues(item, pid)
    if len(values) == 0:
        return None
    if len(values) == 1:
        return values[0]
    raise IndexError("Too many metadata ({count})".format(count=len(values)))

# def getValue(item, pid, v):

class Config:
    def __init__(self, **entries):
        self.__dict__.update(entries)


if __name__ == '__main__':
    args = {
        'format': 'xml:hera',
        'url': '../xquery/ckp_the_books.xml',
        }
    config = Config(**args)
    tree = getDatabase(config)
    # print(etree.tostring(tree, pretty_print=True, encoding=str))

    def by_15th_dynasty(node):
        pid = 'the_books:dynasty'
        value = '15'
        xpath = './/metadata[@pid="{pid}" and text()="{v}"]'.format(pid=pid, v=value)
        found = node.xpath(xpath)
        return len(found) > 0
    print(len(getItems(tree, by_15th_dynasty)))
