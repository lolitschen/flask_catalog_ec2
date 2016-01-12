catalogApp.controller('headerCtrl', ['$scope','$location','$auth','$route','categoryService', '$modal',
	function($scope, $location, $auth, $route, categoryService, $modal){

		// categoryService.getAllCategories(function(data) {
		// 	$scope.categories = data;
		// });
		$scope.isAuthenticated = $auth.isAuthenticated();
		$scope.userID = $auth.getPayload();

		$scope.selectedCategory = {name: "All"};
		$scope.select = function(cat){
			$scope.selectedCategory = cat;
			console.log($scope.selectedCategory);
		}

		categoryService.getAllCategories().then(function(data){
			$scope.categories = data;
		}, function(err) {
			console.log(err)
		});

		// .then(function(data){
		// 	$scope.categories = data;
		// 	console.log(data)
		// })
		$scope.go = function ( path ) {
		  console.log(path);
		  $location.path( path );
		};

		$scope.logout = function() {
		  $auth.logout();
		  $location.path('/');
		  $route.reload();
		  alert('you have successfully logged out!');
		};

		$scope.authenticate = function(provider) {
		  $auth.authenticate(provider).then(function(response){
		  	console.log('success!!');
		  	loginModal.$promise.then(loginModal.hide);
		  	$location.path('/');
		  }, function (err){
		  	console.log(err);
		  })
	  	};

	  	// Pre-fetch an external template populated with a custom scope
		var loginModal = $modal({scope: $scope, templateUrl: '/static/client/shared/header/login_modal.html', show: false});
		// Show when some event occurs (use $promise property to ensure the template has been loaded)
		$scope.showLogin = function() {
		  loginModal.$promise.then(loginModal.show);
		};


	}])