import logging

import structures


def _get_lists():
    return structures.get_lists()


#Additive
def get_tags(tag):
    found_requirements = []
    for x in _get_lists():
        if tag in x.tags:
            found_requirements.append(x)
    return found_requirements


def get_tagged():
    found_requirements = []
    for x in _get_lists():
        if len(x.tags) > 0:
            found_requirements.append(x)
    return found_requirements


def get_titles(title):
    found_requirements = []
    for x in _get_lists():
        if title == x.title:
            found_requirements.append(x)
    if found_requirements == []:
        logging.error(f"Title {title} not found")
        return None
    return found_requirements


def get_titled():
    found_requirements = []
    for x in _get_lists():
        if not x.title == "":
            found_requirements.append(x)
    return found_requirements


def get_all():
    return _get_lists()
