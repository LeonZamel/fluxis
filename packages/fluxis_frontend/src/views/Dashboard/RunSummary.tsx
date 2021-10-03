import React, { useState, useEffect } from 'react';
import { makeStyles } from "@material-ui/core/styles";
import { Table, TableHead, TableRow, TableCell, TableBody, Card, CardHeader, CardContent, Divider, Button, CardActions, CircularProgress, Box } from '@material-ui/core';
import { getAllFlowRuns } from '../../core/apiCalls';
import { IBEShallowFlowRun } from '../../core/@types';
import { ArrowRight } from '@material-ui/icons';
import { Link } from 'react-router-dom';
import { formatRunStart } from '../../core/helpers';
import RunStatus from '../../components/RunStatus';


const useStyles = makeStyles(theme => ({
  root: {
    height: '100%'
  },
  content: {
    padding: 0
  },
  actions: {
    justifyContent: 'flex-end'
  }
}));

type IBEShallowFlowRunArray = IBEShallowFlowRun[]

export default function RunSummary() {
  const classes = useStyles();
  const [runs, setRuns] = useState<IBEShallowFlowRunArray>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAllFlowRuns()
      .then(resp => {
        setRuns(resp.data.slice(0, 5))
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return (
    <Card className={classes.root}>
      <CardHeader title="Latest runs" action={
        loading && <CircularProgress />} />
      <Divider />
      <CardContent className={classes.content}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Flow name</TableCell>
              <TableCell>Run start</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {runs.map((run: IBEShallowFlowRun) => (
              <TableRow key={run.id}>
                <TableCell component="th" scope="row">
                  {run.flow.name}
                </TableCell>
                <TableCell>{formatRunStart(run)}</TableCell>
                <TableCell>
                  <RunStatus run={run} />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
      <CardActions className={classes.actions}>
        <Button
          color="primary"
          size="small"
          variant="text"
          component={Link} to="/runs/"
        >
          View all <ArrowRight />
        </Button>
      </CardActions>
    </Card>
  );
}