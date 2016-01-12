var catalogApp = angular.module('catalogApp', ['ngAnimate','ngRoute', 'mgcrea.ngStrap','satellizer','flow']);

//routes
catalogApp.config(['$routeProvider', 
	function($routeProvider){
		$routeProvider.
			when('/login',{
				templateUrl:'/static/client/components/auth/login.html',
				controller:'authController'
			}).
			when('/', {
				templateUrl:'static/client/components/landing/landing.html',
				controller:'landingCtrl'
			}).
			when('/browse/:categoryId?', {
				templateUrl:'static/client/components/browse/browse.html',
				controller:'browseCtrl'
			}).
			when('/profile', {
				templateUrl:'static/client/components/profile/profile.html',
				controller:'profileCtrl'
			})
			// .otherwise({
			// 	redirectTo: '/'
			// });
	}]);

catalogApp.config(function($httpProvider){
	$httpProvider.defaults.headers.post['Content-Type'] = 'application/json';
})
 
catalogApp.config(function($authProvider){

	$authProvider.google({
		clientId: '540536719213-tiupauupmaf8m8jdho1efdb2dq4e65vq.apps.googleusercontent.com'
	});

	$authProvider.google({
        url: '/api/v1.0/auth/google',
        authorizationEndpoint: 'https://accounts.google.com/o/oauth2/auth',
        redirectUri: window.location.origin || window.location.protocol + '//' + window.location.host,
        requiredUrlParams: ['scope'],
        optionalUrlParams: ['display'],
        scope: ['profile', 'email'],
        scopePrefix: 'openid',
        scopeDelimiter: ' ',
        display: 'popup',
        type: '2.0',
        popupOptions: {width: 452, height: 633}
    });

})