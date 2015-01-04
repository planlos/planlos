'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:EventCtrl
 * @description
 * # EventCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('EventCtrl', function ($http, $routeParams, $scope) {
  	var eventId = $routeParams['id'];

    $scope.dateOptions = {
        yearRange: '2015:-0',
        regional: "de"
    };

  	if(eventId){
  		//update event
  		var respPromise = $http.get('http://localhost:5000/api/events/' + eventId);
  		respPromise.success((function(data, status, headers, config){
		$scope.event = data;
			console.log(data);
		}));
  	}
  	else{
	  	$scope.event = {};
	  	//create new event
  	}

  });
