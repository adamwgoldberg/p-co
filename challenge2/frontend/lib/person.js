var Person = function(floor, driver, dest, confused) {
  this.construct = function() {
    this.driver = driver;

    this.floor = floor;
    this.destination = dest || (Math.floor(Math.random() * (this.driver.floors - 1)) + 1);
    if (this.floor == this.destination) this.destination++;
    this.direction = (this.destination > this.floor ? "up" : "down");
    this.confused = confused === undefined ? (this.floor > 1 && this.floor < this.driver.floors && Math.random() > 0.75) : confused;

    this.element = $('<img/>').attr({
                                      src: 'men/man' + (Math.floor(Math.random() * 9) + 1) + '.png'
                                    }).appendTo(this.driver.floorElement(this.floor));

    this.setState('waiting');

    // create a callback for when we arrive at our desired floor or when it's time to board
    var self = this;
    this.handler = function(_, landing, direction) {
      if (landing == self.floor && (self.confused || direction == self.direction || direction == "stopped") && self.state == 'waiting')
        self.board();
      else if (landing == self.destination && self.state == 'boarded')
        self.arrive();
    };
    $(this.driver).bind('opendoors', this.handler);

    // pause, then call the elevator
    this.element.oneTime(527, function() {
      var dir = self.direction;
      if (self.confused) dir = (self.direction == "up" ? "down" : "up");
      self.driver.hallCall(self.floor, dir);
    });
  };

  this.arrive = function() {
    // disembark
    this.driver.floorElement(this.destination).append(this.element);
    this.setState('arrived');

    // hang around a bit, then get vaporized
    var self = this;
    this.element.oneTime(1876, function() {
      self.element.fadeOut(300, function() { self.element.remove(); });
    });

    $(this.driver).unbind(this.trigger, this.handler);
  };

  this.board = function() {
    this.driver.elevatorElement.append(this.element);
    this.setState('boarded');

    var self = this;
    this.element.oneTime(113, function() {
      self.driver.elevator.carCall(self.destination);
    });
  };

  this.setState = function(state) {
    this.state = state;
    this.element.attr('alt', '' + this.destination + (this.confused ? '?' : ''));
    this.element.qtip({
                        content:  { attr: 'alt' },
                        show:     { ready: true, event: false },
                        position: { target: this.element, my: 'bottom center', at: 'top center' },
                        style:    { classes: "ui-tooltip-blue ui-tooltip-shadow" }
                      });
    var self = this;
    this.element.everyTime(100, function() { self.element.qtip('reposition'); });
  };

  this.construct();
};
