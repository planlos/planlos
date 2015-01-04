'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:DatesCtrl
 * @description
 * # DatesCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('EventsCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
