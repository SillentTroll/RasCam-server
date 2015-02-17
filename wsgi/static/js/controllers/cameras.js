(function () {
    'use strict';
    var camerasModule = angular.module('rascam.modules.cameras', []);

    camerasModule.controller('CamListCtrl', ['$scope', '$http',
      function ($scope, $http) {
            $scope.load_all = function(){
                $http.get('/api/v1/cam').success(function(data) {
                    $scope.cameras = data.cameras;
                });
            }

            this.change_state = function(camera_id){
                $http.post('/api/v1/cam/'+camera_id+'/state').success(function(){
                    //create an simple notification
                    $scope.load_all();
                });
            };

            this.remove_camera = function(camera_name,camera_id){
                bootbox.dialog({
                  message: "<h4>Are you sure you want to permanently remove the <strong>" + camera_name + "</strong> camera?<h4>",
                  size:"small",
                  buttons: {
                    success: {
                      label: "Cancel",
                      className: "btn-default",
                      callback: function() {

                      }
                    },
                    danger: {
                      label: "Remove",
                      className: "btn-danger",
                      callback: function() {
                          $http.delete('/api/v1/cam/'+camera_id).success(function(){
                                  //create an simple notification
                              $scope.load_all();
                          });
                      }
                    },
                  }
                });
            }

            $scope.load_all();
      }]);

})();