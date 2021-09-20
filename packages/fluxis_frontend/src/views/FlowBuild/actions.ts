import { v4 } from 'uuid'
import {
  IChart, identity, IOnCanvasClick,
  IOnCanvasDrop, IOnDeleteKey, IOnDragCanvas, IOnDragCanvasStop,
  IOnDragNode, IOnDragNodeStop, IOnLinkCancel, IOnLinkComplete, IOnLinkMouseEnter, IOnLinkMouseLeave, IOnLinkMove,
  IOnLinkStart, IOnNodeClick, IOnNodeMouseEnter,
  IOnNodeMouseLeave, IOnNodeSizeChange, IOnPortPositionChange, IStateCallback, IOnNodeDoubleClick, IOnZoomCanvas
} from '@mrblenny/react-flow-chart'
import { rotate } from '../../utils/rotate'
import { convertNodeF2B, convertLinkF2B, convertFlowF2B } from '../../core/@types.convert'
import { sendCreateNode, sendCreateLink, sendMoveNode, sendDeleteNode, sendDeleteLink } from '../../core/apiCalls'
import { alertActions } from '../../store/actions/alert.actions'
import { IFluxisChart } from '../../core/@types'

function getOffset(config: any, data: any, zoom?: number) {
  let offset = { x: data.x, y: data.y }
  if (config && config.snapToGrid) {
    offset = {
      x: Math.round(data.x / 20) * 20,
      y: Math.round(data.y / 20) * 20,
    }
  }
  if (zoom) {
    offset.x = offset.x / zoom
    offset.y = offset.y / zoom
  }
  return offset
}

/**
 * This file contains actions for updating state after each of the required callbacks
 */

export const onDragNode: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnDragNode> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ config, event, data, id }) => (chart: IChart) => {
  const nodechart = chart.nodes[id]

  if (nodechart) {
    const delta = {
      x: data.deltaX,
      y: data.deltaY,
    }
    chart.nodes[id] = {
      ...nodechart,
      position: {
        x: nodechart.position.x + delta.x,
        y: nodechart.position.y + delta.y,
      },
    }
  }

  return chart
}

export const onDragNodeStop: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnDragNodeStop> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ config, event, data, id }) => (chart: IChart): IChart => {
  const node = chart.nodes[id]
  if (node) {
    node.position = {
      x: Math.round(data.x),
      y: Math.round(data.y),
    }
    //sendUpdateFlow(flowId, convertFlowF2B(chart as IFluxisChart, flowId))
    sendMoveNode(id, data.x, data.y, flowId)
  }
  return chart
}

export const onDragCanvas: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnDragCanvas> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ config, data }) => (chart: IChart): IChart => {
  chart.offset = getOffset(config, { x: data.positionX, y: data.positionY })
  return chart
}

export const onDragCanvasStop: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnDragCanvasStop> = (chartUpdateCallback: any, buildNode: any, flowId: string) => () => identity

export const onLinkStart: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnLinkStart> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ linkId, fromNodeId, fromPortId }) => (chart: IChart): IChart => {
  /*
  chart.links[linkId] = {
    id: linkId,
    from: {
      nodeId: fromNodeId,
      portId: fromPortId,
    },
    to: {},
  }
  return chart
  */

  // Make sure we can only start links from non constant ports
  if (chart.nodes[fromNodeId].ports[fromPortId].properties.constant_value == undefined ||
    !chart.nodes[fromNodeId].ports[fromPortId].properties.constant_value!.enabled) {
    chart.links[linkId] = {
      id: linkId,
      from: {
        nodeId: fromNodeId,
        portId: fromPortId,
      },
      to: {},
    }
  }
  return chart
}

export const onLinkMove: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnLinkMove> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ linkId, toPosition }) => (chart: IChart): IChart => {
  if (chart.links[linkId] !== undefined) {
    const link = chart.links[linkId]
    link.to.position = toPosition
    chart.links[linkId] = { ...link }
  }
  return chart
}

export const onLinkComplete: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnLinkComplete> = (chartUpdateCallback: any, buildNode: any, flowId: string) => (props) => {
  const { linkId, fromNodeId, fromPortId, toNodeId, toPortId, config = {} } = props
  /*
  return (chart: IChart): IChart => {
    if (!config.readonly && (config.validateLink ? config.validateLink({ ...props, chart }) : true) && [fromNodeId, fromPortId].join() !== [toNodeId, toPortId].join()) {
      chart.links[linkId].to = {
        nodeId: toNodeId,
        portId: toPortId,
      }
    } else {
      delete chart.links[linkId]
    }
    return chart
  }
  */
  return (chart: IChart): IChart => {
    // Link might be undefined if tried to be created from a port with constant value
    if (chart.links[linkId] !== undefined && fromNodeId !== toNodeId) {
      let fnId = chart.links[linkId].from.nodeId
      let fpId = chart.links[linkId].from.portId
      let fp = chart.nodes[fnId].ports[fpId]
      let tp = chart.nodes[toNodeId].ports[toPortId]
      let resp: Promise<string | null> | undefined = undefined
      if (fnId !== toNodeId && (tp.properties.constant_value == undefined || !tp.properties.constant_value!.enabled)) {
        if (fp.type === "output" && tp.type === "input") {
          chart.links[linkId].to = {
            nodeId: toNodeId,
            portId: toPortId,
          }
          resp = sendCreateLink(convertLinkF2B(chart.links[linkId], "dummy-" + v4()), flowId)
        }
        else if (fp.type === "input" && tp.type === "output") {
          chart.links[linkId].to = chart.links[linkId].from
          chart.links[linkId].from = {
            nodeId: toNodeId,
            portId: toPortId,
          }
          resp = sendCreateLink(convertLinkF2B(chart.links[linkId], "dummy-" + v4()), flowId)
        } else {
          return chart
        }
        resp!.then(recId => {
          if (recId !== null) {
            chart.links[recId] = chart.links[linkId]
            chart.links[recId].id = recId
            delete chart.links[linkId]
            chartUpdateCallback(chart)
          } else {
            delete chart.links[linkId]
            chartUpdateCallback(chart)
          }
        })
      }
      return chart
    } else {
      delete chart.links[linkId]
      return chart
    }
  }
}

export const onLinkCancel: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnLinkCancel> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ linkId }) => (chart: IChart) => {
  delete chart.links[linkId]
  return chart
}

export const onLinkMouseEnter: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnLinkMouseEnter> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ linkId }) => (chart: IChart) => {
  // Set the link to hover
  const link = chart.links[linkId]
  // Set the connected ports to hover
  if (link.to.nodeId && link.to.portId) {
    if (chart.hovered.type !== 'link' || chart.hovered.id !== linkId) {
      chart.hovered = {
        type: 'link',
        id: linkId,
      }
    }
  }
  return chart
}

export const onLinkMouseLeave: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnLinkMouseLeave> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ linkId }) => (chart: IChart) => {
  const link = chart.links[linkId]
  // Set the connected ports to hover
  if (link.to.nodeId && link.to.portId) {
    chart.hovered = {}
  }
  return chart
}

export const onLinkClick: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnLinkMouseLeave> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ linkId }) => (chart: IChart) => {
  if (chart.selected.id !== linkId || chart.selected.type !== 'link') {
    chart.selected = {
      type: 'link',
      id: linkId,
    }
  }
  return chart
}

export const onCanvasClick: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnCanvasClick> = (chartUpdateCallback: any, buildNode: any, flowId: string) => () => (chart: IChart) => {
  if (chart.selected.id) {
    chart.selected = {}
  }
  return chart
}

export const onNodeMouseEnter: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnNodeMouseEnter> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ nodeId }) => (chart: IChart) => {
  return {
    ...chart,
    hovered: {
      type: 'node',
      id: nodeId,
    },
  }
}

export const onNodeMouseLeave: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnNodeMouseLeave> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ nodeId }) => (chart: IChart) => {
  if (chart.hovered.type === 'node' && chart.hovered.id === nodeId) {
    return { ...chart, hovered: {} }
  }
  return chart
}

export const onDeleteKey: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnDeleteKey> = (chartUpdateCallback: any, buildNode: any, flowId: string) => () => (chart: IChart) => {
  if (chart.selected.type === 'node' && chart.selected.id) {
    const node = chart.nodes[chart.selected.id]
    // Delete the connected links
    Object.keys(chart.links).forEach((linkId) => {
      const link = chart.links[linkId]
      if (link.from.nodeId === node.id || link.to.nodeId === node.id) {
        delete chart.links[link.id]
      }
    })
    // Delete the node
    delete chart.nodes[chart.selected.id]
    sendDeleteNode(chart.selected.id, flowId)
  } else if (chart.selected.type === 'link' && chart.selected.id) {
    delete chart.links[chart.selected.id]
    sendDeleteLink(chart.selected.id, flowId)
  }
  chart.selected = {}
  return chart
}

export const onNodeClick: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnNodeClick> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ nodeId }) => (chart: IChart) => {
  if (chart.selected.id !== nodeId || chart.selected.type !== 'node') {
    chart.selected = {
      type: 'node',
      id: nodeId,
    }
  }
  return chart
}

export const onNodeSizeChange: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnNodeSizeChange> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ nodeId, size }) => (chart: IChart) => {
  chart.nodes[nodeId] = {
    ...chart.nodes[nodeId],
    size,
  }
  return chart
}

export const onPortPositionChange: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnPortPositionChange> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ node: nodeToUpdate, port, el, nodesEl }) =>
  (chart: IChart): IChart => {
    if (nodeToUpdate.size) {
      // rotate the port's position based on the node's orientation prop (angle)
      const center = { x: nodeToUpdate.size.width / 2, y: nodeToUpdate.size.height / 2 }
      const current = { x: el.offsetLeft + nodesEl.offsetLeft + el.offsetWidth / 2, y: el.offsetTop + nodesEl.offsetTop + el.offsetHeight / 2 }
      const angle = nodeToUpdate.orientation || 0
      const position = rotate(center, current, angle)

      const node = chart.nodes[nodeToUpdate.id]
      node.ports[port.id].position = {
        x: position.x,
        y: position.y,
      }

      chart.nodes[nodeToUpdate.id] = { ...node }
    }
    return chart
  }

export const onCanvasDrop: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnCanvasDrop> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ config, data, position }) => (chart: IChart): IChart => {
  let dummy = buildNode(data.type, "dummy-" + v4())
  dummy.position = { x: Math.round(position.x), y: Math.round(position.y) }
  chart.nodes[dummy.id] = dummy
  var beNode = convertNodeF2B(dummy);
  sendCreateNode(beNode, flowId).then((recId) => {
    // Delete the dummy, either replaced with new node, or none
    delete chart.nodes[dummy.id]
    if (recId !== null) {
      // We need to rebuild the node with the actual id so all the parameter callbacks work
      let finalNode = buildNode(data.type, recId)
      finalNode.position = position
      chart.nodes[recId] = finalNode
      chartUpdateCallback(chart)
    } else {
      alertActions.error("Couldn't create node")
      chartUpdateCallback(chart)
    }
  })
  return chart
}

export const onNodeDoubleClick: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnNodeDoubleClick> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ nodeId }) => (chart: IChart) => {
  if (chart.selected.id !== nodeId || chart.selected.type !== 'node') {
    chart.selected = {
      type: 'node',
      id: nodeId,
    }
  }
  return chart
}

export const onZoomCanvas: (chartUpdateCallback: any, buildNode: any, flowId: string) => IStateCallback<IOnZoomCanvas> = (chartUpdateCallback: any, buildNode: any, flowId: string) => ({ config, data }) => (
  chart: IChart,
): IChart => {
  /* TODO: Add this, currently buggy */
  /*
  if (data) {
    chart.offset = getOffset(config, { x: data.positionX, y: data.positionY })
    chart.scale = data.scale
  }
  */
  return chart
}
