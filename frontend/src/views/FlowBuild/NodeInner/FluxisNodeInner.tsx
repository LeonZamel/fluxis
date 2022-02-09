import * as React from 'react'
import styled from 'styled-components'
import { INode, INodeInnerDefaultProps } from '@mrblenny/react-flow-chart'
import TextField from '@material-ui/core/TextField';
import { Warning, Check, Close } from '@material-ui/icons';
import { Box, Tooltip } from '@material-ui/core';
import { IFluxisNode } from '../../../core/@types';
import _ from 'lodash';

const Outer = styled.div`
  padding: 15px 20px;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
`

const TextOutside = styled.div`
position: absolute;
top: -25px;
text-align: center;
width: 200%;
left: -50%;
`

export const FluxisNodeInner = ({ node }: INodeInnerDefaultProps) => {
  return (
    <Box style={{ height: 100 }}>
      <TextOutside>{node.properties.name}</TextOutside>
      <Outer>
        {node.properties.complete ? <Check /> : <Close />}
      </Outer>
    </Box>
  )
}
