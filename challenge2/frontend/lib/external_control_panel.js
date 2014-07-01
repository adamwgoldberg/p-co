var ExternalControlPanel = function(floor, element, driver) {
  this.construct = function() {
    this.driver = driver;
    this.element = element;
    this.floor = floor;

    var self = this;
    $(this.driver).bind('hallcall', function(_, floor, direction) {
      if (floor != self.floor) return;
      self.light(direction);
    });

    $(this.driver).bind('opendoors', function(_, landing, direction) {
      if (landing != self.floor) return;
      self.unlight(direction);
    });
  };

  this.light = function(direction) {
    if (direction == "up") this.element.find('.call-up').addClass('call-active');
    if (direction == "down") this.element.find('.call-down').addClass('call-active');
  };

  this.unlight = function(direction) {
    if (direction == "up" || direction == "stopped") this.element.find('.call-up').removeClass('call-active');
    if (direction == "down" || direction == "stopped") this.element.find('.call-down').removeClass('call-active');
  };

  this.construct();
};
