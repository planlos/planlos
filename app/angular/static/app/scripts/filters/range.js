'use strict';

/**
 * @ngdoc filter
 * @name staticApp.filter:range
 * @function
 * @description
 * # range
 * Filter in the staticApp.
 */
angular.module('staticApp')
  .filter('range', function() {
	  return function(input, total) {
	    total = parseInt(total);
	    for (var i=0; i<total; i++)
	      input.push(i);
	    return input;
	  };
  });
