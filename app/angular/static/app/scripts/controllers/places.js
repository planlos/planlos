'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:PlacesCtrl
 * @description
 * # PlacesCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('PlacesCtrl', function ($scope, $http, apiUrl) {
  		var respPromise = $http.get('http://'+apiUrl+'/api/locations/');

  		respPromise.success((function(data, status, headers, config){
  			$scope.places = data.locations;
  			console.log(data);
  		}));
  });
