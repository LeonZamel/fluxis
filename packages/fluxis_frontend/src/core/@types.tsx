import { IChart, INode, IPort, ILink, } from '@mrblenny/react-flow-chart'

/*
Naming:
I: Interface
BE: Backend
no identifier if frontend
**/

/*
A key is to identify a node_function, port, parameter, etc. with a clear name, e.g. "url_request"
A name is the displayed name for nicer reading, e.g. "URL Request"
*/


export enum InputDataType {
  OTHER = "other",
  TABLE = "table",
  JSON = "json",
  BOOLEAN = "boolean",
  INT = "int",
  STRING = "string",
  STRING_ARRAY = "string_array",
  ML_MODEL = "ml_model",
}

export const DEFAULT_CONSTANT_VALUE = {
  [InputDataType.OTHER]: "",
  [InputDataType.TABLE]: null,
  [InputDataType.JSON]: null,
  [InputDataType.BOOLEAN]: false,
  [InputDataType.INT]: 0,
  [InputDataType.STRING]: "",
  [InputDataType.STRING_ARRAY]: [],
  [InputDataType.ML_MODEL]: null,
}

export const COLUMN_TYPES_MAPPING: { [key: string]: string } = {
  'object': 'Text',
  'float64': 'Number',
  'int64': 'Whole Number',
  'bool': 'Boolean',
  'datetime64': 'Date and Time',
}

export interface Credentials {
  id: string,
  service: string,  // Unique key for service
}

export interface CredentialsService {
  key: string,
  name: string,
}

export interface CredentialsDef {
  service: string
}

export interface FlowRunSchedule {
  id: number,
  show_tz: string,
  schedule: Crontab,
}

export interface Crontab {
  minute: string,
  hour: string,
  day_of_week: string,
  day_of_month: string,
  month_of_year: string,
}


export interface PortSuggestion {
  how: 'request' | 'from_port',
  from_port?: string,
  getter?: 'column_names'
}

// Backend
//  Defs
export interface IBEPortDef {
  key: string,
  name: string,
  description: string,
  required: boolean,
  internal: boolean,
  data_type: InputDataType,
  suggestion?: PortSuggestion,
}

export type IBEPortDefs = IBEPortDef[]

export interface IBEParameterDef {
  key: string,
  name: string,
  description: string,
  data_type: InputDataType,
  default_value: any,
  required: boolean,
  choices?: any,
}

export type IBEParameterDefs = IBEParameterDef[]

export interface IBENodeDef {
  name: string,
  category: string,
  in_ports: IBEPortDefs,
  out_ports: IBEPortDefs,
  is_trigger_node: boolean,
  parameters: IBEParameterDefs,
  credentials?: CredentialsDef,
}

export interface IBENodeDefs {
  [key: string]: IBENodeDef
}

//  Objects
export interface IBENode {
  id: string, // v4 uuid
  // flow: string, // Flow id
  name: string, // Displayed name
  x: number,
  y: number,
  function: string, // Function type
  in_ports: IBEPort[],
  out_ports: IBEPort[],
  parameters: IBEParameter[],
  trigger_port?: IBEPort,
  credentials?: Credentials,
}

export interface IBEConstantValue {
  value: any,
}

export interface IBEPort {
  key: string,
  node?: string,
  constant_value?: IBEConstantValue,
}

export interface IBELink {
  id: string,
  from_port: IBEPort,
  to_port: IBEPort
}

export interface IBEParameter {
  key: string,
  data_type: string,
  value: any,
}

export type IBEParameters = IBEParameter[]

export interface IBENodeRun {
  id: string, // The Id of the noderun
  node: string, // The Id of the node that was run
  datetime_start: string,
  datetime_end: string,
  name: string, // Name of the node that was run
  function: string, // function of the node that was run
}

export type IBENodes = IBENode[]

export type IBELinks = IBELink[]

export interface IBEFlow {
  id: string,
  nodes: IBENodes,
  edges: IBELinks,
  deployed: boolean,
}

export interface IBEShallowFlow {
  // Shallow, so that no information about the nodes contained has to be known
  id: string,
  name: string,
}

export interface IBEShallowFlowRun {
  // Shallow, so that no information about the node runs has to be known
  id: string,
  flow: IBEShallowFlow,
  datetime_start?: string,
  datetime_end?: string,
  node_run_count: number,
  successful: boolean,
  message: string,
}

export interface IBEFlowRun extends IBEShallowFlowRun {
  node_runs: [IBENodeRun]
}


// Frontend
//  Defs
export type IPortDef = IBEPortDef

export type IPortDefs = { [key: string]: IPortDef }

// TODO: add typing

export type IParameterDef = IBEParameterDef

export type IParameterDefs = { [key: string]: IParameterDef }

export interface INodeDef {
  key: string,
  name: string,
  is_trigger_node: boolean,
  category: string,
  in_ports: { [key: string]: IPortDef },
  out_ports: { [key: string]: IPortDef },
  parameters: { [key: string]: IParameterDef },
  credentials?: CredentialsDef
}

export interface INodeDefs {
  [key: string]: INodeDef
}

//  Objects
export interface IFluxisChart extends IChart {
  scale: number,
  nodes: IFluxisNodes,
  links: IFluxisLinks
}

export type IFluxisLinks = { [id: string]: IFluxisLink }

export type IFluxisLink = ILink

export type IFluxisNodes = { [id: string]: IFluxisNode }

export interface IFluxisNode extends INode {
  type: string, // Function type
  ports: IFluxisPorts,
  properties: {
    name: string, // Displayed name
    parameters: IParameters,
    complete: boolean, // If all ports, parameters have values. For frontend visuals
    credentials?: Credentials,
  }
}

export interface IParameters {
  [key: string]: IParameter
}

export interface IParameter {
  key: string,
  data_type: string,
  value: any,
}

export interface IFluxisPorts {
  [key: string]: IFluxisPort
}

// Currently not used
export interface IFluxisTriggerPort extends IPort {
  type: "input" | "output",
}

export interface IFluxisPort extends IPort {
  // A port has an id which is actually a key. It is the same as the properties.key
  type: "input" | "output", // If the port is input or output, don't confuse with value type that is passed
  properties: {
    key: string,
    name: string,
    data_type?: string, // type of the value being passed, e.g. string, bool, int, table, etc.
    constant_value?: IConstantValue, // Should only be undefined, iff we have an output port
  }
}

export interface IConstantValue {
  value: any,
  enabled: boolean,
}

// Not used
export interface IConstantValueType {
  aggregation: "array" | "single"
  type: "string_array" | "string" | "float" | "int" | "boolean" // | IConstantValueType
}


