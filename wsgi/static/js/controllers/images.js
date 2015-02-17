(function () {
    'use strict';
    var imagesModule = angular.module('rascam.modules.images', ['ui.bootstrap']);

    imagesModule.controller('ImageModalCtrl',
        function ($scope, $http, $modalInstance, selected_image, images) {

        $scope.selected_image = selected_image;
        $scope.images = images;

        $scope.remove_image = function(){
            $http.delete('/api/v1/image/'+$scope.selected_image.id).success(function(data) {
                var index = $scope.images.indexOf($scope.selected_image);
                $scope.next();
                $scope.images.splice(index, 1);
            });
        };
        $scope.next = function(){
            var index = $scope.images.indexOf($scope.selected_image) + 1;
            if (index === $scope.images.length){
                index = 0;
            }
            $scope.selected_image = $scope.images[index];
        }
        $scope.prev = function(){
            var index = $scope.images.indexOf($scope.selected_image) - 1;
            if (index < 0){
                index = $scope.images.length - 1;
            }
            $scope.selected_image = $scope.images[index]
        }
    });

    imagesModule.controller('ImagesListCtrl', ['$scope', '$http','$modal',
        function ($scope, $http, $modal) {
            $scope.load_all = function(){
                $http.get('/api/v1/images').success(function(data) {
                    $scope.images = data.images;
                });
            }

            $scope.load_all();

            $scope.opeImageModal = function (image) {
                var modalInstance = $modal.open({
                       templateUrl: 'static/partials/modal/image_modal.html',
                       controller: 'ImageModalCtrl',
                       resolve: {
                         selected_image: function () {
                            return image;
                         },
                         images : function (){
                            return $scope.images;
                         }
                       }
                 });
                modalInstance.result.then(
                    function (selected_image) {
                       console.log("Image deleted "+selected_image.id);
                    },
                    function () {

                    }
                );
            };
      }]);

})();