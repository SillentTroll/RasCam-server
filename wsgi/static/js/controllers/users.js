(function () {
    'use strict';

    var usersModule = angular.module('rascam.modules.users', ['rascam.modules.auth']);

    usersModule.controller('LoginCtrl', ['$scope', '$location', '$http', 'AuthenticationService',
      function ($scope, $location, $http, AuthenticationService) {
            $http.get('/users/configured')
                .success(function (data){
                   if (data.result === "NOK"){
                        $location.path('/users/configure');
                        return;
                   }
                })
                .error(function(data){
                    $scope.error = "Servers is unavailable."
                    return;
                });
            AuthenticationService.clearCredentials();
            this.email = '';
            this.password = '';
            $scope.login = function(){
                AuthenticationService.login(this.email,this.password, function(email, response) {
                   AuthenticationService.setCredentials(email, response.token);
                   $location.path('/');
               },
               function (response){
                  if(response.message){
                    $scope.error = response.message;
                  } else if (response.description){
                    $scope.error = response.description;
                  }
               });
            }
      }]);

    usersModule.controller('NavController', ['$scope', '$location', 'AuthenticationService','$window',
      function ($scope, $location, AuthenticationService, $window) {
            this.hasToken = $window.sessionStorage.token;
            $scope.logout = function(){
                console.log("User is out")
                AuthenticationService.clearCredentials();
                $location.path('/');
            }
            $scope.isActive = function (viewLocation) {
                return viewLocation === $location.path();
            };
      }]);

    usersModule.controller('RegisterAdminCtrl', ['$scope', '$http','$location',
      function ($scope, $http, $location) {
            $http.get('/users/configured')
              .success(function (data){
                 if (data.result === "OK"){
                      $location.path('/users/login');
                 }
              })
              .error(function(data){
                  $scope.error = "Servers is unavailable."
                  return;
              });
            $scope.title = "You should configure the administrator";
            this.user = {};
            this.register = function(user){
                  var payload = {
                        'email': user.email,
                        'password' : user.password,
                        'password_confirm' : user.password_confirm
                  };
                  $http.put('/api/v1/users/register', payload)
                    .success(function(data){
                          $location.path('/users/login');
                          this.user = {};
                    })
                    .error(function (data){
                        $scope.error = data.message;
                    });
            };
      }]);

})();