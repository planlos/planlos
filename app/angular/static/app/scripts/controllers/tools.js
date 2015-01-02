'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:ToolsCtrl
 * @description
 * # ToolsCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('ToolsCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
