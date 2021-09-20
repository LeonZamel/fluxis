import React from 'react';
import { withStyles, WithStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { getAllTriggers, sendCreateHttpEndpointTrigger, sendCreateTimerTrigger } from '../core/apiCalls';
import Fab from '@material-ui/core/Fab';
import { Add } from '@material-ui/icons';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { Link } from 'react-router-dom';
import { FormControl, InputLabel, Select, MenuItem, Container } from '@material-ui/core';

const styles = (theme: any) => ({
  root: {
    width: '100%',
    backgroundColor: theme.palette.background.paper,
  },
  fab: {
    margin: theme.spacing.unit,
  },
});

function ListItemLink(props: any) {
  return <ListItem button component="a" {...props} />;
}

interface ITriggerListProps extends WithStyles<typeof styles> {

}

interface ITriggerListState {
  triggers: any[],
  dialogOpen: boolean,
  createTriggerName: string,
  triggerTypes: string[],


  createTriggerType: string,
  httpEndpointPath: string,
  timerInterval: number,
  timerRepetitions: number,
}

class TriggerList extends React.Component<ITriggerListProps, ITriggerListState> {
  constructor(props: ITriggerListProps) {
    super(props)
    this.state = {
      triggers: [],
      dialogOpen: false,
      createTriggerName: "",
      triggerTypes: ["Http Endpoint", "Timer"],
      createTriggerType: "",
      httpEndpointPath: "",
      timerInterval: 100,
      timerRepetitions: 100,
    }
  }

  handleTriggerNameChange = (e: any) => {
    this.setState({ createTriggerName: e.target.value });
  }

  handleHttpEndpointPathChange = (e: any) => {
    this.setState({ httpEndpointPath: e.target.value });
  }

  handleTimerIntervalChange = (e: any) => {
    this.setState({ timerInterval: e.target.value });
  }

  handleTimerRepetitionsChange = (e: any) => {
    this.setState({ timerRepetitions: e.target.value });
  }

  handleClickOpen = () => {
    this.setState({ dialogOpen: true });
  };

  handleClose = () => {
    this.setState({ dialogOpen: false });
  };

  handleCreate = () => {
    if (this.state.createTriggerType != "") {
      let resp;
      switch (this.state.createTriggerType) {
        case 'Http Endpoint':
          resp = sendCreateHttpEndpointTrigger(this.state.createTriggerName, this.state.httpEndpointPath)
          break;
        case "Timer":
          resp = sendCreateTimerTrigger(this.state.createTriggerName, this.state.timerInterval, this.state.timerRepetitions)
          break;
        default: return;
      }
      resp.then(res => {
        this.setState({ triggers: [...this.state.triggers, res.data] })
        this.setState({ dialogOpen: false });
      }).catch()

      /*
      sendCreateTrigger(this.state.createTriggerType, this.state.).then((res) => {
        this.setState({ flows: [...this.state.flows, res.data] })
      })
      */
    }
  };

  componentDidMount() {
    getAllTriggers().then(res => {
      this.setState(
        {
          triggers: res.data
        }
      )
    })
  }

  renderTriggerForm() {
    switch (this.state.createTriggerType) {
      case 'Http Endpoint':
        return (
          <TextField
            autoFocus
            margin="dense"
            id="httpEndpointPath"
            label="Path"
            type="text"
            fullWidth
            value={this.state.httpEndpointPath}
            onChange={this.handleHttpEndpointPathChange}
          />
        );
      case "Timer":
        return (
          <div>
            <TextField
              autoFocus
              margin="dense"
              id="timerInterval"
              label="Interval"
              type="number"
              fullWidth
              value={this.state.timerInterval}
              onChange={this.handleTimerIntervalChange}
            />
            <TextField
              autoFocus
              margin="dense"
              id="timerRepetitions"
              label="Repetitions"
              type="number"
              fullWidth
              value={this.state.timerRepetitions}
              onChange={this.handleTimerRepetitionsChange}
            />
          </div>
        );
      default: return;
    }
  }

  public render() {
    const { classes } = this.props;
    return (
      <div >
        <Container>
          <List component="nav">
            {this.state.triggers.map((trigger: any) => {
              return (
                <ListItem button={true}>
                  <ListItemText key={trigger.id} primary={trigger.name} secondary={trigger.id} />
                </ListItem>
              )
            })}
          </List>
          <Fab color="primary" aria-label="Add" className={classes.fab} onClick={this.handleClickOpen}>
            <Add />
          </Fab>
        </Container>
        <div>
          <Dialog
            open={this.state.dialogOpen}
            onClose={this.handleClose}
            aria-labelledby="form-dialog-title"
          >
            <DialogTitle id="form-dialog-title">Create new Trigger</DialogTitle>
            <DialogContent>
              <TextField
                autoFocus
                margin="dense"
                id="name"
                label="Name"
                type="text"
                fullWidth
                value={this.state.createTriggerName}
                onChange={this.handleTriggerNameChange}
              />
              <FormControl fullWidth>
                <InputLabel htmlFor="trigger-type">Trigger type</InputLabel>
                <Select fullWidth
                  id="trigger-type"
                  value={this.state.createTriggerType}
                  onChange={(e: any) => this.setState({ createTriggerType: e.target.value })}
                >
                  {this.state.triggerTypes.map((entry, id) =>
                    <MenuItem key={entry} value={entry}>{entry}</MenuItem>
                  )}
                </Select>
              </FormControl>
              {this.renderTriggerForm()}
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleClose} color="primary">
                Cancel
            </Button>
              <Button onClick={this.handleCreate} color="primary">
                Create
            </Button>
            </DialogActions>
          </Dialog>
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(TriggerList);