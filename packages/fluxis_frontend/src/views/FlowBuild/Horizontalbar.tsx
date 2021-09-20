import * as React from 'react';
import { makeStyles, Paper } from "@material-ui/core";

const useStyles = makeStyles(theme => ({
  root: {
    position: 'absolute',
    margin: theme.spacing(1),
    padding: theme.spacing(1),
    left: '210px',
    flexDirection: 'row',
    display: 'flex',
    alignItems: 'center',
    height: '10%'
  }
}));

export default function Horizontalbar(props: any) {
  const classes = useStyles();

  return (
    <Paper className={classes.root}>
      {props.children}
    </Paper>
  )
}