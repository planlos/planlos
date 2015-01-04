'use strict';

describe('Filter: range', function () {

  // load the filter's module
  beforeEach(module('staticApp'));

  // initialize a new instance of the filter before each test
  var range;
  beforeEach(inject(function ($filter) {
    range = $filter('range');
  }));

  it('should return the input prefixed with "range filter:"', function () {
    var text = 'angularjs';
    expect(range(text)).toBe('range filter: ' + text);
  });

});
