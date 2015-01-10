'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:PlaceCtrl
 * @description
 * # PlaceCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('PlaceCtrl', function ($http, $routeParams, $scope) {
    var placeId = $routeParams['id'];

  	if(placeId){
  		//update event
  		var respPromise = $http.get('http://'+apiUrl+'/api/locations/' + placeId);
  		respPromise.success((function(data, status, headers, config){
		$scope.place = data.location;
			console.log(data);
		}));
  	}
  	else{
	  	$scope.place = {};
	  	//create new event
  	}
  });
