import React from 'react';
import { makeStyles } from "@material-ui/core/styles";
import { Grid } from '@material-ui/core';
import RunSummary from './RunSummary';


const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3)
  },
  content: {
    marginTop: theme.spacing(2)
  }
}));

export default function Dashboard() {
  const classes = useStyles();
  return (
    <div className={classes.root}>
      <Grid
        container
        spacing={4}
      >
        <Grid
          item
          xl={3}
          lg={6}
          md={8}
          sm={12}
          xs={12}
        >
          <RunSummary />
        </Grid>
        <Grid
          item
          xl={3}
          lg={6}
          md={12}
          sm={12}
          xs={12}
        >
          <div />
        </Grid>
        <Grid
          item
          xl={3}
          lg={6}
          md={12}
          sm={12}
          xs={12}
        >
          <div />
        </Grid>
        <Grid
          item
          xl={3}
          lg={6}
          md={12}
          sm={12}
          xs={12}
        >
          <div />
        </Grid>
        <Grid
          item
          xl={3}
          lg={6}
          md={12}
          sm={12}
          xs={12}
        >
          <div />
        </Grid>
        <Grid
          item
          xl={3}
          lg={6}
          md={12}
          sm={12}
          xs={12}
        >
          <div />
        </Grid>
        <Grid
          item
          xl={3}
          lg={6}
          md={12}
          sm={12}
          xs={12}
        >
          <div />
        </Grid>
        <Grid
          item
          xl={3}
          lg={6}
          md={12}
          sm={12}
          xs={12}
        >
          <div />
        </Grid>
      </Grid>
    </div>
  );
}