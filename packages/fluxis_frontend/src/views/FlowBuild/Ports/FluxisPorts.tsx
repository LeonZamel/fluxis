import * as React from 'react'
import { FluxisPortsGroup } from './FluxisPortsGroup';
import { IPortsDefaultProps } from '@mrblenny/react-flow-chart';


export const FluxisPorts = ({ children }: IPortsDefaultProps) => {
  return (
    <div>
      <FluxisPortsGroup side="left-top">
        {children.filter((child) => child.props.port.type === 'input' && child.props.port.id !== "trigger")}
      </FluxisPortsGroup>
      <FluxisPortsGroup side="right-top">
        {children.filter((child) => ['output'].includes(child.props.port.type))}
      </FluxisPortsGroup>
      <FluxisPortsGroup side="left">
        {children.filter((child) => child.props.port.type === 'input' && child.props.port.id === "trigger")}
      </FluxisPortsGroup>

      <FluxisPortsGroup side="right">
        {children.filter((child) => ['right'].includes(child.props.port.type))}
      </FluxisPortsGroup>
      <FluxisPortsGroup side="left">
        {children.filter((child) => ['left'].includes(child.props.port.type))}
      </FluxisPortsGroup>
    </div>
  )
}