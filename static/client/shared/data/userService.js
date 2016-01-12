catalogApp.factory('userService', ['$http',
	function($http){
		// var categories =[
		//     {
		//         'id': 1,
		//         'name': 'Sports Equipment',
		//         'description': 'Equipment for all different kinds of sports.'
		//     },
		//     {
		//         'id': 2,
		//         'title': 'Computer Hardware',
		//         'description': 'All kinds of hardware for computers: PSU, GPU, CPU, SSD, HDD, etc.'
		//     }
		// ]

		var service = {};
		var baseURL = '/api/v1.0';
		service.getUser = function(id) {
			return $http.get(baseURL+'/user/'+id).then(function(response){
				return response.data;
			}, function(err){
				return err
			});
		}

		return service;
	}]);

// curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:8000/api/v1.0/categories/
