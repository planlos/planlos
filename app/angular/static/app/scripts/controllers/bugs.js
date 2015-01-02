'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:BugsCtrl
 * @description
 * # BugsCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('BugsCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
