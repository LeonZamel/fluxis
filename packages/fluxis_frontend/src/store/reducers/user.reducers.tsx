import { userConstants } from '../constants/user.constants';
import { updateObject } from '../utility';

const initialState = {
  token: null,
  username: "",
  error: null,
  loading: false,
}


const login_start = (state: any, action: any) => {
  return updateObject(state, {
    error: null,
    loading: true,
  })
}

const login_success = (state: any, action: any) => {
  return updateObject(state, {
    token: action.token,
    error: null,
    loading: false,
  })
}

const login_failure = (state: any, action: any) => {
  return updateObject(state, {
    error: action.error,
    loading: false,
  })
}

const signup_start = (state: any, action: any) => {
  return updateObject(state, {
    error: null,
    loading: true,
  })
}

const signup_success = (state: any, action: any) => {
  return updateObject(state, {
    token: action.token,
    error: null,
    loading: false,
  })
}

const signup_failure = (state: any, action: any) => {
  return updateObject(state, {
    error: action.error,
    loading: false,
  })
}

const logout = (state: any, action: any) => {
  return updateObject(state, {
    token: null,
  })
}

const get_info_start = (state: any, action: any) => {
  return updateObject(state, {
    username: ""
  })
}

const get_info_success = (state: any, action: any) => {
  return updateObject(state, {
    username: action.user.username
  })
}

const get_info_failure = (state: any, action: any) => {
  return updateObject(state, {
    username: ""
  })
}

const user = (state: any = initialState, action: any) => {
  switch (action.type) {
    case userConstants.LOGIN_START: return login_start(state, action);
    case userConstants.LOGIN_SUCCESS: return login_success(state, action);
    case userConstants.LOGIN_FAILURE: return login_failure(state, action);
    case userConstants.AUTO_LOGIN_START: return login_start(state, action);
    case userConstants.AUTO_LOGIN_SUCCESS: return login_success(state, action);
    case userConstants.AUTO_LOGIN_FAILURE: return login_failure(state, action);
    case userConstants.SIGNUP_START: return signup_start(state, action);
    case userConstants.SIGNUP_SUCCESS: return signup_success(state, action);
    case userConstants.SIGNUP_FAILURE: return signup_failure(state, action);
    case userConstants.LOGOUT: return logout(state, action);
    case userConstants.GET_INFO_START: return get_info_start(state, action);
    case userConstants.GET_INFO_SUCCESS: return get_info_success(state, action);
    case userConstants.GET_INFO_FAILURE: return get_info_failure(state, action);
    default:
      return state;
  }
}

export default user;
