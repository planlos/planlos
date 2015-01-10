'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:DatesCtrl
 * @description
 * # DatesCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('EventsCtrl', function ($http, $scope, apiUrl) {
  	var respPromise = $http.get('http://'+apiUrl+'/api/events/');

	respPromise.success((function(data, status, headers, config){
		$scope.events = data.events;
		console.log(data);
	}));
  });
