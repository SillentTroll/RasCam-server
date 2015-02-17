(function(){
    'use strict';
      
    var authModule = angular.module('rascam.modules.auth',[]);
      
    authModule.factory('AuthenticationService',
        ['$http', '$rootScope', '$timeout','$window',
        function ($http, $rootScope, $timeout, $window) {
            var service = {};
     
            service.login = function (email, password, callback, error_callback) {
      
                $http.post('/api/v1/users/auth', { username: email, password: password })
                    .success(function (response) {
                        callback(email, response);
                    })
                    .error(function(response){
                       delete $window.sessionStorage.token;
                       error_callback(response);
                    });       
            };
      
            service.setCredentials = function (username, token) {
                $window.sessionStorage.token = token;
                $window.sessionStorage.username = username;
            };
      
            service.clearCredentials = function () {
                delete $window.sessionStorage.token;
                delete $window.sessionStorage.username;
            };
      
            return service;
        }])

})();