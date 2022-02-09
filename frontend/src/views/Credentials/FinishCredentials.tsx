import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import withStyles from '@material-ui/core/styles/withStyles';
import { connect } from 'react-redux';
import { Box, CircularProgress } from '@material-ui/core';
import { Redirect } from 'react-router-dom';
import { getOAuth2URL, sendOAuth2Code } from '../../core/apiCalls';
import { alertActions } from '../../store/actions/alert.actions';
// import MuiAlert, { AlertProps } from '@material-ui/utils/';

const styles: any = (theme: any) => ({
  main: {
    width: 'auto',
    display: 'block', // Fix IE 11 issue.
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
      width: 400,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing.unit * 8,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
  },
  avatar: {
    margin: theme.spacing.unit,
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing.unit,
  },
  submit: {
    marginTop: theme.spacing.unit * 3,
  },
});

function FinishCredentials(props: any) {
  const [done, setDone] = useState(false)

  useEffect(() => {
    sendOAuth2Code(props.location.search).then(res => {
      props.success()
    }).catch(err => {
      props.error()
    }).finally(() => setDone(true))
  }, [])

  return (
    done ? <Redirect to='/credentials/'></Redirect> :
      <Box minHeight='100vh' display='flex' justifyContent='center' alignItems='center'>
        <CircularProgress size={50} />
      </Box>
  );
}

FinishCredentials.propTypes = {
  classes: PropTypes.object.isRequired,
};

const styledFinishCredentialsForm = withStyles(styles)(FinishCredentials);

const mapStateToProps = (state: any) => {
  return {
  }
}

const mapDispatchToProps = (dispatch: any) => {
  return {
    success: () => dispatch(alertActions.success('Successfully authenticated!')),
    error: () => dispatch(alertActions.error('Something went wrong. Please try again'))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(styledFinishCredentialsForm);
