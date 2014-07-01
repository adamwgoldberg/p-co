var Soundtrack = function(driver) {
  this.constructor = function() {
    this.driver = driver;
    $(this.driver).bind('opendoors', function() { $('#open')[0].play(); });
    //$(this.driver).bind('closedoors', function() { $('#close')[0].play(); });
    $(this.driver).bind('hallcall', function() { $('#ding')[0].play(); });
  };

  this.constructor();
};
