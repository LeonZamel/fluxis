import React from 'react';
import { withStyles, WithStyles } from '@material-ui/core/styles';

import { getAllFlowRuns } from '../core/apiCalls';

import { Table, TableHead, TableRow, TableCell, TableBody, Card } from '@material-ui/core';
import { IBEShallowFlowRun } from '../core/@types';
import { formatRunStart, formatRunDuration } from '../core/helpers';
import RunStatus from '../components/RunStatus';



const styles = (theme: any) => ({
  root: {
    padding: theme.spacing(3),
  },
});

interface IRunListProps extends WithStyles<typeof styles> {

}

interface IRunListState {
  runs: IBEShallowFlowRun[],
}

class RunList extends React.Component<IRunListProps, IRunListState> {
  constructor(props: IRunListProps) {
    super(props)
    this.state = {
      runs: [],
    }
  }

  componentDidMount() {
    getAllFlowRuns().then(res => {
      this.setState(
        {
          runs: res
        }
      )
    })
  }

  public render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <Card>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Flow name</TableCell>
                <TableCell>Run id</TableCell>
                <TableCell>Start</TableCell>
                <TableCell>Duration</TableCell>
                <TableCell>Nodes ran</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {
                this.state.runs.map(run => (
                  <TableRow key={run.id}>
                    <TableCell component="th" scope="row">
                      {run.flow.name}
                    </TableCell>
                    <TableCell>{run.id}</TableCell>
                    <TableCell>{formatRunStart(run)}</TableCell>
                    <TableCell>{formatRunDuration(run.datetime_start, run.datetime_end)}</TableCell>
                    <TableCell>{run.node_run_count}</TableCell>
                    <TableCell><RunStatus run={run} /></TableCell>
                  </TableRow>
                ))
              }

            </TableBody>
          </Table>
        </Card >
      </div >
    );
  }
}

export default withStyles(styles)(RunList);