import { alertConstants } from '../constants/alert.constants';

export const alertActions = {
  success,
  error,
  clear
}

function success(message: string) {
  return {
    type: alertConstants.SUCCESS,
    message,
  }
}

function error(message: string) {
  return {
    type: alertConstants.ERROR,
    message,
  }
}

function clear() {
  return {
    type: alertConstants.CLEAR,
  }
}