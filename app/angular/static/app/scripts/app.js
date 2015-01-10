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
    'ngTouch',
    'ui.date'
  ])
  .constant('apiUrl', 'localhost:5000')
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/events', {
        templateUrl: 'views/events.html',
        controller: 'EventsCtrl'
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
      .when('/tools/:cmd', {
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
      .when('/event', {
        templateUrl: 'views/event.html',
        controller: 'EventCtrl'
      })
      .when('/event/:id', {
        templateUrl: 'views/event.html',
        controller: 'EventCtrl'
      })
      .when('/place', {
        templateUrl: 'views/place.html',
        controller: 'PlaceCtrl'
      })
      .when('/place/:id', {
        templateUrl: 'views/place.html',
        controller: 'PlaceCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
