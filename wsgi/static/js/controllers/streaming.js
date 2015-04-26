(function () {
    'use strict';
    var streamingModule = angular.module('rascam.modules.streaming', []);

    streamingModule.controller('StreamsListCtrl', ['$scope', '$http',
      function ($scope, $http) {
            $scope.load_all = function(){
                $http.get('/api/v1/streams').success(function(data) {
                    $scope.cameras = data.cameras;
                });
            }

            this.change_state = function(camera_id){
                $http.post('/api/v1/cam/'+camera_id+'/state').success(function(){
                    $scope.load_all();
                });
            };

            $scope.load_all();
      }]);

})();