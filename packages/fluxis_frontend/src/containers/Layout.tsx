import React from 'react';
import { withStyles, WithStyles, createStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import { Link } from 'react-router-dom';
import { userActions } from '../store/actions/user.actions';
import { connect } from 'react-redux';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { Snackbar, SnackbarContent, Divider, ListItemIcon, Theme, Box } from '@material-ui/core';
import { alertActions } from '../store/actions/alert.actions';
import { Close, ChevronLeft, Dashboard, Layers, BarChart, LockOpen, AccountTree, AttachFile, Folder } from '@material-ui/icons';

const drawerWidth = 240;

const styles = (theme: Theme) => createStyles({
  root: {
    flexGrow: 1,
  },
  grow: {
    flexGrow: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
  list: {
    width: 250,
  },
  rightText: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(1),
  },
});


// TODO: fix props, split up for redux etc
interface Props extends WithStyles<typeof styles> {
  children: any,
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

class FlowFluxisLayout extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      sideBarOpen: false,
    }
  }

  private toggleDrawer = (open: boolean) => (
    event: React.KeyboardEvent | React.MouseEvent,
  ) => {
    if (
      event.type === 'keydown' &&
      ((event as React.KeyboardEvent).key === 'Tab' ||
        (event as React.KeyboardEvent).key === 'Shift')
    ) {
      return;
    }
    this.setState({ ...this.state, sideBarOpen: open });
  };

  public render() {
    const { classes } = this.props;
    return (
      <Box className={classes.root} >
        <AppBar position="sticky">
          <Toolbar>
            <IconButton className={classes.menuButton} color="inherit" aria-label="Menu" onClick={this.toggleDrawer(true)}>
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" color="inherit" className={classes.grow}>
              Fluxis
            </Typography>
            {
              this.props.isAuthenticated ?
                <Box className={classes.rightText}>
                  <Typography variant="h6" color="inherit" style={{ marginRight: '30px' }}>
                    {"Hello " + this.props.username}
                  </Typography>
                  <Button color="inherit" onClick={this.props.logout} >Logout</Button>
                </Box>
                :
                <Button color="inherit" component={Link} to="/login/">Login</Button>
            }
          </Toolbar>
        </AppBar>
        <Box
          role="presentation"
          onClick={this.toggleDrawer(false)}
          onKeyDown={this.toggleDrawer(false)}
        >
          <Drawer open={this.state.sideBarOpen} onClose={this.toggleDrawer(false)}>
            <Box className={classes.toolbarIcon}>
              <IconButton onClick={this.toggleDrawer(false)}>
                <ChevronLeft />
              </IconButton>
            </Box>
            <Divider />
            <List className={classes.list}>
              <ListItem divider button key={'Dashboard'} component={Link} to={'/'}>
                <ListItemIcon><Dashboard /></ListItemIcon>
                <ListItemText primary={'Dashboard'} />
              </ListItem>
              <ListItem divider button key={'Flows'} component={Link} to={'/flows/'}>
                <ListItemIcon><AccountTree /></ListItemIcon>
                <ListItemText primary={'Flows'} />
              </ListItem>
              <ListItem divider button key={'Runs'} component={Link} to={'/runs/'}>
                <ListItemIcon><BarChart /></ListItemIcon>
                <ListItemText primary={'Runs'} />
              </ListItem>
              <ListItem divider button key={'Files'} component={Link} to={'/files/'}>
                <ListItemIcon><Folder /></ListItemIcon>
                <ListItemText primary={'Files'} />
              </ListItem>
              <ListItem divider button key={'Credentials'} component={Link} to={'/credentials/'}>
                <ListItemIcon><LockOpen /></ListItemIcon>
                <ListItemText primary={'Credentials'} />
              </ListItem>
            </List>
          </Drawer>
        </Box >
        {this.props.children}
      </Box >
    );
  }
}

/*
FlowFluxisLayout.propTypes = {
      classes: PropTypes.object.isRequired,
} as any;
*/

const mapStateToProps = (state: any) => {
  return {
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
    clearAlert: () => dispatch(alertActions.clear())
  }
}

const styledLayout = withStyles(styles)(FlowFluxisLayout);

export default connect(mapStateToProps, mapDispatchToProps)(styledLayout);