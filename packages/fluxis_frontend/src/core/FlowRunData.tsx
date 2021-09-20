import { getFlowRunNodeData } from "./apiCalls";

export interface NodeData {
  ports: { [key: string]: PortData },
  hasData: boolean,
  loadingData: boolean,
}

export interface PortData {
  data: any,
  type: "tabular" | "string" | "number" | "object" | "boolean"
}

export class FlowRunData {
  constructor(runId: string) {
    this.runId = runId;
    this.nodes = {};
  }
  public runId: string;
  public nodes: { [key: string]: NodeData };
  /**
   * getPortData
   * @param nodeRunId nodeRunId of the node
   * @param portId Id/key of the port
   * @returns Data from the corresponding port from the run. Will be cached  
   */

  public static hasNodeData(runData: FlowRunData, nodeRunId: string): boolean {
    return (nodeRunId in runData.nodes && runData.nodes[nodeRunId].hasData)
  }

  public static isLoadingNodeData(runData: FlowRunData, nodeRunId: string): boolean {
    return (nodeRunId in runData.nodes && runData.nodes[nodeRunId].loadingData)
  }

  public static loadNodeData(flowRunId: string, nodeRunId: string): Promise<any> {
    return getFlowRunNodeData(" ", flowRunId, nodeRunId)
  }

  public static setLoadingNodeData(runData: FlowRunData, nodeRunId: string, loading: boolean): void {
    if (!(nodeRunId in runData.nodes)) {
      runData.nodes[nodeRunId] = {
        ports: {},
        hasData: true,
        loadingData: true,
      }
    } else {
      runData.nodes[nodeRunId].loadingData = true
    }
  }

  public static setNodeData(runData: FlowRunData, nodeRunId: string, data: any): void {
    runData.nodes[nodeRunId] = {
      ports: data,
      hasData: true,
      loadingData: false,
    }
  }
}