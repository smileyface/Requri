import structures


def _get_lists():
    return structures.get_lists()


def get_tags(tag):
    found_requirements = []
    for x in _get_lists():
        if tag in x.tags:
            found_requirements.append(x)
    return found_requirements
