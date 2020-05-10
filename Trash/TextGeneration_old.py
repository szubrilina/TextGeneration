import random
import string
import json
import argparse
import sys

# ---------------------------------------------------------------------------
# ---------------------CALCULATING PROBABILITIES-----------------------------
# ---------------------------------------------------------------------------


def final_format(str):

    if len(str) <= 1:
        return str

    for i in range(3):
        for ch1 in string.punctuation:
            str = str.replace(ch1 + " " + ch1, ch1)

    str = str.replace(" ,", ",")
    str = str.replace(" .", ".")
    str = str.replace(" !", "!")
    str = str.replace(" '", "'")
    str = str.replace(" :", ":")
    str = str.replace(" ;", ";")
    str = str.replace(" $", "$")
    str = str.replace(" %", "%")
    str = str.replace(" ?", "?")
    str = str.replace(" )", ")")
    str = str.replace("( ", "(")
    str = str.replace(",.", ".")
    str = str.replace(",)", ")")

    str = str.lstrip()
    str = str.lstrip((string.punctuation).replace('"', ''))
    str = str.rstrip(";:,")

    new_str = ""
    # quotes = 0
    # brackets = 0

    quotes = 0
    brackets = ""

    next_step = 0
    for ch in str:
        fl = 1

        if next_step == 1 and ch not in string.ascii_letters:
            continue

        if next_step == 1 and ch in string.ascii_letters:
            next_step = 0

        if ch == '"':
            if quotes > 0:
                quotes -= 1
                new_str = new_str[:-1]
            else:
                quotes += 1
                next_step = 1

        if ch == ')':
            if len(brackets) > 0:
                brackets = brackets[:-1]
            else:
                fl = 0

        if ch == '(':
            brackets += '('

        if fl:
            new_str += ch

    str = new_str

    str = str.replace(" )", ")")
    str = str.replace("( ", "(")

    str = str.replace("  ", " ")

    for ch in string.ascii_lowercase:
        str = str.replace(". " + ch, ". " + ch.upper())
    for ch in string.ascii_lowercase:
        str = str.replace("? " + ch, "? " + ch.upper())
    for ch in string.ascii_lowercase:
        str = str.replace("! " + ch, "! " + ch.upper())
    for ch in string.ascii_lowercase:
        str = str.replace(", " + ch, ", " + ch.lower())

    str = str[::-1]
    str = (str).replace('(', "", len(brackets))
    str = (str).replace('"', "", quotes)
    str = str[::-1]

    str = str.rstrip()
    str = str.lstrip()

    str = str.replace("  ", " ")

    if str != "" and str[-1] not in "!?.":
        str += '.'

    if len(str) >= 2:
        str = str[0].upper() + str[1:]

    return str


def get_string(list):
    str = ""
    for item in list:
        str = str + item + ' '

    str = str.rstrip(" ")
    return str


def calculate_n_tokens(depth, tokens_list, probabilities):

    current = []

    for item in tokens_list:
        current.append(item)

        if len(current) < depth:
            continue

        str = get_string(current[:-1:])

        if probabilities.get(str, None) is None:
            probabilities[str] = dict()

        if probabilities[str].get(item, None) is None:
            probabilities[str][item] = 0

        probabilities[str][item] += 1

        current = current[1::]

    return probabilities


def calculate_all_len_tokens(max_depth,
                             list):

    probabilities = dict()

    for d in range(1, max_depth + 1, 1):
        probabilities = calculate_n_tokens(d,
                                           list,
                                           probabilities)

    return probabilities


def read_initial_text(input_file):

    tokens_list = []

    input = open(input_file, "r")
    s = input.read()

    s = s.split()

    for token in s:
        while token != "" and (string.punctuation).find(token[0]) != -1:
            tokens_list.append(token[0])
            token = token[1:]

        new_token = token.rstrip(string.punctuation)
        tokens_list.append(new_token)

        while token != "" and (string.punctuation).find(token[-1]) != -1:
            tokens_list.append(token[-1])
            token = token[:-1]

    input.close()
    return tokens_list

# -------------------------------------------------------------------------
# ------------------------GENERATING TEXT----------------------------------
# -------------------------------------------------------------------------


def decide(current_text, probabilities, uniform_proba):

    random_number = random.random()

    if uniform_proba > random_number:
        current_text = ""

    dict = probabilities[get_string(current_text)]

    list_keys = []
    list_vals = []

    for k, v in dict.items():
        list_keys.append(k)
        list_vals.append(v)

    prev = 0
    for i in range(len(list_vals)):
        list_vals[i] += prev
        prev = list_vals[i]

    random_number = random.uniform(0, prev)

    for ind in range(len(list_vals)):
        if list_vals[ind] >= random_number:
            return list_keys[ind]


def generate(depth, probabilities, len_of_generating_text, uniform_proba):

    current_text = []
    output_text = []

    for i in range(len_of_generating_text):

        new_item = decide(current_text, probabilities, uniform_proba)

        current_text.append(new_item)
        output_text.append(new_item)

        while (len(current_text) > depth or
               probabilities.get(get_string(current_text), None) is None):
            current_text = current_text[1::]

    print(get_string(output_text), end="\n\n")
    result = final_format(get_string(output_text))
    return result


# -----------------------------------------------------------------------
# ------------------------MAIN-------------------------------------------
# -----------------------------------------------------------------------


def calculate_probabilities(args):

    tokens_list = read_initial_text(args.input_file)

    probabilities = calculate_all_len_tokens(args.depth, tokens_list)

    with open(args.probabilities_file, "w") as write_file:
        json.dump(probabilities, write_file)

    # print(probabilities)


def generate_text(args):

    with open(args.probabilities_file, "r") as read_file:
        probabilities = json.load(read_file)

    result = generate(args.depth, probabilities,
                      args.number_of_tokens, args.uniform_proba)

    if args.output_file is None:
        print(result)
    else:
        with open(args.output_file, "w") as write_file:
            write_file.write(result)

    # print(result)

# str = input()
# str = final_format(str)
# print (str)


parser = argparse.ArgumentParser(description='Parser')
subparsers = parser.add_subparsers(help='sub-command help')

parser_probab = subparsers.add_parser('calculate_probabilities',
                                      help='for colculating probabilities')

parser_probab.add_argument('--input_file', default=None,
                           help='file name with text, more than 10000 words')

parser_probab.add_argument('--probabilities_file', default=None,
                           help='file name where dict' +
                                ' with probabilities will be writen. (.json)')

parser_probab.add_argument('--depth', type=int,
                           help='maximal depth for tokens')

parser_probab.set_defaults(func=calculate_probabilities)

parser_gen = subparsers.add_parser('generate_text',
                                   help='for generating random text')

parser_gen.add_argument('--probabilities_file', default=None,
                        help='File name where dict with probabilities is.' +
                             ' It must be .json')

parser_gen.add_argument('--depth', type=int,
                        help='maximal depth for tokens')

parser_gen.add_argument('--number_of_tokens', type=int,
                        help='number_of_tokens')

parser_gen.add_argument('--uniform_proba', default=0, type=float,
                        help='with uniform_proba probability we ' +
                             'schoose new token' +
                             ' from all ignoring depth-1 last ones')

parser_gen.add_argument('--output_file', default=None,
                        help='(Optional, defaul terminal). ' +
                             'File name where generated text will' +
                             'be written. (.txt)')

parser_gen.set_defaults(func=generate_text)

# args = parser.parse_args()
args.func(args)
