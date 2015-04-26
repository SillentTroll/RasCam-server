(function () {
    'use strict';
    var app = angular.module('pycamServerApp', ['ngRoute',
                                                'rascam.modules.cameras',
                                                'rascam.modules.images',
                                                'rascam.modules.users',
                                                'rascam.modules.auth',
                                                'rascam.modules.streaming',
                                                'angular.filter']);

    app.config(['$routeProvider','$locationProvider',
            function($routeProvider,$locationProvider) {
                $routeProvider
                    .when('/', {
                        templateUrl: 'static/partials/images.html',
                        controller: 'ImagesListCtrl'
                    }).when('/cameras', {
                        templateUrl: 'static/partials/cameras.html',
                        controller: 'CamListCtrl'
                    }).when('/streaming', {
                        templateUrl: 'static/partials/streaming.html',
                        controller: 'StreamsListCtrl'
                    }).when('/users/login', {
                        templateUrl: 'static/partials/login.html',
                        controller: 'LoginCtrl'
                    }).when('/users/configure', {
                        templateUrl: 'static/partials/register.html',
                        controller: 'RegisterAdminCtrl'
                    }).otherwise({
                        redirectTo: '/'
                    });
                $locationProvider.html5Mode(true);
            }]);

    app.factory('authInterceptor', function ($rootScope, $q, $window, $location) {
      return {
        request: function (config) {
          config.headers = config.headers || {};
          if ($window.sessionStorage.token) {
            config.headers.Authorization = 'Bearer ' + $window.sessionStorage.token;
          }
          return config;
        },
        response: function (response) {
          if (response.status === 401||
                (response.status === 400 && response.data.error==='Invalid JWT')) {
                delete $window.sessionStorage.token;
                $location.path('/users/login');
          }
          return response || $q.when(response);
        },
        responseError: function(response) {
            if(response.status === 401 ||
                (response.status === 400 && response.data.error==='Invalid JWT')) {
                delete $window.sessionStorage.token;
                $location.path('/users/login');
            }
            return $q.reject(response);
        }
      };
    });

    app.config(function ($httpProvider) {
        $httpProvider.interceptors.push('authInterceptor');
    });

    app.run(['$rootScope','$location', '$window',
        function ( $rootScope, $location, $window) {
            $rootScope.$on('$locationChangeStart', function (event, next, current) {
                // redirect to login page if not logged in
                if ($location.path() !== '/users/login'
                    && $location.path() !== '/users/configure'
                    && !$window.sessionStorage.token) {
                     $location.path('/users/login');
                }
            });
    }]);

})();

