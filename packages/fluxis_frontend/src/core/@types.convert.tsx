import { IBENodeDef, INodeDef, IPortDef, IParameterDef, IBELink, IBENode, IBEPort, IFluxisNode, IFluxisPort, IBEParameter, IParameters, IFluxisPorts, IPortDefs, IParameterDefs, IFluxisChart, IBEFlow, IFluxisNodes, IFluxisLinks, IFluxisLink, IBENodes, IBELinks } from './@types'
import { INode, IChart, ILink } from '@mrblenny/react-flow-chart'

export function convertNodeDefB2F(key: string, nodeDef: IBENodeDef): INodeDef {
  let in_ports: IPortDefs = {}
  let out_ports: IPortDefs = {}
  let parameters: IParameterDefs = {}

  nodeDef.in_ports.forEach(bePortDef => {
    in_ports[bePortDef.key] = bePortDef
  })

  nodeDef.out_ports.forEach(bePortDef => {
    out_ports[bePortDef.key] = bePortDef
  })

  nodeDef.parameters.forEach(beParameterDef => {
    parameters[beParameterDef.key] = beParameterDef
  })

  return {
    key,
    name: nodeDef.name,
    is_trigger_node: nodeDef.is_trigger_node,
    category: nodeDef.category,
    in_ports,
    out_ports,
    parameters,
    credentials: nodeDef.credentials,
  }
}


export function convertNodeF2B(node: IFluxisNode, id?: string): IBENode {
  var ret: IBENode = {
    id: id ? id : '_',
    name: node.properties.name,
    x: node.position.x,
    y: node.position.y,
    function: node.type,
    in_ports: [],
    out_ports: [],
    parameters: [],
    credentials: node.properties.credentials
  }
  for (var port_id in node.ports) {
    let p = node.ports[port_id]
    let port: IBEPort = {
      key: p.id,
      node: node.id,
    }
    if (p.type === 'input') {
      ret.in_ports.push(port)
    } else if (p.type === 'output') {
      ret.out_ports.push(port)
    } else {
      console.error(`Port has type ${p.type}, which cannot be resolved`)
    }
  }
  return ret
}

export function convertNodeB2F(be_node: IBENode, nodeDef: INodeDef): IFluxisNode {
  // We need the nodeDef to give the node its port names
  var ret: IFluxisNode = {
    id: be_node.id,
    ports: convertPortsB2F(be_node.in_ports, be_node.out_ports, nodeDef, be_node.trigger_port),
    type: be_node.function,
    properties: {
      name: be_node.name,
      parameters: convertParametersB2F(be_node.parameters),
      complete: false,
      credentials: be_node.credentials
    },
    position: { x: be_node.x, y: be_node.y }
  }
  return ret
}


export function convertParametersB2F(be_parameters: IBEParameter[]): IParameters {
  let ret: IParameters = {}
  be_parameters.forEach((element: IBEParameter) => {
    ret[element.key] = element
  });
  return ret
}


export function convertLinkF2B(link: ILink, id: string): IBELink {
  return {
    id,
    from_port: {
      node: link.from.nodeId!,
      key: link.from.portId!
    },
    to_port: {
      node: link.to.nodeId!,
      key: link.to.portId!
    }
  }
}

export function convertPortsB2F(be_in_ports: IBEPort[], be_out_ports: IBEPort[], nodeDef: INodeDef, trigger_port?: IBEPort): IFluxisPorts {
  let ret: IFluxisPorts = {}
  be_in_ports.forEach((be_in_port: IBEPort) => {
    ret[be_in_port.key] = convertPortB2F(be_in_port, 'input', nodeDef.in_ports[be_in_port.key].name)
  });
  if (trigger_port != null) {
    ret[trigger_port!.key] = convertPortB2F(trigger_port!, 'input', 'Trigger')
  }
  be_out_ports.forEach((be_out_port: IBEPort) => {
    ret[be_out_port.key] = convertPortB2F(be_out_port, 'output', nodeDef.out_ports[be_out_port.key].name)
  });
  return ret
}

export function convertPortF2B(port: IFluxisPort, nodeId: string): IBEPort {
  let ret: IBEPort = {
    key: port.properties.key,
    node: nodeId,
  }

  // We only want to add a constant value if it's an input port
  if (port.type === 'input') {
    // If the constant value is disabled we don't send it to the backend, because it will be null in the database
    if (port.properties.constant_value!.enabled) {
      ret.constant_value = { value: port.properties.constant_value!.value }
    }
  }

  return ret;
}

export function convertPortB2F(port: IBEPort, type: "input" | "output", portName: string): IFluxisPort {
  let ret: IFluxisPort = {
    id: port.key,
    type: type,
    properties: {
      key: port.key,
      name: portName,
      constant_value: port.constant_value == undefined ? { value: undefined, enabled: false } : { value: port.constant_value!.value, enabled: true }
    }
  }
  return ret;
}

export function convertNodesF2B(nodes: IFluxisNodes): IBENodes {
  return Object.entries(nodes).map(([nodeId, node]) => convertNodeF2B(node, nodeId))
}

export function convertEdgesF2B(edges: IFluxisLinks): IBELinks {
  return Object.entries(edges).map(([edgeId, edge]) => convertLinkF2B(edge, edgeId))
}

export function convertFlowF2B(chart: IFluxisChart, flowId: string, deployed: boolean): IBEFlow {
  return {
    id: flowId,
    nodes: convertNodesF2B(chart.nodes),
    edges: convertEdgesF2B(chart.links),
    deployed
  }
}