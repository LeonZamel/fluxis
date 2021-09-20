import { alertConstants } from '../constants/alert.constants';
import { updateObject } from '../utility';


const initialState = {
  severity: null,
  message: null,
}

const success = (state: any, action: any) => {
  return updateObject(state, {
    severity: "alert-success",
    message: action.message
  })
}

const error = (state: any, action: any) => {
  return updateObject(state, {
    severity: "alert-error",
    message: action.message
  })
}

const clear = (state: any, action: any) => {
  return updateObject(state, {
    severity: null,
    message: null
  })
}

const alert = (state: any = initialState, action: any) => {
  switch (action.type) {
    case alertConstants.SUCCESS: return success(state, action);
    case alertConstants.ERROR: return error(state, action);
    case alertConstants.CLEAR: return clear(state, action);
    default:
      return state;
  }
}

export default alert;
