'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:UsersCtrl
 * @description
 * # UsersCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('UsersCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
