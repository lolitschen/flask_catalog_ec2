catalogApp.controller('browseCtrl', ['$scope', '$routeParams','$location', 'categoryService','userService', '$auth', 'itemService','$route','$filter', 
	function($scope, $routeParams, $location, categoryService, userService, $auth, itemService, $route, $filter){

		$scope.categoryId = $routeParams.categoryId;



		if($scope.categoryId) {$scope.browseAll = false;}
		else {$scope.browseAll = true;}

		if($auth.getPayload() != null) {
			$scope.userID = $auth.getPayload().sub;
			userService.getUser($auth.getPayload().sub).then(function(data){
				$scope.user = data;
			}, function(err) {
				console.log(err)
			});
		}

		$scope.numItemsWithCurrentCategoryID = function(id){
		  var count = 0;
		  angular.forEach($scope.items, function(obj, key) {
		  	if(id == obj.category_id) count +=1;
		  });
		  return count;
		}


		categoryService.getAllCategories().then(function(data){
			$scope.categories = data;
		}, function(err) {
			console.log(err)
		});

		itemService.getAllItems().then(function(data){
			$scope.items = data.items;
		}, function(err) {
			console.log(err)
		});


		$scope.edit = function(id){
			itemService.updateItem(id,id).then(function(data){
				alert(data)			
			}, function(err) {
				console.log(err)
			});
		}

		$scope.delete = function(id){
			itemService.deleteItem(id).then(function(data){
				alert(data)
				$route.reload()		
			}, function(err) {
				console.log(err)
			});
		}


		// $scope.items = [
		// 	{
		// 		id: 1,
		// 		name: 'Burton Snowboard',
		// 		desc: 'This is an item description',
		// 		category_id: 1,
		// 		owner: 'Chen',
		// 		price: 150
		// 	},
		// 	{
		// 		id: 2,
		// 		name: 'Burton Snowboard Type #2',
		// 		desc: 'This is an item description',
		// 		category_id: 1,
		// 		owner: 'Chen',
		// 		price: 150
		// 	},
		// 	{
		// 		id: 3,
		// 		name: 'Burton Ski',
		// 		desc: 'This is an item description',
		// 		category_id: 2,
		// 		owner: 'Aleka',
		// 		price: 150
		// 	},
		// 	{
		// 		id: 4,
		// 		name: 'Burton Ski Type #2',
		// 		desc: 'This is an item description',
		// 		category_id: 2,
		// 		owner: 'Aleka',
		// 		price: 250
		// 	},
		// ]

		$scope.go = function ( path ) {
		  console.log(path);
		  $location.path( path );
		};

	}]);


