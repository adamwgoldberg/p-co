# Handler for the elevator object. The front-end will actually move the elevator
# div around the page; this class encapsulates the behavior of the elevator.
# It receives three different methods when different events occur (arrive,
# hall_call, and car_call), and is responsible for tracking its own internal
# state. The only state it exposes is its current direction, which can be "up",
# "down", or "stopped". The front-end uses this information to manage the
# elevator div.
#
# For all methods, floors are assumed to start at 1. The initializer receives
# a number equal to the top floor (or the total number of floors). It can be
# assumed that the elevator is initialized on the first floor.
#
# Passengers will typically press the correct hall button depending on the floor
# they intend to go to. Some "confused" passengers will press the incorrect
# hall button (they will have a question mark in their speech bubble). No
# passenger will ever intend to go to the floor they are currently on.

from collections import defaultdict

class Elevator(object):
  def __init__(self, landings):
    # (floor, direction) => count
    self.people = defaultdict(int)
    self.schedule = []
    self.dir = "up" # or "stopped" or "down" - internal state for arrival decisions
    self.floor = 1 # replicate for internal usage

  # Called when an elevator arrives at a floor, or passes through a floor.
  # This method should return true if the elevator should stop and open its
  # doors, or false if the elevator should continue past the floor.

  def arrive(self, landing):
    # Update floor
    self.floor = landing

    # If it's scheduled, stop
    if landing in self.schedule:
      self.schedule.remove(landing)
      self.clean_floor(landing)
      return True

    # If we are going up, and people on this floor want to go up
    if self.dir is "up" and self.people[(landing, "up")] > 0:
      self.clean_floor(landing)
      return True

    # If wea re going down and people on this floor want to go down
    if self.dir is "down" and self.people[(landing, "down")] > 0:
      self.clean_floor(landing)
      return True

    # Nobody should get on
    return False

  def clean_floor(self, landing):
    self.dir = "stopped"
    self.people[(landing, 'up')] = 0
    self.people[(landing, 'down')] = 0

  # Called when someone outside the elevator presses a call button. Receives
  # the floor on which the button was pressed, and "up" or "down" depending
  # on which button was pressed. It can be assumed that this method will
  # never be called with the bottom floor and "down", or the top floor and
  # "up". The return value is ignored.

  def hall_call(self, landing, direction):
    # Update people map
    self.people[(landing, direction)] += 1

    # Add to schedule
    if landing not in self.schedule:
      self.schedule.append(landing)

  # Called when someone inside the elevator presses a floor button. The return
  # value is ignored. You can, but do not need to, handle the case where
  # someone calls the floor they are currently on.

  def car_call(self, landing):
    # Add to schedule
    if landing not in self.schedule:
      self.schedule.append(landing)

  # This method should return the current elevator direction: "up", "down",
  # or "stopped". The front-end uses this to properly animate the elevator.

  def direction(self):
    # If nobody wants to go anywhere, don't go anywhere
    if len(self.schedule) == 0:
      self.dir = 'stopped'
      return "stopped"

    # Go up if you need to
    if self.schedule[0] > self.floor:
      self.dir ='up'
      return "up"

    # Go down if you need to
    if self.schedule[0] < self.floor:
      self.dir = 'down'
      return "down"
