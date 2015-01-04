'use strict';

describe('Controller: PlaceCtrl', function () {

  // load the controller's module
  beforeEach(module('staticApp'));

  var PlaceCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    PlaceCtrl = $controller('PlaceCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
