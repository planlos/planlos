'use strict';

/**
 * @ngdoc overview
 * @name staticApp
 * @description
 * # staticApp
 *
 * Main module of the application.
 */
angular
  .module('staticApp', [
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/dates', {
        templateUrl: 'views/dates.html',
        controller: 'DatesCtrl'
      })
      .when('/places', {
        templateUrl: 'views/places.html',
        controller: 'PlacesCtrl'
      })
      .when('/mediapool', {
        templateUrl: 'views/mediapool.html',
        controller: 'MediapoolCtrl'
      })
      .when('/tools', {
        templateUrl: 'views/tools.html',
        controller: 'ToolsCtrl'
      })
      .when('/account', {
        templateUrl: 'views/account.html',
        controller: 'AccountCtrl'
      })
      .when('/bugs', {
        templateUrl: 'views/bugs.html',
        controller: 'BugsCtrl'
      })
      .when('/users', {
        templateUrl: 'views/users.html',
        controller: 'UsersCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
