catalogApp.controller('landingCtrl', ['$scope',
	function($scope){
		$scope.test = "testing";

		$scope.popularimages = [{id: 1, name:'item name', url:'http://placehold.it/200x200'},{id: 2, name:'item name', url:'http://placehold.it/200x200'},{id: 3, name:'item name', url:'http://placehold.it/200x200'},{id: 4, name:'item name', url:'http://placehold.it/200x200'}]
		
		$scope.recentAdditions = [{id:1, name:'burton snwoboard 1', category:'snowboard', cost:'150'},{id:2, name:'burton ski 1', category:'ski', cost:'125'}]

	}])