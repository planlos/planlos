'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:EventCtrl
 * @description
 * # EventCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('EventCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

    $scope.dateOptions = {
        yearRange: '2015:-0',
        regional: "de"
    };

  });
