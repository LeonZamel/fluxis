import React, { Component } from 'react';
import { Router, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import FlowList from './views/FlowList/FlowList';
import { FlowFluxisRouter } from './routes';
import { userActions } from './store/actions/user.actions';
import { history } from './core/history';
import { createMuiTheme, SimplePaletteColorOptions, MuiThemeProvider } from '@material-ui/core/styles';
import { ThemeProvider } from 'styled-components';
import { Snackbar, SnackbarContent, Button } from '@material-ui/core';
import { Close } from '@material-ui/icons';
import { MuiPickersUtilsProvider } from '@material-ui/pickers';

import MomentUtils from '@date-io/moment';

import { alertActions } from './store/actions/alert.actions';

interface IAppProps {
  onTryAutoLogin: any,
  isAuthenticated: boolean,
  error: any,
  loading: boolean,
  username: string,
  alert_severity: string,
  alert_message: string,

  logout: any,
  clearAlert: any,
}

interface State {
  sideBarOpen: boolean,
}

const theme = createMuiTheme({
  palette: {
    primary: { main: '#001eea' },
    secondary: { main: '#0af4b2' },
  },
})

class App extends Component<IAppProps> {

  componentDidMount() {
    this.props.onTryAutoLogin();
  }

  render() {
    return (
      <div className="App">
        <MuiThemeProvider theme={theme}>
          <MuiPickersUtilsProvider utils={MomentUtils}>
            <Snackbar
              open={this.props.alert_severity !== null}
            >
              <SnackbarContent message={this.props.alert_message} action={
                <Button onClick={this.props.clearAlert} color='secondary'><Close />
                </Button>}></SnackbarContent>
            </Snackbar>
            <Router history={history}>
              <FlowFluxisRouter />
            </Router>
          </MuiPickersUtilsProvider>
        </MuiThemeProvider>
      </div>
    );
  }
}

const mapStateToProps = (state: any) => {
  return {
    isAuthenticated: state.user.token !== null,
    loading: state.user.loading,
    error: state.user.error,
    username: state.user.username,
    alert_severity: state.alert.severity,
    alert_message: state.alert.message,
  }
}

const mapDispatchToProps = (dispatch: any) => {
  return {
    logout: () => dispatch(userActions.logout()),
    clearAlert: () => dispatch(alertActions.clear()),
    onTryAutoLogin: () => {
      dispatch(userActions.checkState())
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
