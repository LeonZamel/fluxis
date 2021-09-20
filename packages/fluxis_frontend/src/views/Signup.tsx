import React from 'react';
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
import { Link, Redirect } from 'react-router-dom';
import { Link as MaterialUILink, Box } from '@material-ui/core';

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
    margin: theme.spacing(1),
    color: theme.palette.text.primary,
    backgroundColor: theme.palette.background.paper,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing.unit,
  },
  submit: {
    marginTop: theme.spacing.unit * 3,
  },
});

function Signup(props: any) {

  const handleSubmit = (e: any) => {
    e.preventDefault();
    props.onSignup(e.target.username.value, e.target.email.value, e.target.password.value, e.target.confirmPassword.value);
  }

  const { classes } = props;

  return (
    props.isAuthenticated ? <Redirect to='/' />
      :
      <main className={classes.main}>
        <CssBaseline />
        <Paper className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography variant="h5">
            Sign up
        </Typography>
          <form className={classes.form}
            onSubmit={handleSubmit}>
            <FormControl margin="normal" required fullWidth>
              <InputLabel htmlFor="username">Username</InputLabel>
              <Input id="username" name="username" autoComplete="username" autoFocus />
            </FormControl>
            <FormControl margin="normal" required fullWidth>
              <InputLabel htmlFor="email">Email Address</InputLabel>
              <Input id="email" name="email" autoComplete="email" autoFocus />
            </FormControl>
            <FormControl margin="normal" required fullWidth>
              <InputLabel htmlFor="password">Password</InputLabel>
              <Input name="password" type="password" id="password" autoComplete="password" />
            </FormControl>
            <FormControl margin="normal" required fullWidth>
              <InputLabel htmlFor="confirmPassword">Confirm your Password</InputLabel>
              <Input name="confirmPassword" type="password" id="confirmPassword" autoComplete="confirmPassword" />
            </FormControl>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
            >
              Sign up
          </Button>
          </form>
          <Box mt={2}>
            <MaterialUILink to='/login/' component={Link}>Already have an account? Log In</MaterialUILink>
          </Box>
        </Paper>
      </main>
  );
}

Signup.propTypes = {
  classes: PropTypes.object.isRequired,
};

const WrappedLoginForm = withStyles(styles)(Signup);

const mapStateToProps = (state: any) => {
  return {
    isAuthenticated: state.user.token !== null,
    loading: state.loading,
    error: state.error
  }
}

const mapDispatchToProps = (dispatch: any) => {
  return {
    onSignup: (username: string, email: string, password1: string, password2: string) => dispatch(userActions.signup(username, email, password1, password2))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(WrappedLoginForm);
