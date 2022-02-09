import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, compose, applyMiddleware, combineReducers } from 'redux';
import { Provider } from 'react-redux';
import thunk from 'redux-thunk';
import App from './App';
import * as serviceWorker from './serviceWorker';
import './index.css'

import 'typeface-roboto';

import axios from 'axios'

import user from './store/reducers/user.reducers';
import alert from './store/reducers/alert.reducers';



/** Redux setup */
const composeEnhancers = (window as any)['__REDUX_DEVTOOLS_EXTENSION_COMPOSE__'] as typeof compose || compose;
const store = createStore(combineReducers({ user, alert }), composeEnhancers(
  applyMiddleware(thunk)
));

/** Global axios config */
axios.defaults.timeout = 5000;
axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'
axios.interceptors.request.use(function (config) {
  const token = store.getState().user.token;
  if (token) {
    // This is the correct formatting for the bearer token expected by drf
    // https://www.django-rest-framework.org/api-guide/authentication/
    config.headers!.Authorization = `Token ${token}`;
  }
  return config;
});

const app = (
  <Provider store={store}>
    <App />
  </Provider>
)

ReactDOM.render(app, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();