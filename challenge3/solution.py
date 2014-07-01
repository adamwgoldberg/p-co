"""Processes queries
"""

import sys

if len(sys.argv) != 3:
    sys.stderr.write('You should only provide 2 arguments to the script, the input file and the output file\n')
    sys.exit(2)

input_file = sys.argv[1]
output_file = sys.argv[2]

def search(dry_run=False):
    """Optimize this method to run faster."""

    num_matches = []

    with open(input_file) as input_descriptor:

        # read in input
        lines = input_descriptor.readlines()
        num_pins = int(lines[0].strip())
        pin_lines = map(str.strip, lines[1:num_pins + 1])
        num_queries = int(lines[num_pins + 1].strip())
        query_lines = map(str.strip, lines[num_pins + 2:])

        # process each query
        for query in query_lines:
            query = query.lower()

            # parse each query
            conjunctives = query.split(' and ')
            disjunctives = [map(int, A_i.strip('()').split(' or ')) for A_i in conjunctives]

            all_matches = []  # matching pins
            # try searching for each pin_query in a disjunctive element
            for pin_query in disjunctives:
                disjunctive_matches = []

                # figure out which images contain any of the objects
                for pin_id in range(len(pin_lines)):
                    object_ids = map(int, pin_lines[pin_id].split())
                    for object_id in object_ids[1:]:
                        if object_id in pin_query and \
                                pin_id not in disjunctive_matches:  # remove duplicates
                            disjunctive_matches.append(pin_id)
                all_matches.append(disjunctive_matches)

            # apply the conjunctive to each element
            if not all_matches:
                num_matches.append(0)
                continue
            conjunctive_matches = all_matches[0]
            for disjunctive_matches in all_matches[1:]:
                intersection_matches = []
                for pin_id in conjunctive_matches:
                    # only keep pin_id if they've appeared in previous conjunctive
                    if pin_id in disjunctive_matches:
                        intersection_matches.append(pin_id)
                conjunctive_matches = intersection_matches

            num_matches.append(len(conjunctive_matches))

    with open(output_file, 'w') as output_descriptor:
        for num in num_matches:
            output_descriptor.write('%d\n' % num)


if __name__ == '__main__':
    search()
