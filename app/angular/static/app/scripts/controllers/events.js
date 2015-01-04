'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:DatesCtrl
 * @description
 * # DatesCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('EventsCtrl', function ($http, $scope) {
  	var respPromise = $http.get('http://localhost:5000/api/events/');

	respPromise.success((function(data, status, headers, config){
		$scope.events = data.events;
		console.log(data);
	}));
  });
