'use strict';

describe('Controller: BugsCtrl', function () {

  // load the controller's module
  beforeEach(module('staticApp'));

  var BugsCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    BugsCtrl = $controller('BugsCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
