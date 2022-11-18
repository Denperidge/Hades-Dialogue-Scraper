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

array_parse_ints = lambda x: int(x) if x.isnumeric() else x

def id_to_description(id):
    result = None

    for (regex, format_string) in tests:
        result = search(regex, id)
        if result is not None:
            # Parse out any camelcase remaining
            results = [split_camelcase(value) for value in result.groups()]
            results = [array_parse_ints(value) for value in results]
            print(results)
            description = format_string.format(*results)
            return description

    # If no matching description can be found, split the ID according to Camelcase
    return split_camelcase(id)

    


def split_camelcase(string):
    regex_search = findall(r"[A-Z][a-z]*|[0-9]*", string)
    return " ".join([result for result in regex_search if result != ""])

