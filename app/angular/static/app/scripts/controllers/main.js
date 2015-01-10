'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('MainCtrl', function ($http, $scope) {
    var respPromise = $http.get('http://'+apiUrl+'/api/events/');

	respPromise.success((function(data, status, headers, config){
		$scope.events = data.events;
		console.log(data);
	}));
  });
