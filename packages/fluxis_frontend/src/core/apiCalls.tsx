import axios, { AxiosPromise } from 'axios'
import { IBENode, IBELink, IBEPort, IBEFlowRun, IBEShallowFlowRun, IParameters, IBEFlow, Credentials, Crontab, FlowRunSchedule, CredentialsService } from './@types';

// TODO: unify error messages (also in actions.ts)

const bigDataConfig = { timeout: 30000 } // 30 Seconds

export const sendChangeDeployFlow = (flowId: string, deployed: boolean) => {
  return axios.patch(`/api/v1/flows/${flowId}/`, { "deployed": deployed })
}

export const sendCreateNode = (node: IBENode, flowId: string) => {
  return axios.post(`/api/v1/flows/${flowId}/nodes/`, node)
}

export const sendMoveNode = (nodeId: string, x: number, y: number, flowId: string) => {
  return axios.patch(`/api/v1/flows/${flowId}/nodes/${nodeId}/`, { x, y })
}

export const sendCreateLink = (link: IBELink, flowId: string): AxiosPromise<IBELink> => {
  return axios.post(`/api/v1/flows/${flowId}/edges/`, link)
}

export const sendDeleteLink = (linkId: string, flowId: string) => {
  return axios.delete(`/api/v1/flows/${flowId}/edges/${linkId}/`)
}

export const sendDeleteNode = (nodeId: string, flowId: string) => {
  return axios.delete(`/api/v1/flows/${flowId}/nodes/${nodeId}/`)
}

export const sendChangeTriggerPort = (nodeId: string, enabled: boolean, flowId: string) => {
  let data: any = null
  if (enabled) {
    data = {
      "key": "trigger"
    }
  }
  return axios.patch(`/api/v1/flows/${flowId}/nodes/${nodeId}/`, { "trigger_port": data })
}

export const sendChangeParameterValue = (nodeId: string, parameters: IParameters, flowId: string): AxiosPromise<IBENode> => {
  return axios.patch(`/api/v1/flows/${flowId}/nodes/${nodeId}/`, { parameters: Object.entries(parameters).map(([parameterKey, parameter]) => parameter) })
}

export const sendChangeConstantInputValue = (nodeId: string, in_ports: IBEPort[], flowId: string): AxiosPromise<IBENode> => {
  return axios.patch(`/api/v1/flows/${flowId}/nodes/${nodeId}/`, { in_ports: in_ports })
}

export const sendRunFlow = (flowId: string): AxiosPromise<IBEFlowRun> => {
  return axios.post(`/api/v1/flows/${flowId}/runs/`)
}

export const getInit = (): AxiosPromise<any> => {
  return axios.get(`/api/v1/init/`)
}

export const getAllFlows = () => {
  return axios.get(`/api/v1/flows/`)
}

export const getAllTriggers = () => {
  return axios.get(`/api/v1/triggers/`)
}

// TODO: should error be cancelled here?
export const getAllFlowRuns = (): AxiosPromise<IBEShallowFlowRun[]> => {
  return axios.get(`/api/v1/runs/`)
}

export const getFlowRuns = (flowId: string): AxiosPromise<IBEShallowFlowRun[]> => {
  return axios.get(`/api/v1/flows/${flowId}/runs/`)
}

export const getFlowRun = (flowId: string, flowRunId: string): AxiosPromise<IBEFlowRun> => {
  return axios.get(`/api/v1/flows/${flowId}/runs/${flowRunId}/`)
}

export const getFlowRunNodeData = (flowId: string, runId: string, nodeRunId: string): AxiosPromise<any> => {
  return axios.get(`/api/v1/flows/${flowId}/runs/${runId}/${nodeRunId}/`, bigDataConfig)
}

/*
export const getNodesForFlow = (flowId: string) => {
  return axios.get(`/api/v1/flows/${flowId}/nodes/`)
}
 
export const getEdgesForFlow = (flowId: string) => {
  return axios.get(`/api/v1/flows/${flowId}/edges/`)
}
*/

export const getFlow = (flowId: string): AxiosPromise<IBEFlow> => {
  return axios.get(`/api/v1/flows/${flowId}/`)
}

export const getFlowConfig = (flowId: string) => {
  return axios.get(`/api/v1/flows/${flowId}/config/`)
}

export const sendLogin = (username: string, password: string): AxiosPromise<any> => {
  return axios.post('/api/v1/rest-auth/login/', {
    username, password
  })
}

export const getUserInfo = () => {
  return axios.get('/api/v1/rest-auth/user/')
}

export const sendLogout = () => {
  return axios.post('/api/v1/rest-auth/logout/')
}

export const sendSignup = (username: string, email: string, password1: string, password2: string): AxiosPromise<any> => {
  return axios.post('/api/v1/rest-auth/registration/', {
    username, email, password1, password2
  })
}

/*
export const sendUpdateFlow = (flowId: string, flow: IBEFlow): AxiosPromise<IBEFlow> => {
  return axios.patch(`/api/v1/flows/${flowId}/`, flow)
}
    */

export const sendCreateFlow = (name: string) => {
  return axios.post('/api/v1/flows/', { name })
}

export const sendDeleteFlow = (flowId: string) => {
  return axios.delete(`/api/v1/flows/${flowId}/`)
}

export const getAllFiles = () => {
  return axios.get(`/api/v1/files/`)
}

export const sendCreateFile = (name: string) => {
  return axios.post('/api/v1/flows/', { name })
}

export const sendDeleteFile = (flowId: string) => {
  return axios.delete(`/api/v1/flows/${flowId}/`)
}

export const sendCreateHttpEndpointTrigger = (name: string, path: string): AxiosPromise<any> => {
  return axios.post('/api/v1/triggers/http_endpoint/', { name, path })
}

export const sendCreateTimerTrigger = (name: string, interval: number, repetitions: number): AxiosPromise<any> => {
  return axios.post('/api/v1/triggers/timer/', { name, interval, repetitions })
}


export const sendCreateCredentials = (service: string, username: string, password: string, host: string, port: number, database: string): AxiosPromise<Credentials> => {
  return axios.post('/api/v1/auth/database/', { service, username, password, host, port, database })
}

export const getOAuth2URL = (service_key: string): AxiosPromise<any> => {
  return axios.get('/api/v1/oauth2/start/', { 'params': { service_key } })
}

export const sendOAuth2Code = (code: string) => {
  return axios.post('/api/v1/oauth2/callback/', { code })
}

export const getAllCredentials = (): AxiosPromise<Credentials[]> => {
  return axios.get('/api/v1/auth/credentials/')
}

export const getOAuth2CredentialServices = (): AxiosPromise<CredentialsService[]> => {
  return axios.get('/api/v1/auth/oauth2/services/')
}

export const getDatabaseCredentialServices = (): AxiosPromise<CredentialsService[]> => {
  return axios.get('/api/v1/auth/database/services/')
}

export const sendDeleteCredentials = (credentialsId: string) => {
  return axios.delete(`/api/v1/auth/credentials/${credentialsId}/`)
}

export const sendChangeNodeCredentials = (nodeId: string, flowId: string, credentials: string) => {
  // credentials should be the credentials id
  return axios.patch(`/api/v1/flows/${flowId}/nodes/${nodeId}/`, { credentials })
}

export const getFlowRunSchedules = (flowId: string): AxiosPromise<FlowRunSchedule[]> => {
  return axios.get(`/api/v1/flows/${flowId}/schedules/`)
}

export const sendDeleteSchedule = (flowId: string, scheduleId: number) => {
  return axios.delete(`/api/v1/flows/${flowId}/schedules/${scheduleId}/`)
}

export const sendCreateSchedule = (flowId: string, scheduleInterval: string, scheduleWeekdays: number[], scheduleDate: moment.Moment, show_tz: string): AxiosPromise<FlowRunSchedule> => {
  return axios.post(`/api/v1/flows/${flowId}/schedules/`, {
    'show_tz': show_tz,
    'schedule': {
      'minute': scheduleDate.minutes().toString(), 'hour': scheduleDate.hour().toString(), 'day_of_week': scheduleWeekdays.join(","),
      'day_of_month': "*", 'month_of_year': "*"
    }
  })
}