catalogApp.controller('profileCtrl', ['$scope','$auth','$modal','$http','userService', 'itemService', 'categoryService','$route', '$location',
	function($scope,$auth,$modal,$http, userService, itemService, categoryService, $route, $location){
		if($auth.getPayload() == null){
			alert('Please login first.');
			$location.path('/');
			return;
		}

		categoryService.getAllCategories().then(function(data){
			$scope.categories = data.categories;
		}, function(err) {
			console.log(err)
		});

		$scope.getCategoryName = function(id) {
		  for (var i = 0; i < $scope.categories.length; i++) {
		    if ($scope.categories[i]['id'] === id) {
		      return $scope.categories[i]['name'];
		    }
		  }
		  return null;
		}

		// Pre-fetch an external template populated with a custom scope
		var myOtherModal = $modal({scope: $scope, templateUrl: '/static/client/components/profile/new_item_form.html', show: false});
		// Show when some event occurs (use $promise property to ensure the template has been loaded)
		$scope.showModal = function() {
		  myOtherModal.$promise.then(myOtherModal.show);
		};

		var editModal = $modal({scope: $scope, templateUrl: '/static/client/components/profile/edit_item_form.html', show: false});
		$scope.showEditModal = function(item_id){
			itemService.getItem(item_id).then(function(data){
				console.log(data.item)
				$scope.editingItem = data.item;
				$scope.editingItem.category_name = $scope.getCategoryName(data.item.category_id)
				editModal.$promise.then(editModal.show);
			}, function(err) {
				console.log(err)
			});;
		}

		$scope.formData = {
			name: 'enter a name',
			price: 50,
			description: 'desc',
			owner_id: $auth.getPayload().sub,
			category_name: 'test category',
			image: ''
		};

		userService.getUser($auth.getPayload().sub).then(function(data){
			$scope.user = data.user;
			$scope.myListings = data.items;
		}, function(err) {
			console.log(err)
		});

		// itemService.getMyListings($auth.getPayload().sub).then(function(data){
		// 	$scope.myListings = data.items;
		// }, function(err) {
		// 	console.log(err)
		// });
		$scope.delete = function(id){
			itemService.deleteItem(id).then(function(data){
				alert(data);
				$route.reload();			
			}, function(err) {
				console.log(err)
			});
		}

		$scope.processForm = function(){
			itemService.addListing($scope.formData).then(function(data){
				console.log(data.data)
			}, function(err) {
				console.log(err)
			});
			myOtherModal.$promise.then(myOtherModal.hide);
			$route.reload();
		}

		$scope.processEditForm = function(){
			itemService.updateItem($scope.editingItem).then(function(response){
				console.log(response)
			}, function(err) {
				console.log(err)
			});;
			editModal.$promise.then(editModal.hide);
			$route.reload();
		}
		// $scope.uploader = {}
		// $scope.upload = function () {
		//   $scope.uploader.flow.upload();  
		  
		// }
		// $scope.$on('flow::fileAdded', function (event, $flow, flowFile) {
		//   console.log(flowFile)
		// });


	}])