from re import search, findall

"""
As seen in https://hades.fandom.com/wiki/Zeus/Quotes, there are human readable titles. ZeusWithDemeter -> Duo - Zeus and Demeter
The functions in here will try to create them automatically from the provided ID's
"""

# Don't use \d: NameCloseWithName
duo = (r"([A-Z][a-z]*)With(\D*)(\d*)", "Duo - {0} and {1} ({2})")


tests = [
    duo
    ]

def id_to_description(id):
    result = None

    for (regex, format_string) in tests:
        result = search(regex, id)
        if result is not None:
            # Parse out any camelcase remaining
            #results = [split_camelcase_into_array(value) for value in result.groups()]
            description = format_string.format(*result.groups())
            return description

    # If no matching description can be found, split the ID according to Camelcase
    return " ".join(split_camelcase_into_array(id))

    


def split_camelcase_into_array(string):
    regex_search = findall(r"[A-Z][a-z]*|[0-9]*", string)
    return [result for result in regex_search if result != ""]

