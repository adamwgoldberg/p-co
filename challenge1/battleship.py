import urllib2
import json

base_url = 'https://student.people.co/api/challenge/battleship/972b28c2e435/'

already_hit = set()

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

def solve_all():
    #query = base_url + 'boards'
    #response = urllib2.urlopen(query)
    #data = json.load(response)
    #boards = [str(d['board_id']) for d in data]
    # Uncomment above
    boards = ['live_board_5']
    print boards
    for board in boards:
        print 'Solving board', board
        solve(board)

def solve(board_id):
    already_hit = set()
    print 'Starting hunting phase for board', board_id
    targets = hunt(board_id)
    print 'Starting targeting phase for board', board_id
    target(board_id, targets)
    print 'Solved board', board_id

# Hit every other square A1, A3, ...
def hunt(board_id):

    red = ['A1', 'A3', 'A5', 'A7', 'A9', \
           'B2', 'B4', 'B6', 'B8', 'B10', \
           'C1', 'C3', 'C5', 'C7', 'C9', \
           'D2', 'D4', 'D6', 'D8', 'D10', \
           'E1', 'E3', 'E5', 'E7', 'E9', \
           'F2', 'F4', 'F6', 'F8', 'F10',\
           'G1', 'G3', 'G5', 'G7', 'G9', \
           'H2', 'H4', 'H6', 'H8', 'H10',  \
           'I1', 'I3', 'I5', 'I7', 'I9', \
           'J2', 'J4', 'J6', 'J8', 'J10']

    hits = set()

    for sq in red:
        already_hit.add(sq)

        query = base_url + 'boards/' + board_id + '/' + sq
        response = urllib2.urlopen(query)
        data = json.load(response)

        is_it_hit = "No"
        if data['is_hit']:
            hits.add(sq)
            is_it_hit = "Yes"

        print 'Board:' , board_id, 'attacking: ', sq, 'result:', is_it_hit

    print 'Hits:', len(hits)
    return hits

def target(board_id, targets):
    for target in targets:
        print 'Eliminating:', target, 'on board', board_id
        eliminate(board_id, target)

# Returns when ship is eliminated
def eliminate(board_id, target):
    letter = target[0]
    num = int(target[1])

    # above
    above = None
    above_letter = chr(ord(letter) - 1)
    if above_letter in chars:
        above = above_letter + str(num)

    # below
    below=None
    below_letter = chr(ord(letter) + 1)
    if below_letter in chars:
        below = below_letter + str(num)

    # right
    right = None
    right_num = num + 1
    if right_num <= 10:
        right = letter + str(right_num)

    # left
    left = None
    left_num = num - 1
    if left_num > 0:
        left = letter + str(left_num)

    squares = [above, below, right, left]
    next_square = None
    for sq in squares:
      if sq is None: continue
      if sq not in already_hit:
          already_hit.add(sq)
          query = base_url + 'boards/' + board_id + '/' + sq
          response = urllib2.urlopen(query)
          data = json.load(response)
          if data['sunk'] != None:
              print 'Board', board_id, 'sunk', data['sunk']
              return 1
          if data['is_hit']:
              if eliminate(board_id, sq) == 1:
                  return 1

    return 0
