from structures.requirement_id import RequirementId


class Requirement:
    def __init__(self, section, sub, title, text, tags):
        self._unique_id = RequirementId(section, sub)
        self.text = text
        self.tags = tags
        self.title = title

    @property
    def unique_id(self):
        return self._unique_id

    def to_string(self):
        string = self.unique_id.to_string() + ": " + self.title + "\n" + self.text +"\n\t"
        for x in self.tags:
            string += "#" + x + ", "
        return string


class RequirementList:
    def __init__(self):
        self.req_map = {}

    @property
    def map(self):
        return self.req_map

    def append(self, requirement):
        if (requirement.unique_id.section, requirement.unique_id.sub) not in self.req_map:
            self.req_map[(requirement.unique_id.section, requirement.unique_id.sub)] = {}
        self.req_map[(requirement.unique_id.section, requirement.unique_id.sub)][
            requirement.unique_id.unique_id] = requirement

    def remove(self, requirement):
        del self.req_map[(requirement.unique_id.section, requirement.unique_id.sub)][requirement.unique_id]

    @staticmethod
    def get_section_lists():
        thing = set()
        for x in requirements_list.map:
            thing.add(x[0])
        return list(thing)

    @staticmethod
    def get_subsection_lists(section):
        thing = set()
        for x in requirements_list.map:
            if x[0] == section:
                thing.add(x[1])
        return list(thing)

    @staticmethod
    def add_requirement(requirement):
        requirements_list.append(requirement)

    @staticmethod
    def get_requirement_map():
        return requirements_list.map

    @staticmethod
    def clear_list():
        requirements_list.map.clear()


requirements_list = RequirementList()
