import React from 'react';
import { Route, Redirect } from 'react-router-dom';

import { PrivateRoute } from './components/PrivateRoute';

import FlowList from './views/FlowList/FlowList';
import TriggerList from './views/TriggerList';
import FlowBuild from './views/FlowBuild/FlowBuild';
import Login from './views/Login';
import Signup from './views/Signup';
import RunList from './views/RunList';
import Dashboard from './views/Dashboard/Dashboard';
import FinishCredentials from './views/Credentials/FinishCredentials';
import CredentialsList from './views/Credentials/CredentialsList';
import FileList from './views/Files/FileList';

export const FlowFluxisRouter = () => (
  <div>
    <Route exact path='/login/' component={Login} />
    <Route exact path='/signup/' component={Signup} />
    <PrivateRoute exact path='/' component={Dashboard} />
    <PrivateRoute exact path='/flows/' component={FlowList} />
    <PrivateRoute exact path='/flows/:flowId/' component={FlowBuild} />
    <PrivateRoute exact path='/triggers/' component={TriggerList} />
    <PrivateRoute exact path='/runs/' component={RunList} />
    <PrivateRoute exact path='/credentials/' component={CredentialsList} />
    <PrivateRoute exact path='/finish_credentials/' component={FinishCredentials} />
    <PrivateRoute exact path='/files/' component={FileList} />
  </div>
)

// <Redirect from='*' to='/' />