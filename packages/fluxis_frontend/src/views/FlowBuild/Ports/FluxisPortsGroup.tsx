import styled, { css } from 'styled-components'
import { IPortsGroupDefaultProps } from '@mrblenny/react-flow-chart'

export interface IFluxisPortsGroupProps {
  side: "left-top" | "right-top" | IPortsGroupDefaultProps["side"]
}

export const FluxisPortsGroup = styled.div<IFluxisPortsGroupProps>`
  position: absolute;
  display: flex;
  justify-content: center;
  ${(props) => {
    if (props.side === 'top') {
      return css`
        width: 100%;
        left: 0;
        top: -12px;
        flex-direction: row;
        > div {
          margin: 0 3px;
        }
      `
    } else if (props.side === 'bottom') {
      return css`
        width: 100%;
        left: 0;
        bottom: -12px;
        flex-direction: row;
        > div {
          margin: 0 3px;
        }
      `
    } else if (props.side === 'left') {
      return css`
        height: 100%;
        top: 0;
        left: -12px;
        flex-direction: column;
        > div {
          margin: 3px 0;
        }
      `
    } else if (props.side === 'right') {
      return css`
        height: 100%;
        top: 0;
        right: -12px;
        flex-direction: column;
        > div {
          margin: 3px 0;
        }
      `
    } else if (props.side === 'left-top') {
      return css`
      height: 100%;
        top: 0;
        left: -6px;
        flex-direction: column;
        > div {
          margin: 3px 0;
        }
      `
    } else if (props.side === 'right-top') {
      return css`
      height: 100%;
      top: 0;
      right: -6px;
      flex-direction: column;
      > div {
        margin: 3px 0;
      }
      `
    }
  }}
`