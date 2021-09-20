import * as React from 'react';
import { Popover, Button, makeStyles, CardActions, CardContent, Card, Divider } from "@material-ui/core";


const useStyles = makeStyles(theme => ({
  container: {
    width: '98vw',
    height: '96vh',
  },
  actions: {
    justifyContent: 'flex-end'
  },
  content: {
    padding: 0,
    height: '100%',
    width: '100%',
    overflow: 'auto'
  }
}));

export default function DataOverlay(props: any) {
  const classes = useStyles();

  return (
    <Popover
      style={{ margin: "0" }}
      open={props.open}
    >
      <Card className={classes.container}>
        <CardActions className={classes.actions}>
          <Button onClick={props.closeAction} variant="contained" size='small' color="primary">Close</Button>
        </CardActions>
        <Divider />
        <CardContent className={classes.content}>
          {props.children}
        </CardContent>
      </Card>
    </ Popover>
  )
}