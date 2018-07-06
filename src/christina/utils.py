import re


# Very naive tokenizer.
WORD_PATTERN = re.compile(
    r'''
    [@|#]?  # Maybe a mention or an issue?
    [-\w]+  # Word-like.
    ''',
    re.VERBOSE,
)


def find_words(sentence):
    return WORD_PATTERN.findall(sentence)


def iter_issue_number(words):
    for word in words:
        if word.startswith('#') and word[1:].isdigit():
            yield int(word[1:])
