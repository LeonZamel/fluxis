export const updateObject = (oldObject: any, updatedProperties: any) => {
  return {
    ...oldObject,
    ...updatedProperties,
  }
}

export function noSpamApi(callBack: any, valueGetter: () => any, delay: number) {
  // Wait for value to not change for the specified time, then call callback
  const prevVal = valueGetter()
  setTimeout(() => {
    if (prevVal === valueGetter()) {
      callBack()
    }
  }, delay)
}


export function getErrorMessage(error: any): string {
  if (error.response) {
    switch (error.response.status) {
      case 500:
        return "Server Error"
      case 400:
        return ([].concat.apply([], Object.values(error.response.data))).join("\n")
      default: return error.message
    }
  } else {
    return "Server did not respond. Timeout exceeded."
  }
}
