import styled, { css } from 'styled-components'
import { INode, INodeDefaultProps } from '@mrblenny/react-flow-chart'

export const FluxisNode = styled.div<INodeDefaultProps>`
  position: absolute;
  transition: 0.3s ease box-shadow, 0.3s ease margin-top;
  background: white;
  border-radius: 4px;
  min-width: 100px;
  min-height: 100px;
  ${(props) => props.isSelected && css`
    box-shadow: 0 10px 20px rgba(0,0,0,.4);
    margin-top: -2px
    `
  }
` as any


