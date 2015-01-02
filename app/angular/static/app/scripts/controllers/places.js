'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:PlacesCtrl
 * @description
 * # PlacesCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('PlacesCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
