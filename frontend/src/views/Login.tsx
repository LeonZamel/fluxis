import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import withStyles from '@material-ui/core/styles/withStyles';
import { connect } from 'react-redux';
import { userActions } from '../store/actions/user.actions';
import { Box } from '@material-ui/core';
import { Theme } from '@material-ui/core/styles';
import { Link, Redirect } from 'react-router-dom';
import { Link as MaterialUILink } from '@material-ui/core';
// import MuiAlert, { AlertProps } from '@material-ui/utils/';

const styles: any = (theme: Theme) => ({
  main: {
    width: 'auto',
    display: 'block', // Fix IE 11 issue.
    marginLeft: theme.spacing(3),
    marginRight: theme.spacing(3),
    [theme.breakpoints.up(400 + theme.spacing(3 * 2))]: {
      width: 400,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: `${theme.spacing(2)}px ${theme.spacing(3)}px ${theme.spacing(3)}px`,
  },
  avatar: {
    margin: theme.spacing(1),
    color: theme.palette.text.primary,
    backgroundColor: theme.palette.background.paper,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    marginTop: theme.spacing(1),
  },
});

function Login(props: any) {
  useEffect(() => {
    props.logout()
  }, [])

  const handleSubmit = (e: any) => {
    e.preventDefault();
    props.onAuth(e.target.username.value, e.target.password.value);
  }

  const { classes } = props;

  return (
    props.isAuthenticated ? <Redirect to='/' />
      :
      < main className={classes.main} >
        <CssBaseline />
        <Paper className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography variant="h5">
            Login
        </Typography>
          <form className={classes.form}
            onSubmit={handleSubmit}>
            <FormControl margin="normal" required fullWidth>
              <InputLabel htmlFor="username">Username</InputLabel>
              <Input id="username" name="username" autoComplete="username" autoFocus />
            </FormControl>
            <FormControl margin="normal" required fullWidth>
              <InputLabel htmlFor="password">Password</InputLabel>
              <Input name="password" type="password" id="password" autoComplete="current-password" />
            </FormControl>
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
            >
              Login
          </Button>
          </form>
          <Box mt={2}>
            <MaterialUILink to='/signup/' component={Link}>Don't have an account? Sign Up</MaterialUILink>
          </Box>
        </Paper>
      </main >
  );
}

Login.propTypes = {
  classes: PropTypes.object.isRequired,
};

const styledLoginForm = withStyles(styles)(Login);

const mapStateToProps = (state: any) => {
  return {
    isAuthenticated: state.user.token !== null,
    loading: state.user.loading,
    error: state.user.error
  }
}

const mapDispatchToProps = (dispatch: any) => {
  return {
    onAuth: (username: string, password: string) => dispatch(userActions.login(username, password)),
    logout: () => dispatch(userActions.logout())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(styledLoginForm);
