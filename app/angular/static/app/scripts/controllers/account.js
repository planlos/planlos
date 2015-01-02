'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:AccountCtrl
 * @description
 * # AccountCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('AccountCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
