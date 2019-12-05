import json

file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)


def get_by_key(data, key):
    values = data[key].items()
    values = [(int(index), item) for index, item in values]
    values = sorted(values, key=lambda x: x[0])

    return values


# Breaks down the items by the top level directory
authors = get_by_key(data, 'Author')
descriptions = get_by_key(data, 'Description')
direct_links = get_by_key(data, 'DirectLink')
languages = get_by_key(data, 'Language')
photo_links = get_by_key(data, 'PhotoLink')
providers = get_by_key(data, 'Provider')
titles = get_by_key(data, 'Title')
week_sections = get_by_key(data, 'WeekSection')
knowledges = get_by_key(data, 'Knowledge')


def get_course(id):
    course_title = titles[id][1]
    course_description = descriptions[id][1]
    course_provider = providers[id][1]
    course_prof = ', '.join(authors[id][1])
    course_knowledge = ', '.join(knowledges[id][1])

    return f"\n{course_title} ({course_provider})\n\n{course_prof}\n\n{course_description}\n\n{course_knowledge}"


print(get_course(5))
