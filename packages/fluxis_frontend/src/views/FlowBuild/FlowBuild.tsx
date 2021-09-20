import * as React from 'react'
import moment from 'moment-timezone';
import { TimePicker } from "@material-ui/pickers";
import { IChart, IFlowChartComponents, ILink, FlowChart } from '@mrblenny/react-flow-chart'
import { Page } from '../../components'
import { FluxisNodeInner } from './NodeInner/FluxisNodeInner';
import { INodeDefs, IFluxisNode, IBELink, IBEParameter, IFluxisChart, IBENode, IBEFlowRun, IBEShallowFlowRun, IBENodeDefs, IParameterDef, InputDataType, IPortDef, IFluxisPorts, INodeDef, Credentials, Crontab, FlowRunSchedule, IFluxisPort, DEFAULT_CONSTANT_VALUE } from '../../core/@types';
import { convertNodeDefB2F, convertPortF2B, convertNodeB2F, convertPortsB2F } from '../../core/@types.convert';
import { sendChangeParameterValue, sendRunFlow, getInit, sendChangeConstantInputValue, sendChangeTriggerPort, getFlowRuns, getFlowRun, getFlow, getAllCredentials, sendChangeNodeCredentials, sendCreateSchedule, getFlowRunSchedules, sendDeleteSchedule, sendChangeDeployFlow } from '../../core/apiCalls';
import { NodeFactory } from '../../core/NodeFactory';
import { Button, Paper, List, TextField, Divider, Switch, Tooltip, Box, Collapse, ListItemText, ListItem, Checkbox, Select, InputLabel, MenuItem, Popover, Card, CardActions, CardContent, Dialog, DialogTitle, DialogContent, DialogActions, FormControlLabel, ListItemSecondaryAction, IconButton, Chip } from '@material-ui/core';
import { FluxisNode } from './Node/FluxisNode';
import { FluxisPort } from './Port/FluxisPort';
import { FluxisPorts } from './Ports/FluxisPorts';
import { RouteComponentProps, Link } from 'react-router-dom';
import * as actions from './actions'
import mapValues from '../../utils/mapValues'
import _ from 'lodash';
import { Typography } from '@material-ui/core';
import { ExpandMore, ExpandLess, Delete } from '@material-ui/icons';
import Horizontalbar from './Horizontalbar';
import { FlowRunData } from '../../core/FlowRunData';
import DataTable from './DataTable';
import DataOverlay from './DataOverlay';
import Sidebar from './Sidebar';
import { SidebarNodeItem } from './SidebarNodeItem';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { formatRunStart, formatRunDuration, formatDuration } from '../../core/helpers';
import { connect } from 'react-redux';
import { alertActions } from '../../store/actions/alert.actions';
import RunStatus from '../../components/RunStatus';
import { noSpamApi, getErrorMessage } from '../../store/utility';
import { timezones } from '../../utils/timezones';
import { HM_TIME_FORMAT } from '../../core/constants';

import update from 'immutability-helper';


const FLOW_RUN_POLLING_DELAY_MS = 1000

// These props come from the router
interface IFlowBuildRouterProps {
  flowId: string,
}

export interface IFlowBuildProps extends RouteComponentProps<IFlowBuildRouterProps> {
  Components?: IFlowChartComponents,
  alert_error: any,
}

export interface IFlowBuildState {
  chart: IFluxisChart,
  nodeFunctions: INodeDefs, // Available nodes
  nodeFunctionsCategoriesOpen: { [category: string]: boolean }, // If the collapse in the node choice is open
  flowId: string,
  searchBox: string,
  credentials: Credentials[], // Credentials to use in nodes

  deployed: boolean,

  // If we are testing, we are currently inspecting a test run, but the flow is not deployed
  testing: boolean,

  // Only needed when not in build mode
  currentRunId: string,
  currentRun: IBEFlowRun | null,
  currentNodeRunsOpen: { [nr_id: string]: boolean }, // If the collapse in the noderun list is open
  runData: FlowRunData | null,
  runs: IBEShallowFlowRun[],
  dataOverlayOpenId: string | undefined, // Id of the noderun data that is currently fullscreen
  currentlyRunning: boolean,
  currentlyRunningId: string,

  currentSchedule: FlowRunSchedule[],
  createScheduleOpen: boolean,
  scheduleInterval: string,
  scheduleDateTime: Date,
  scheduleWeekdays: number[],
  scheduleTimezone: string,
}

/**
 * Flow Chart With State
 */
class FlowBuild extends React.Component<IFlowBuildProps, IFlowBuildState> {
  private timer: any = null
  private stateActions: any;

  constructor(props: IFlowBuildProps) {
    super(props)
    this.state = {
      chart: {
        scale: 1,
        offset: {
          x: 0,
          y: 0,
        },
        nodes: {},
        links: {},
        selected: {},
        hovered: {},
      },
      nodeFunctions: {}, 
      nodeFunctionsCategoriesOpen: {},
      flowId: this.props.match.params.flowId,

      searchBox: "",
      credentials: [],

      deployed: false,
      testing: false,

      currentRunId: "",
      currentRun: null,
      currentNodeRunsOpen: {},
      runData: null,
      runs: [],
      dataOverlayOpenId: undefined,
      currentlyRunning: false,
      currentlyRunningId: "",
      // TODO: Clearly differentiate all these parameters

      // TODO: Add schedules back in
      currentSchedule: [],
      createScheduleOpen: false,
      scheduleInterval: "Day", // TODO: allow monthly
      scheduleDateTime: new Date(),
      scheduleWeekdays: [],
      scheduleTimezone: "",
    }
    this.stateActions = mapValues(actions, (func: any) =>
      (...args: any) => this.setState(prevState => ({ chart: func(this.chartUpdateCallback.bind(this), this.buildNode.bind(this), prevState.flowId)(...args)(prevState.chart) })))
  }

  public componentDidMount() {
    getInit().then(resp => {
      let node_defs: INodeDefs = {}
      let response_defs: IBENodeDefs = resp.data.node_functions_definitions
      for (let node_def_key in response_defs) {
        node_defs[node_def_key] = convertNodeDefB2F(node_def_key, response_defs[node_def_key])
      }
      let nodeFunctionsCategories: { [key: string]: boolean } = {};
      for (let node_cat_key of resp.data.node_functions_categories) {
        nodeFunctionsCategories[node_cat_key] = false
      }
      this.setState(
        {
          nodeFunctions: node_defs,
          nodeFunctionsCategoriesOpen: nodeFunctionsCategories
        },
        this.loadFlow
      )
    })
    getFlowRuns(this.state.flowId).then(resp => {
      this.setState({ runs: resp })
    })
    getAllCredentials().then(resp => {
      this.setState({ credentials: resp.data })
    })
    getFlowRunSchedules(this.state.flowId).then(resp => {
      this.setState({ currentSchedule: resp.data })
    })
  }

  private async loadFlow() {
    let newChart: IFluxisChart = {
      scale: 1,
      offset: {
        x: 0,
        y: 0,
      },
      nodes: {},
      links: {},
      selected: {},
      hovered: {},
    };

    let flowResp = await getFlow(this.state.flowId)

    let deployed: boolean = flowResp.data.deployed

    let nodesResp: IBENode[] = flowResp.data.nodes

    for (let node of nodesResp) {
      // We build the node based on the type, then set the values based on the ones from the backend
      // TODO: should everything be copied over from the backend directly?
      let nn: IFluxisNode = this.buildNode(node.function, node.id!);

      // Add optional credentials
      nn.properties.credentials = node.credentials

      // Add optional parameters
      let parameters: IBEParameter[] = node.parameters!
      for (let parameter of parameters) {
        nn.properties.parameters[parameter.key].value = parameter.value
      }

      nn.ports = convertPortsB2F(node.in_ports, node.out_ports, this.state.nodeFunctions[node.function], node.trigger_port)

      nn.position.x = node.x;
      nn.position.y = node.y;
      newChart.nodes[nn.id] = nn;
    }

    let linksResp: IBELink[] = flowResp.data.edges

    for (let link of linksResp) {
      let nl: ILink = {
        id: link.id,
        from: {
          nodeId: link.from_port.node!,
          portId: link.from_port.key
        },
        to: {
          nodeId: link.to_port.node,
          portId: link.to_port.key
        }
      }
      newChart.links[nl.id] = nl;
    }

    this.setState({
      deployed,
      chart: newChart,
    })
  }

  private startPollFlowRun() {
    // Repeatedly poll the server to get the result of the current run
    if (this.state.currentlyRunning) {
      getFlowRun(this.state.flowId, this.state.currentlyRunningId).then(res => {
        this.downloadFlowRunData(this.state.currentlyRunningId, this.state.flowId)
        if (res.datetime_end === null) {
          setTimeout(this.startPollFlowRun.bind(this), FLOW_RUN_POLLING_DELAY_MS)
        } else {
          this.setState(prevState => ({
            currentlyRunning: false,
            runs: [res, ...(prevState.runs.filter(run => run.id !== prevState.currentlyRunningId))],
            currentlyRunningId: ""
          })
          )
        }
      })
    }
  }

  private updateCompletedNodes() {
    // Check if a node is completed, i.e. all inputs are connected or have a constant value
    let newNodes = this.state.chart.nodes
    Object.entries(newNodes).forEach(([key, node]) => {
      node.properties.complete = true
      // Get all inputs which don't have a constant value
      let empty_ports = _.pickBy(node.ports, (port) =>
        port.type === "input" && !port.properties.constant_value!.enabled
      )
      // If a node is connected, also dismiss it
      Object.entries(this.state.chart.links).forEach(([linkKey, link]) => {
        if (!!link.to.nodeId && link.to.nodeId === key && !!link.to.portId && !!empty_ports[link.to.portId]) {
          delete empty_ports[link.to.portId]
        }
      })
      node.properties.complete = _.isEmpty(empty_ports) && _.isEmpty(_.pickBy(node.properties.parameters, param => param.value == null))
    })
  }

  private nodeParameterValueChangeCallback(nodeId: string, parameterKey: string, value: any) {
    this.setState(state => (state.chart.nodes[nodeId].properties.parameters[parameterKey].value = value, state),
      () =>
        noSpamApi(() =>
          sendChangeParameterValue(nodeId, this.state.chart.nodes[nodeId].properties.parameters, this.state.flowId),
          () => this.state.chart.nodes[nodeId].properties.parameters[parameterKey].value,
          1000
        )
    )
  }

  private nodeInputConstantToggleCallback(nodeId: string, portKey: string, enable: boolean, defaultValue: any) {
    if (enable) {
      // Remove visual link to port if it is set to constant value, backend automatically removes edge
      this.setState(state => (state.chart.links = _.pickBy(state.chart.links, (val: any) => (val.to.nodeId !== nodeId || val.to.portId !== portKey)), state))
    }
    const newConstantVal = this.state.chart.nodes[nodeId].ports[portKey].properties.constant_value!
    newConstantVal.enabled = enable
    newConstantVal.value = defaultValue

    this.setState(state => (state.chart.nodes[nodeId].ports[portKey].properties.constant_value = newConstantVal, state),
      () => sendChangeConstantInputValue(nodeId, [convertPortF2B(this.state.chart.nodes[nodeId].ports[portKey], nodeId)], this.state.flowId)
    )
  }

  private nodeInputConstantValueChangeCallback(nodeId: string, portKey: string, value: any) {
    const newConstantVal = this.state.chart.nodes[nodeId].ports[portKey].properties.constant_value!
    newConstantVal.enabled = true
    newConstantVal.value = value
    this.setState(state => (
      state.chart.nodes[nodeId].ports[portKey].properties.constant_value = newConstantVal,
      state.chart.links = _.pickBy(state.chart.links, (val: any) => (val.to.nodeId !== nodeId || val.to.portId !== portKey)),
      state),
      () => noSpamApi(
        () => sendChangeConstantInputValue(nodeId, [convertPortF2B(this.state.chart.nodes[nodeId].ports[portKey], nodeId)], this.state.flowId),
        () => this.state.chart.nodes[nodeId].ports[portKey].properties.constant_value!.value,
        1000
      )
    )
  }

  public buildNode(type: string, id: string): IFluxisNode {
    return NodeFactory.call(this, this.state.nodeFunctions[type], id)
  }

  public chartUpdateCallback(newChart: IFluxisChart) {
    if (newChart !== undefined) {
      this.setState({ chart: newChart })
    }
  }

  private selectCurrentRun(runId: string): void {
    this.setState({ currentRunId: runId, runData: new FlowRunData(runId) },
      () => this.downloadFlowRunData(runId, this.state.flowId))
  }

  private downloadFlowRunData(flowRunId: string, flowId: string) {
    getFlowRun(flowId, flowRunId).then((resp) => {
      this.setState({ currentRun: resp, currentNodeRunsOpen: Object.fromEntries(resp.node_runs.map((val) => [val, false])) },
        () => {
          this.state.currentRun!.node_runs.forEach((nodeRun) => {
            if (nodeRun.datetime_end != null) {
              if (!(FlowRunData.hasNodeData(this.state.runData!, nodeRun.id) || FlowRunData.isLoadingNodeData(this.state.runData!, nodeRun.id))) {
                this.downloadNodeRunData(nodeRun.id)
              }
            }
          })
        }
      )
    })
  }

  private downloadNodeRunData(nodeRunId: string) {
    this.setState(prevState => {
      let newRunData: FlowRunData = { ...prevState.runData! };
      FlowRunData.setLoadingNodeData(this.state.runData!, nodeRunId, true)
      return { runData: newRunData }
    })
    FlowRunData.loadNodeData(this.state.runData!.runId, nodeRunId).then((resp: any) => {
      this.setState(prevState => {
        let newRunData: FlowRunData = { ...prevState.runData! };
        FlowRunData.setNodeData(newRunData, nodeRunId, resp)
        return { runData: newRunData }
      })
    })
  }

  private runFlow(): void {
    this.setState(prevState => ({
      currentlyRunning: true,
      currentRun: null,
      currentRunId: "",
    }))
    sendRunFlow(this.state.flowId).then(res => {
      this.setState(prevState => ({
        testing: !prevState.deployed,
        currentlyRunning: true,
        currentlyRunningId: res.data.id,
        runs: [{
          id: res.data.id,
          flow: { id: "", name: "" },
          datetime_start: res.data.datetime_start,
          datetime_end: res.data.datetime_end,
          node_run_count: 0,
          successful: false,
          message: ""
        }, ...prevState.runs]
      }), () => {
        this.selectCurrentRun(res.data.id)
        this.startPollFlowRun()
      })
    }).catch(err => {
      this.setState({ currentlyRunning: false })
      this.props.alert_error(getErrorMessage(err))
    })
  }


  private changeDeployFlow(deploy: boolean) {
    sendChangeDeployFlow(this.state.flowId, deploy)
    this.setState({ deployed: deploy })
  }

  private calculateSearchResults(): { [category: string]: INodeDefs } {
    let searchResults;
    if (this.state.searchBox.length) {
      const searchPattern = new RegExp(this.state.searchBox.split(' ').map(term => `(?=.*${term})`).join(''), 'i');
      searchResults = _.pickBy(this.state.nodeFunctions, option =>
        option.name.match(searchPattern)
      );
    } else {
      searchResults = this.state.nodeFunctions;
    }

    let searchResultsByCategory: { [category: string]: INodeDefs } = {}
    Object.entries(searchResults).forEach(([key, val]) => {
      if (!searchResultsByCategory[val.category]) {
        searchResultsByCategory[val.category] = {}
      }
      searchResultsByCategory[val.category][key] = val
    })

    return searchResultsByCategory
  }

  private renderTable(data: any, nodeRunId: string): any {
    return (
      <Box width='100%'>
        <Box width='100%' height='40vh'>
          <DataTable data={data} />
        </Box>
        <Button size="small" variant="contained" color="primary" onClick={(ev) => {
          ev.stopPropagation()
          this.setState(prevState => { return { dataOverlayOpenId: nodeRunId } })
        }
        }>Show Fullscreen</Button>
        <DataOverlay open={this.state.dataOverlayOpenId === nodeRunId} closeAction={() => this.setState(prevState => { return { dataOverlayOpenId: undefined } })}>
          <DataTable data={data} />
        </DataOverlay>
      </Box>
    )
  }

  private renderRunOutputs(): any {
    var sortedRuns = this.state.currentRun!.node_runs.sort((nrA, nrB) => nrA.datetime_start.localeCompare(nrB.datetime_start))
    return (
      <Box maxHeight='100%' display='flex' flexDirection='column'>
        <Box m={2} flexGrow='0'>
          <Box display='flex' flexDirection='row' justifyContent='space-between'><Typography variant='h6'>Run results</Typography><Button size="small" variant="contained" color="primary" onClick={() => this.setState(prevState => ({ testing: false, currentRun: null, currentRunId: "" }))}>Close</Button></Box>
          <Typography variant='subtitle1'>{formatRunStart(this.state.currentRun!)}</Typography>
          <Divider />
        </Box>
        <Box flexGrow='1' overflow='auto'>
          <List style={{ maxHeight: '100%' }} >
            {
              sortedRuns.map((nr) => {
                let hasData: boolean = FlowRunData.hasNodeData(this.state.runData!, nr.id)
                let isLoading: boolean = FlowRunData.isLoadingNodeData(this.state.runData!, nr.id)
                return (
                  <ListItem
                    button
                    disableRipple
                    divider
                    key={nr.id}
                    onClick={() =>
                      this.setState(prevState => {
                        let currentNodeRunsOpen = { ...prevState.currentNodeRunsOpen }
                        currentNodeRunsOpen[nr.id] = !currentNodeRunsOpen[nr.id]
                        return { currentNodeRunsOpen }
                      })
                    }>
                    <Box display='flex' flexDirection='column' maxWidth='100%'>
                      <Box>
                        <ListItemText primary={this.state.nodeFunctions[nr.function].name} secondary={formatRunDuration(nr.datetime_start, nr.datetime_end)} />
                        {this.state.currentNodeRunsOpen[nr.id] ? <ExpandLess /> : <ExpandMore />}
                      </Box>
                      <Collapse in={this.state.currentNodeRunsOpen[nr.id]} timeout="auto" unmountOnExit>
                        <Box>
                          {
                            (!hasData || isLoading) ?
                              "Loading data..." :
                              ('non_serializable' in this.state.runData!.nodes[nr.id].ports) ?
                                (<Box>Binary Data</Box>) :
                                ('error' in this.state.runData!.nodes[nr.id].ports) ?
                                  (<Box><Box>Error</Box>{this.state.runData!.nodes[nr.id].ports["error"].data}</Box>) :
                                  Object.entries(this.state.runData!.nodes[nr.id].ports).map(([portId, port]) =>
                                  (<Box key={portId} width='100%'>
                                    <Box width='100%'>{
                                      this.state.runData!.nodes[nr.id] && port ?
                                        port.type === "tabular" ? this.renderTable(port.data, nr.id) : JSON.stringify(port.data)
                                        : "Couldn't load data"
                                    }</Box>
                                  </Box >)
                                  )
                          }
                        </Box>
                      </Collapse>

                    </Box>
                  </ListItem> /*
                
                if (!hasData || isLoading) {
                  
                }
            if ('error' in this.state.runData!.nodes[nr.id].ports) {
                  (<Box><Box>Error</Box>{this.state.runData!.nodes[nr.id].ports["error"].data}</Box>)
                }
            Object.entries(this.state.runData!.nodes[nr.id].ports).map(([portId, port]) => {
                  (<Box key={portId}>
                    <Box>{ port.properties.key + ":" }</Box>
                    <Box>{
                      this.state.runData!.nodes[nr.id] && this.state.runData!.nodes[nr.id].ports[portId] ?
                        this.state.runData!.nodes[nr.id].ports[portId].type === "tabular" ? this.renderTable(this.state.runData!.nodes[nr.id].ports[portId].data) : JSON.stringify(this.state.runData!.nodes[nr.id].ports[portId].data)
                        : "Couldn't load data"
                    }</Box>
                  </Box >)
                })
              )} */)
              })}
          </List>
        </Box>
      </Box>
    )
    /*
  let nodeRun: any = this.state.currentRun!.node_runs.find((nr) => nr.node === selectedNode.id)
  if (nodeRun === undefined) {
    return "No data"
  }
  let hasData: boolean = FlowRunData.hasNodeData(this.state.runData!, nodeRun.id)
  let isLoading: boolean = FlowRunData.isLoadingNodeData(this.state.runData!, nodeRun.id)
  if (!hasData || isLoading) {
    return "Loading data..."
  }
  if ('error' in this.state.runData!.nodes[nodeRun.id].ports) {
    return (<Box><Box>Error</Box>{this.state.runData!.nodes[nodeRun.id].ports["error"].data}</Box>)
  }

  */
  }

  private renderValueSelection(name: string, data_type: InputDataType, value_getter: any, value_setter: any, suggestions: any[], freeChoice: boolean) {
    var current_val = value_getter()
    if (data_type === InputDataType.BOOLEAN) {
      if (!(typeof current_val === "boolean")) {
        current_val = false
      }
      return (
        <Box>
          {name}
          <Checkbox
            checked={current_val}
            onChange={(event: object, checked: boolean) => value_setter(checked)}
          />
        </Box>
      )
    } else if (data_type === InputDataType.STRING_ARRAY) {
      if (!(Array.isArray(current_val))) {
        current_val = []
      }
      return (
        <Box>
          <Autocomplete
            style={{ width: "100%" }}
            multiple
            freeSolo={freeChoice}
            id={name}
            options={suggestions}
            defaultValue={current_val}
            onChange={(event: any, values: any) => value_setter(values)}
            renderTags={(value: string[], getTagProps: any) =>
              value.map((option: string, index: number) => (
                <Chip variant="outlined" label={option} {...getTagProps({ index })} />
              ))
            }
            renderInput={(params) => (
              <TextField style={{ width: "100%" }} {...params} label={name} />
            )
            }
          />
          <Typography variant="caption">You can select multiple values. Press enter to add the value.</Typography>
        </Box>)
    } else if (data_type === InputDataType.STRING || true) {
      return (
        <Autocomplete
          disableClearable={!freeChoice}
          freeSolo={freeChoice}
          id={name}
          options={suggestions}
          inputValue={current_val}
          onInputChange={(event: any, newVal: any) => value_setter(newVal)}
          defaultValue={current_val}
          renderInput={(params) => (
            <TextField
              {...params}
              style={{ width: "100%" }}
              key={name}
              label={name}
              margin="normal"
              fullWidth
            />
          )}
        />
      )
    }
  }

  private renderParameterConfiguration(parameterDef: IParameterDef, selectedNode: IFluxisNode) {
    const parameterDataType: InputDataType = parameterDef.data_type
    const parameterKey: string = parameterDef.key

    var suggestions: any[] = []
    if (parameterDef.choices) {
      suggestions = parameterDef.choices
    }

    return this.renderValueSelection(
      parameterDef.name, parameterDef.data_type,
      () => selectedNode.properties.parameters[parameterKey].value,
      (val: any) => this.nodeParameterValueChangeCallback(selectedNode!.id, parameterKey, val),
      suggestions,
      false)
  }

  private renderConstantValueInput(portKey: string, portVal: IFluxisPort, selectedNode: IFluxisNode) {
    const portDef: IPortDef = this.state.nodeFunctions[selectedNode.type].in_ports[portKey]
    const uniqueKey: string = selectedNode.id + "-" + portKey


    // Some input port types don't support inputting constant values
    if (portDef.data_type === InputDataType.TABLE || portDef.data_type === InputDataType.ML_MODEL) {
      return null
    }

    let getCurrentConstantVal = () => selectedNode!.ports[portKey].properties.constant_value!.value || DEFAULT_CONSTANT_VALUE[portDef.data_type]

    // If we are currently testing we are still inspecting a run
    // We can make suggestions from the previous run data
    var suggestions: any[] = []
    if (this.state.testing) {
      if (portDef.suggestion && portDef.suggestion!.how === 'from_port') {
        // We get the suggestion based on the data coming into a port
        // e.g. for column_name a valid value would be one of the columns from the table coming in to the table_in port of the same node
        let link = Object.values(this.state.chart.links).find((link) => { return link.to.nodeId === selectedNode.id && link.to.portId === portDef.suggestion!.from_port! })
        if (link) {
          // There is a link connected to this port. Get the from port and check if it had data last run
          let noderun = this.state.currentRun?.node_runs.find((nr) => nr.node === link!.from.nodeId)
          if (noderun) {
            var raw = this.state.runData!.nodes[noderun.id].ports[link.from.portId]
            if (portDef.suggestion!.getter === 'column_names') {
              if (raw['type'] === 'tabular') {
                suggestions = Object.keys(raw['data']['values'])
              }
            }
          }
        }
      }
    }

    return (
      <Box key={uniqueKey} flexDirection='row' display='flex' alignItems='center' justifyContent='space-between'>
        <Tooltip title={portDef.description}>
          <Box width={"100%"}>
            {
              this.renderValueSelection(
                portDef.name,
                portDef.data_type,
                getCurrentConstantVal,
                (val: any) => this.nodeInputConstantValueChangeCallback(selectedNode!.id, portKey, val),
                suggestions,
                true)
            }
          </Box>
        </Tooltip>
        {
          /*
          <Select
            style={{ width: '100%' }}
            labelId='select-constant-value-type'
            value={portVal.properties.constant_value?.data_type}
            onChange={(e: any) => {
              this.setState(state => (
                state.chart.nodes[selectedNode.id].ports[portKey].properties.constant_value!.data_type = e.target.value, state))
            }
            }
          >
            {Object.values(InputDataType).map((val: string) =>
              <MenuItem key={val} value={val}>{val}</MenuItem>
            )}
          </Select>
          */
        }
        <Tooltip title={"Use constant value"}>
          <Checkbox
            checked={selectedNode!.ports[portKey].properties.constant_value!.enabled}
            onChange={(event: object, checked: boolean) => { this.nodeInputConstantToggleCallback(selectedNode!.id, portKey, checked, getCurrentConstantVal()) }}
          />
        </Tooltip>
      </Box >
    )
  }

  private renderConstantInputSelection(selectedNodeInputPorts: IFluxisPorts, selectedNode: IFluxisNode) {
    // Cannot choose constant values for Table input
    var inputPorts = Object.entries(selectedNodeInputPorts)
    if (inputPorts.length > 0) {
      return (
        <Box>
          <Typography variant='h6'>Inputs:</Typography>
          <List>
            {inputPorts.map(([portKey, portVal]) =>
              this.renderConstantValueInput(portKey, portVal, selectedNode)
            )}
          </List>
        </Box>
      )
    }
    else { return null }
  }

  private renderNodeConfig(selectedNode: IFluxisNode, selectedNodeInputPorts: IFluxisPorts): any {
    const selectedNodeDef: INodeDef = this.state.nodeFunctions[selectedNode.type]

    return (
      <Box mx={2}>
        <Box my={2}>
          <Typography variant='h6'>{selectedNode.properties.name}</Typography>
        </Box>
        <Divider />
        <Box>
          { /*
        // Only show the require trigger option when the selected node isn't a trigger node
          !this.state.nodeFunctions[selectedNode.type].is_trigger_node &&
          <Box>
            <Box mb={2} flexDirection='row' display='flex' alignItems='center' justifyContent='space-between'>
              <Box>Require trigger signal</Box>
              <Checkbox
                checked={selectedNode.ports["trigger"] !== undefined}
                onChange={(event: object, checked: boolean) => this.nodeTriggerPortToggleCallback(selectedNode!.id, checked)}
              />
            </Box>
            <Divider />
          </Box>
          */
          }
          { // Parameter options
            (!_.isEmpty(selectedNode.properties.parameters) || selectedNodeDef.credentials) &&
            <Box>
              <Typography variant='h6'>Parameters:</Typography>
              { // Credentials
                selectedNodeDef.credentials &&
                <Box>
                  <InputLabel id='select-label'>Credentials</InputLabel>
                  <Select
                    style={{ width: '100%' }}
                    labelId='select-label'
                    value={selectedNode.properties.credentials && selectedNode.properties.credentials.id || undefined
                      // selectedNode.properties.credentials?.id Won't compile even with correct typescript version???
                    }
                    onChange={(e: any) => {
                      sendChangeNodeCredentials(selectedNode.id, this.state.flowId, e.target.value).then(resp => {
                        this.setState(state => (
                          state.chart.nodes[selectedNode.id].properties.credentials = state.credentials.find(cred => cred.id == e.target.value), state),
                        )
                      })
                    }}
                  >
                    {this.state.credentials.filter((cred) => cred.service === selectedNodeDef.credentials!.service).map(cred =>
                      <MenuItem key={cred.id} value={cred.id}>{cred.service}</MenuItem>
                    )}
                  </Select>
                  <Divider />
                </Box>
              }
              <List>
                {Object.entries(this.state.nodeFunctions[selectedNode.type].parameters).map(([paramKey, paramVal]) => {
                  const parameterDef: IParameterDef = this.state.nodeFunctions[selectedNode.type].parameters[paramKey]
                  return (
                    <Box key={paramKey}>
                      <Tooltip title={parameterDef.description}>
                        {this.renderParameterConfiguration(parameterDef, selectedNode!)}
                      </Tooltip>
                    </Box>
                  )
                })}
              </List>
              <Divider />
            </Box>
          }

          { // If no ports and no parameters, display message
            _.isEmpty(selectedNode.properties.parameters) && _.isEmpty(selectedNodeInputPorts) ?
              <Box my={1}>No configuration needed</Box> : null
            // If ports and parameters, display divider
            /*
            !_.isEmpty(selectedNode.properties.parameters) && !_.isEmpty(selectedNodeInputPorts) ?
              <Divider /> : null
              */
          }

          {
            this.renderConstantInputSelection(selectedNodeInputPorts, selectedNode)
          }
        </Box >
      </Box>
    )
  }

  private renderRunEntry(run: IBEShallowFlowRun) {
    return (
      <Box>
        <RunStatus run={run} />
        <ListItemText primary={formatRunStart(run)} secondary={formatRunDuration(run.datetime_start, run.datetime_end)} />
      </Box>
    )
  }

  private renderFlowRuns() {
    return (
      <Box>
        <List>
          {this.state.runs.map(run =>
            <Box key={run.id}>
              <ListItem
                selected={this.state.currentRunId === run.id}
                button onClick={() =>
                  this.selectCurrentRun(run.id)
                }>
                {/* If run id is blank this is the currently running run */}
                {this.renderRunEntry(run)}
              </ListItem>
              <Divider />
            </Box>
          )}
        </List>
      </Box>
    )
  }

  private renderDragDropNodes() {
    let searchResultsByCategory: { [category: string]: INodeDefs } = this.calculateSearchResults()
    return (
      <List>
        {Object.entries(searchResultsByCategory).map(([category, defs]) =>
          <Box key={category}>
            <ListItem
              button onClick={() =>
                this.setState(prevState => {
                  let nodeFunctionsCategoriesOpen = { ...prevState.nodeFunctionsCategoriesOpen }
                  nodeFunctionsCategoriesOpen[category] = !nodeFunctionsCategoriesOpen[category]
                  return { nodeFunctionsCategoriesOpen }
                })
              }>
              <ListItemText primary={<b>{category}</b>} />
              {this.state.nodeFunctionsCategoriesOpen[category] ? <ExpandLess /> : <ExpandMore />}
            </ListItem>
            <Divider />
            <Collapse in={this.state.nodeFunctionsCategoriesOpen[category]} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {Object.entries(defs).map(([key, def]) =>
                  <Box key={key}>
                    <SidebarNodeItem
                      type={key}
                      properties={{
                        name: def.name,
                      }} />
                    <Divider />
                  </Box>)}
              </List>
            </Collapse>
          </Box>
        )}
      </List>
    )
  }

  private handleCreateSchedule() {
    sendCreateSchedule(this.state.flowId, this.state.scheduleInterval, this.state.scheduleWeekdays, moment.tz(this.state.scheduleDateTime, this.state.scheduleTimezone).utc(), this.state.scheduleTimezone).then(
      resp => {
        this.setState(prevState => { return { currentSchedule: [resp.data, ...prevState.currentSchedule], createScheduleOpen: false } })
      }
    )
  }

  private handleDeleteSchedule(scheduleId: number) {
    sendDeleteSchedule(this.state.flowId, scheduleId).then(
      resp => {
        this.setState(prevState => { return { currentSchedule: prevState.currentSchedule.filter(sched => sched.id !== scheduleId) } })
      }
    )
  }

  private renderSchedule() {
    return (
      <List>
        {this.state.currentSchedule!.map((s) => {
          const id = s.id
          const sched = s.schedule
          const show_tz = s.show_tz
          const time: moment.Moment = moment(sched.hour + ':' + sched.minute, "hh:mm").tz(show_tz)

          return (
            <ListItem key={id} divider>
              <ListItemText
                primary={time.format(HM_TIME_FORMAT)}
                secondary={
                  <Box display='flex' flexDirection='column'>
                    <Box>{_.at(moment.weekdays(), sched.day_of_week.split(',').map(e => parseInt(e, 10))).map(e => e.slice(0, 3)).join(', ')}</Box>
                    <Box>{show_tz}</Box>
                  </Box>
                }
              />
              <ListItemSecondaryAction>
                <IconButton edge="end" aria-label="delete" onClick={() => this.handleDeleteSchedule(id)}>
                  <Delete />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          )
        })}
      </List>
    )
  }

  private renderLeftToolbar() {
    let selectedNode: IFluxisNode | undefined = this.state.chart.selected ? this.state.chart.nodes[this.state.chart.selected.id!] : undefined;
    let selectedNodeInputPorts: any = selectedNode === undefined ? {} : _.pickBy(selectedNode!.ports, (val: any) => val.type === "input" && val.id !== "trigger")

    return (
      <Sidebar style={{ height: '90%', width: '20vw' }}>
        <Paper style={{ maxHeight: '100%', display: 'flex', flexDirection: 'column' }}>
          {!this.state.deployed && selectedNode !== undefined ?
            this.renderNodeConfig(selectedNode!, selectedNodeInputPorts)
            :
            <Box maxHeight={1} display='flex' flexDirection='column'>
              <Box style={{
                flexDirection: 'row',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-around',
                margin: '10px'
              }} >
                <Switch
                  color={'primary'}
                  checked={this.state.deployed}
                  onChange={(event: object, checked: boolean) => this.changeDeployFlow(checked)}
                />
                Deploy
                <Button style={{ margin: '5%', width: '90%' }} disabled={this.state.currentlyRunning} size="large" variant="contained" color="primary" onClick={() => this.runFlow()}>
                  Run Now
                </Button>
              </Box>
              <Divider />
              {!this.state.deployed ?
                <TextField
                  id="search_function"
                  label="Search"
                  type="search"
                  margin="dense"
                  variant="outlined"
                  style={{ margin: '3%', width: '94%' }}
                  onChange={(e: any) => { this.setState({ searchBox: e.target.value }) }}
                />
                :
                <Box>
                  {/*
                  <Box>
                    {this.state.currentSchedule.length > 0 ?
                      this.renderSchedule()
                      :
                      <Box m={2}>No Run Schedule</Box>}
                  </Box>
                  <Button style={{ margin: '5%', width: '90%' }} size="small" variant="contained" color="secondary" onClick={() => this.setState({ createScheduleOpen: true })}>
                    Edit run schedule
                    </Button>
                    */}
                </Box>
              }
              <Divider />
              <Box style={{ maxHeight: '100%', overflow: 'auto' }}>
                {!this.state.deployed ?
                  this.renderDragDropNodes()
                  :
                  this.renderFlowRuns()
                }
              </Box>
            </Box>
          }
        </Paper>
        <Dialog
          fullWidth={true}
          maxWidth={'sm'}
          open={this.state.createScheduleOpen}
          onClose={() => this.setState({ createScheduleOpen: false })}
          aria-labelledby="form-dialog-title"
        >
          {

            <Box>
              <DialogTitle id="form-dialog-title">New Schedule</DialogTitle>
              <DialogContent>
                <Box display='flex' flexDirection='column' justifyContent='space-around'>
                  Run
                  {/*
                <Select
                    labelId='select-label'
                    value={this.state.scheduleInterval}
                    onChange={(e: any) => { this.setState({ scheduleInterval: e.target.value }) }}
                  >
                    {["Day", "Month"].map(val =>
                      <MenuItem key={val} value={val}>{val}</MenuItem>
                    )}
                  </Select>
                    */}
                  {this.state.scheduleInterval === 'Day' ?
                    <Box>
                      On:
                      {moment.weekdays().map((val, i) => (
                      <FormControlLabel
                        key={i}
                        value={i}
                        control={
                          <Checkbox
                            checked={this.state.scheduleWeekdays.includes(i)}
                            onChange={(event: object, checked: boolean) => {
                              this.setState(prevState => ({
                                scheduleWeekdays: [...prevState.scheduleWeekdays, i].filter((e) => e !== i || checked)
                              }))
                            }}
                          />
                        }
                        label={val.slice(0, 3)}
                        labelPlacement="top"
                      />))
                      }
                    </Box>
                    :
                    <Box>
                      Day of Month:
                    </Box>
                  }
              At:
              <TimePicker
                    clearable
                    ampm={false}
                    label="24 hours"
                    value={this.state.scheduleDateTime}
                    onChange={(val: any) => this.setState({ scheduleDateTime: val })}
                  />
                Timezone:
                      <Select
                    labelId='select-timezone'
                    value={this.state.scheduleTimezone}
                    onChange={(e: any) => { this.setState({ scheduleTimezone: e.target.value }) }}
                  >
                    {timezones.map(val =>
                      <MenuItem key={val.timezone} value={val.timezone}>
                        <Box display='flex' flexDirection='column'>
                          <Box>{val.timezone}</Box>
                          <Box>{val.display}</Box>
                          <Box>{val.name}</Box>
                        </Box>
                      </MenuItem>
                    )}
                  </Select>
                </Box>
              </DialogContent>
              <DialogActions>
                <Button onClick={() => this.setState({ createScheduleOpen: false })} color="default">
                  Cancel
            </Button>
                <Button onClick={() => this.handleCreateSchedule()} color="primary">
                  Done
            </Button>
              </DialogActions>
            </Box>
          }
        </Dialog>
      </Sidebar>
    )
  }

  private renderRightToolbar() {
    if (this.state.deployed || this.state.testing) {
      return (
        <Sidebar style={{ right: 0, width: '25vw', height: '90%' }}>
          <Paper style={{ maxHeight: '100%', maxWidth: '100%', display: 'flex', flexDirection: 'column' }}>
            {this.state.currentRunId === "" || this.state.currentRun === null ?
              <Box m={1}>
                <Typography variant='h6'>
                  {(this.state.deployed && this.state.currentRunId === "") ?
                    "Please select a run to display its data."
                    :
                    (this.state.currentRun === null && this.state.deployed) ?
                      "Getting run info..."
                      :
                      (this.state.currentRun === null && this.state.testing) ?
                        "Running..."
                        :
                        "Something went wrong. Please reload."}
                </Typography>
              </Box>
              :
              this.renderRunOutputs()
            }
          </Paper>
        </Sidebar>
      )
    }
  }

  public render() {
    // TODO: Do not do this on every render
    this.updateCompletedNodes()

    return (
      <Page>
        <FlowChart
          chart={this.state.chart}
          callbacks={this.stateActions}
          config={{
            chart: this.state.chart,
            custom_readonly: this.state.deployed,
            readonly: this.state.deployed,
            chartUpdateCallback: this.chartUpdateCallback.bind(this),
            buildNode: this.buildNode.bind(this),
            flowId: this.state.flowId,
          }}
          Components={{ Node: FluxisNode, NodeInner: FluxisNodeInner, Port: FluxisPort, Ports: FluxisPorts }} />
        {this.renderLeftToolbar()}
        {this.renderRightToolbar()}
      </Page >
    )
  }
}

const mapDispatchToProps = (dispatch: any) => {
  return {
    alert_error: (message: string) => dispatch(alertActions.error(message))
  }
}

export default connect(null, mapDispatchToProps)(FlowBuild)