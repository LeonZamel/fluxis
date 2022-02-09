import { userConstants } from '../constants/user.constants';
import { sendLogin, sendSignup, sendLogout, getUserInfo } from '../../core/apiCalls';
import { alertActions } from './alert.actions';
import { history } from '../../core/history';
import axios from 'axios'
import { getErrorMessage } from '../utility';

export const userActions = {
  login,
  signup,
  logout,
  checkState,
  getInfo
}

function logout() {
  localStorage.removeItem('token');
  sendLogout();
  return {
    type: userConstants.LOGOUT
  }
}

function login(username: string, password: string) {
  return (dispatch: any) => {
    dispatch(start())
    sendLogin(username, password)
      .then(res => {
        const token = res.data.key
        localStorage.setItem('token', token)
        dispatch(success(token))
        dispatch(getInfo())
      })
      .catch(error => {
        dispatch(failure(error))
        dispatch(alertActions.error(getErrorMessage(error)))
      })
  }

  function start() { return { type: userConstants.LOGIN_START } }
  function success(token: string) { return { type: userConstants.LOGIN_SUCCESS, token } }
  function failure(error: any) { return { type: userConstants.LOGIN_FAILURE, error } }
}

function signup(username: string, email: string, password1: string, password2: string) {
  return (dispatch: any) => {
    dispatch(start())
    sendSignup(username, email, password1, password2)
      .then(res => {
        const token = res.data.key
        localStorage.setItem('token', token)
        dispatch(success(token))
        dispatch(getInfo())
      })
      .catch(error => {
        dispatch(failure(error))
        dispatch(alertActions.error(getErrorMessage(error)))
      })
  }

  function start() { return { type: userConstants.SIGNUP_START } }
  function success(token: string) { return { type: userConstants.SIGNUP_SUCCESS, token } }
  function failure(error: any) { return { type: userConstants.SIGNUP_FAILURE, error } }
}

function checkState() {
  return (dispatch: any) => {
    dispatch(start())
    const token = localStorage.getItem('token');
    if (token == undefined) {
      dispatch(failure(null))
      dispatch(logout())
    } else {
      dispatch(success(token));
      dispatch(getInfo());
    }
  }

  function start() { return { type: userConstants.AUTO_LOGIN_START } }
  function success(token: string) { return { type: userConstants.AUTO_LOGIN_SUCCESS, token } }
  function failure(error: any) { return { type: userConstants.AUTO_LOGIN_FAILURE, error } }
}

function getInfo() {
  return (dispatch: any) => {
    dispatch(start());
    getUserInfo()
      .then(res => {
        dispatch(success(res.data));
      }).catch(error => {
        dispatch(logout())
        dispatch(failure(error))
      })
  };

  function start() { return { type: userConstants.GET_INFO_START } }
  function success(user: any) { return { type: userConstants.GET_INFO_SUCCESS, user } }
  function failure(error: any) { return { type: userConstants.GET_INFO_FAILURE, error } }
}