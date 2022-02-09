import React from 'react';
import { IBEShallowFlowRun } from "../core/@types";
import { makeStyles } from "@material-ui/core/styles";
import { Box } from "@material-ui/core";
import StatusBullet from "./StatusBullet";

type RunStatusProps = {
  run: IBEShallowFlowRun
}

const useStyles = makeStyles(theme => ({
  statusContainer: {
    display: 'flex',
    alignItems: 'center'
  },
}));


export default function RunStatus(props: RunStatusProps) {
  const classes = useStyles()

  const color: 'success' | 'danger' | 'info' = props.run.datetime_end === null ? 'info' : props.run.successful ? 'success' : 'danger'
  const mapToStatus = {
    'success': 'Succeeded',
    'danger': 'Failed',
    'info': 'Running'
  }


  return (
    <Box className={classes.statusContainer}>
      <StatusBullet color={color} size='sm' />
      <Box ml={1}>{mapToStatus[color]}</Box>
    </Box>
  )

}

