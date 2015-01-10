'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:ToolsCtrl
 * @description
 * # ToolsCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('ToolsCtrl', function ($http, $routeParams, $scope, apiUrl) {
    var cmd = $routeParams['cmd'];
    if(cmd){
    	var respPromise = $http.post('http://'+apiUrl+'/api/tools', {'cmd' : cmd});
    	respPromise.success(function(data){
    		console.log(data);
    	});
    }
  });
