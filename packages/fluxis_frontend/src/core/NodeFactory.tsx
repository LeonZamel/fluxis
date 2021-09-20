import { INodeDef, IFluxisNode, IParameters, IFluxisPort, InputDataType } from "./@types";
import { IPort, IPosition } from "@mrblenny/react-flow-chart";
import _ from "lodash";

export const must_have_trigger_port_by_def = function (def: INodeDef): boolean {
  return (_.isEmpty(def.in_ports) && !def.is_trigger_node)
}

export const must_have_trigger_port = function (def: INodeDef, node: IFluxisNode): boolean {
  // Must have by def or no input ports without constant val
  return must_have_trigger_port_by_def(def) || _.isEmpty(_.pickBy(node.ports, (val) => (val.type === 'input' && val.id !== 'trigger' && (val.properties.constant_value === undefined || !val.properties.constant_value.enabled))))
}

/*
If this is used again, check the type definition and use IFluxisTriggerPort

export const create_trigger_port = function (ports: { [key: string]: IFluxisTriggerPort }) {
  ports["trigger"] = {
    id: "trigger",
    type: "input",
    properties: {
      key: "trigger",
      name: 'Trigger',
    },
  }
}
*/

export const NodeFactory = function (def: INodeDef, id: string): IFluxisNode {
  var name = def.name
  var node: IFluxisNode
  var ports: {
    [id: string]: IFluxisPort,
  } = {}

  var ports: { [key: string]: IFluxisPort } = {}
  for (var in_port in def.in_ports) {
    ports[in_port] = {
      id: in_port,
      type: 'input',
      properties: {
        key: in_port,
        name: def.in_ports[in_port].name,
        constant_value: {
          value: undefined,
          enabled: false,
        },
      }
    }
  }

  /*
  if (must_have_trigger_port_by_def(def)) {
    create_trigger_port(ports)
  }
  */

  for (var out_port in def.out_ports) {
    ports[out_port] = {
      id: out_port,
      type: 'output',
      properties: {
        key: out_port,
        name: def.out_ports[out_port].name,
      }
    }
  }

  var position: IPosition = {
    x: 0,
    y: 0,
  }
  node = {
    id,
    type: def.key,
    position: position,
    ports: ports,
    properties: {
      name: name,
      parameters: {},
      complete: false,
    }
  }

  var parameters: IParameters = {}
  for (let parameter in def.parameters) {
    // TODO: Type shoud be considered
    parameters[parameter] = {
      key: parameter,
      data_type: def.parameters[parameter].data_type,
      value: def.parameters[parameter].default_value,
    }
  }

  node.properties.parameters = parameters

  return node;
}