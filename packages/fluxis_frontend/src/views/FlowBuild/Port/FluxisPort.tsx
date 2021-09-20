import * as React from 'react'
import styled from 'styled-components'
import { IPortDefaultProps, ILink, IChart } from '@mrblenny/react-flow-chart'
import { Grid, Tooltip, Box } from '@material-ui/core';
import { KeyboardArrowDown, Check, KeyboardArrowRight } from '@material-ui/icons';

const PortDefaultOuter = styled.div`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: white;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  &:hover > div {
    background: cornflowerblue;
  }
`

const PortDefaultInner = styled.div<{ active: boolean }>`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background:  ${(props) => props.active ? 'cornflowerblue' : 'grey'};
  cursor: pointer;
`

const Label = styled.div`
  position: absolute;
  background: white;
  padding: 1px 1px;
  border-radius: 4px;
`

const LabelContent = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  font-size: 12px;
  cursor: pointer;
  text-overflow: ellipsis;
  white-space: nowrap;
`

export const FluxisPort = ({ isLinkSelected, isLinkHovered, config, isHovered, isSelected, ...props }: IPortDefaultProps) => {
  const hovering = config!.chart.hovered.id
  const chart: IChart = config!.chart
  const currentlyMakingLink = Object.values(chart.links).find((link: ILink) => link.to.nodeId === undefined)

  if (!props.port.properties.constant_value || !props.port.properties.constant_value.enabled) {
    return (
      <Box>
        {
          (isLinkHovered || isHovered || isLinkSelected || isSelected || hovering || currentlyMakingLink) &&
          <Label style={{ right: (props.port.type === 'input' ? 22 : ''), left: (props.port.type === 'input' ? '' : 22) }}><LabelContent>{props.port.properties.name}</LabelContent></Label>
        }
        <PortDefaultOuter>
          <PortDefaultInner
            active={!config.readonly && (isLinkSelected || isLinkHovered)}
          />
        </PortDefaultOuter>

      </Box>
    )
  } else {
    return (
      <Box height='12px'></Box>
    )
  }
}

// width: 24px;
// height: 24px;

/*

<svg style={{ width: '24px', height: '24px' }} viewBox="0 0 24 24">
          <path fill="white" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
        </svg>

*/
/*
export const FluxisPort = (props: IPortDefaultProps) => (
  <div>
    {props.port.properties && props.port.properties.value === 'yes' && (
      <svg style={{ width: '24px', height: '24px' }} viewBox="0 0 24 24">
        <path fill="white" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
      </svg>
    )}
    {props.port.properties && props.port.properties.value === 'no' && (
      <svg style={{ width: '24px', height: '24px' }} viewBox="0 0 24 24">
        <path fill="white" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
      </svg>
    )}

    { // Actually used
      props.port.properties && props.port.properties.key && props.port.id !== 'trigger' && (!props.port.properties.constant_value || !props.port.properties.constant_value.enabled) && (
        <PortDefaultOuter>
          <Tooltip title={props.port.properties.name}>
            <Grid
              container
              direction="row"
              justify="center"
              alignItems="center"
            >
              <KeyboardArrowDown />
            </Grid>
          </Tooltip>
        </PortDefaultOuter>
      )
    }

    {// Actually used, this is so a port with a constant value becomes invisible
      props.port.properties && props.port.properties.key && (props.port.properties.constant_value && props.port.properties.constant_value.enabled) && (
        <span style={{ margin: '17px' }}></span>
      )
    }

    {// Actually used, for the trigger port
      props.port.properties && props.port.properties.key && props.port.id === 'trigger' && (
        <PortDefaultOuter>
          <Tooltip title={props.port.properties.name}>
            <Grid
              container
              direction="row"
              justify="center"
              alignItems="center"
            >
              <KeyboardArrowRight />
            </Grid>
          </Tooltip>
        </PortDefaultOuter>
      )
    }


    {!props.port.properties && (
      <svg style={{ width: '24px', height: '24px' }} viewBox="0 0 24 24">
        <path fill="white" d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" />
      </svg>
    )}
  </div>
)

*/