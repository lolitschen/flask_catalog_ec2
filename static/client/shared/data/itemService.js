catalogApp.factory('itemService', ['$http',
	function($http){

		var service = {};
		var baseURL = '/api/v1.0';
		service.addListing = function(data) {
			return $http.post(baseURL+'/item/', data).then(function(response){
				console.log(response);
				return response;
			}, function(err){
				return err
			});
		}

		service.getItem = function(id){
			return $http.get(baseURL+'/item/'+id + '/').then(function(response){
				return response.data;
			}, function(err){
				return err
			});
		}

		service.updateItem = function(item){
			console.log(item)
			return $http.put(baseURL+'/item/'+item.id+'/', item).then(function(response){
				return response.data
			}, function(err) {
				console.log(err)
			});
		}

		service.deleteItem = function(id){
			return $http.delete(baseURL+'/item/'+id+'/').then(function(response){
				return response.data
			}, function(err) {
				console.log(err)
			});
		}

		service.getAllItems = function() {
			return $http.get(baseURL+'/item/').then(function(response){
				return response.data;
			}, function(err){
				return err
			});
		}


		return service;
	}]);

// curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:8000/api/v1.0/categories/
