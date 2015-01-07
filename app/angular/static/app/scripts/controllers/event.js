'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:EventCtrl
 * @description
 * # EventCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('EventCtrl', function ($q, $http, $routeParams, $scope) {
  	var eventId = $routeParams['id'];

  	var EVENT = 'event';
  	var LOCATIONS = 'locations';

    $scope.dateOptions = {
        yearRange: '2015:-0',
        regional: "de"
    };

  	if(eventId){
  		//update event
  		var eventsPromise = $http.get('http://192.168.1.41:5000/api/events/' + eventId, {key: EVENT});
  		var locationsPromise = $http.get('http://192.168.1.41:5000/api/locations/', {key: LOCATIONS});

  		/*$q.all([eventsPromise, locationsPromise]).then(function(result){
  			var tmp = [];
  			console.log(result);
  			angular.forEach(result, function(response){

  			});
  		})*/
  		eventsPromise.success(
        function(data, status, headers, config){
		      $scope.event = data;
		    }
    	);
		locationsPromise.success(
        function(data, status, headers, config){
		      $scope.locations = data.locations;
		    }
    	);
  	}
  	else{
	  	$scope.event = {};
	  	var locationsPromise = $http.get('http://192.168.1.41:5000/api/locations/');
	  	//create new event
  	}

  	$scope.saveEvent = function(){
  		var eventsPromise = $http.post('http://192.168.1.41:5000/api/events/' + $scope.event.id, $scope.event);
  		eventsPromise.success(
  			function(data, status, headers, config){
		      console.log(data);
		    }
  		);
  	}

  });
