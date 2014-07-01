var Driver = function(element) {
  this.WIDTH = 500;
  this.FLOOR_HEIGHT = 100;

  this.construct = function() {
    this.element = element;
    this.floors = element.find('.floor').length;
    this.elevator = new Elevator(this.floors);
    this.elevatorElement = element.find('#car');
    this.landing = 1;

    // configure dimensions
    var height = this.floors * this.FLOOR_HEIGHT;
    this.element.css({ left: ($(window).width() - this.WIDTH) / 2,
                       top:  ($(window).height() - height) / 2 });
    this.element.css({ width: this.WIDTH, height: height });

    // add external control panels
    this.externalControlPanels = new Array();
    for (var i = 1; i <= this.floors; i++) this.externalControlPanels.push(new ExternalControlPanel(i, this.floorElement(i), this));

    // activate spawn form
    var self = this;
    $('#spawn').submit(function() {
      var origin = parseInt($('[name=origin]').val());
      var dest = parseInt($('[name=destination]').val());
      var confused = $('[name=confused]').val() == 'true';
      new Person(origin, self, dest, confused);
      return false;
    });

    // start randomly instantiating people
    var createPerson = function() {
      if ($('#autospawn')[0].checked)
        new Person(Math.floor(Math.random() * self.floors) + 1, self);
      self.element.oneTime(Math.floor(Math.random() * 5000) + 4000, createPerson);
    };
    createPerson();

    // and run the elevator; 1-second ticks
    var doorsOpen = false;
    this.element.everyTime(1000, function() {
      // handle the open-doors case first
      if (doorsOpen) {
        doorsOpen = false;
        return;
      }

      doorsOpen = self.elevator.arrive(self.landing);
      var dir = self.elevator.direction();
      switch (dir) {
        case "up":
          $('#car-direction').text("⬆"); break;
        case "down":
          $('#car-direction').text("⬇"); break;
        case "stopped":
          $('#car-direction').text("●");
      }

      if (doorsOpen) {
        $('#car-direction').css('color', 'steelblue');
        $(self).trigger('opendoors', [ self.landing, dir ]);
        self.element.oneTime(1000, function() {
          $('#car-direction').css('color', 'gray');
          $(self).trigger('closedoors', [ self.landing, dir ]);
        });
        return;
      }

      // move the elevator to a new landing if necessary
      switch (dir) {
        case "up":
          if (self.landing >= self.floors) throw new Error("Tried to go up past the last landing!");
          self.landing += 1;
          self.elevatorElement.animate({ bottom: '' + ((self.landing - 1) * 100) + 'px' }, 1000, 'linear');
          break;
        case "down":
          if (self.landing <= 1) throw new Error("Tried to go down past the first landing!");
          self.landing -= 1;
          self.elevatorElement.animate({ bottom: '' + ((self.landing - 1) * 100) + 'px' }, 1000, 'linear');
          break;
        case "stopped":
          break;
        default:
          throw new Error("Invalid elevator direction!");
      }
    });
  };

  this.floorElement = function(floor) {
    return this.element.find('#floor' + floor);
  };

  // proxy hallCall to the elevator but trigger events too
  this.hallCall = function(floor, direction) {
    $(this).trigger('hallcall', [ floor, direction ]);
    this.elevator.hallCall(floor, direction);
  };

  this.construct();
};
