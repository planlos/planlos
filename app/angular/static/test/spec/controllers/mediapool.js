'use strict';

describe('Controller: MediapoolCtrl', function () {

  // load the controller's module
  beforeEach(module('staticApp'));

  var MediapoolCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MediapoolCtrl = $controller('MediapoolCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
