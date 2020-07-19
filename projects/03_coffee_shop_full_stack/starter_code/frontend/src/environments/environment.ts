/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffee-silo.au', // the auth0 domain prefix
    audience: 'coffee-silo', // the audience set for the auth0 app
    clientId: 'sfuFrJY2mOQ0wULfuxc9TXkTM0hwbA0r', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
