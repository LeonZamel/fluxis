import * as React from 'react'
import styled from 'styled-components'
import { REACT_FLOW_CHART } from '@mrblenny/react-flow-chart'

const Outer = styled.div`
  padding: 15px 15px;
  font-size: 14px;
  background: white;
  cursor: move;
`

export interface ISidebarItemProps {
  type: string,
  properties?: any,
}

export const SidebarNodeItem = ({ type, properties }: ISidebarItemProps) => {
  return (
    <Outer
      draggable={true}
      onDragStart={(event: any) => {
        event.dataTransfer.setData(REACT_FLOW_CHART, JSON.stringify({ type }))
      }}
    >
      {properties.name}
    </Outer>
  )
}
