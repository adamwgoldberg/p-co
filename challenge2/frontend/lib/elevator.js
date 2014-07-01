/**
 * Handler for the elevator object. The Driver will actually move the elevator
 * div around the page; this class encapsulates the behavior of the elevator.
 * It receives three different methods when different events occur (arrive,
 * hallCall, and carCall), and is responsible for tracking its own internal
 * state. The only state it exposes is its current direction, which can be "up",
 * "down", or "stopped". The Driver uses this information to manage the elevator
 * div.
 *
 * For all methods, floors are assumed to start at 1. The constructor receives
 * a number equal to the top floor (or the total number of floors). It can be
 * assumed that the elevator is initialized on the first floor.
 *
 * Passengers will typically press the correct hall button depending on the floor
 * they intend to go to. Some "confused" passengers will press the incorrect
 * hall button (they will have a question mark in their speech bubble). No
 * passenger will ever intend to go to the floor they are currently on.
 **/

var Elevator = function(landings) {

  $.ajax({
           type:  'GET',
           async: false,
           url:   'http://localhost:3130/reset',
           data:  $.param({landings: landings})
         });

  /**
   * Called when an elevator arrives at a floor, or passes through a floor.
   * This method should return true if the elevator should stop and open its
   * doors, or false if the elevator should continue past the floor.
   **/

  this.arrive = function(landing) {
    var response = $.ajax({
                            type:  'GET',
                            async: false,
                            url:   'http://localhost:3130/arrive',
                            data:  $.param({landing: landing})
                          }).responseText;
    if (response === 'true') return true;
    else if (response === 'false') return false;
    else throw new Error("Invalid response from arrive: " + response);
  };

  /**
   * Called when someone outside the elevator presses a call button. Receives
   * the floor on which the button was pressed, and "up" or "down" depending
   * on which button was pressed. It can be assumed that this method will
   * never be called with the bottom floor and "down", or the top floor and
   * "up". The return value is ignored.
   **/

  this.hallCall = function(landing, direction) {
    $.ajax({
             type:  'GET',
             async: false,
             url:   'http://localhost:3130/hallcall',
             data:  $.param({landing: landing, direction: direction})
           });
  };

  /**
   * Called when someone inside the elevator presses a floor button. The return
   * value is ignored. You can, but do not need to, handle the case where
   * someone calls the floor they are currently on.
   **/

  this.carCall = function(landing) {
    $.ajax({
             type:  'GET',
             async: false,
             url:   'http://localhost:3130/carcall',
             data:  $.param({landing: landing})
           });
  };

  /**
   * This method should return the current elevator direction: "up", "down",
   * or "stopped". The Driver uses this to properly animate the elevator.
   **/

  this.direction = function() {
    var response = $.ajax({
                            type:  'GET',
                            async: false,
                            url:   'http://localhost:3130/direction'
                          }).responseText;
    if (['up', 'down', 'stopped'].indexOf(response) >= 0) return response;
    else throw new Error("Invalid response from direction: " + response);
  };
};
