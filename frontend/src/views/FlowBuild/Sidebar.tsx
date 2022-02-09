import * as React from 'react';
import { makeStyles, Paper } from "@material-ui/core";

const useStyles = makeStyles(theme => ({
  root: {
    width: '250px',
    maxHeight: '100vh',
    position: 'absolute',
    margin: theme.spacing(1),
    display: 'flex',
    flexDirection: 'column',
  }
}));

export default function Sidebar(props: any) {
  const classes = useStyles();
  const { style } = props;

  return (
    <div className={classes.root} style={style}>
      {props.children}
    </div>
  )
}