import React from 'react';
import { Route, Redirect, RouteProps } from 'react-router-dom';
import FlowFluxisLayout from '../containers/Layout';

export const PrivateRoute: React.FC<RouteProps> = ({ component: Component, ...rest }) => {
  if (!Component) return null
  else return (
    <Route {...rest} render={(props) => (
      localStorage.getItem('token')
        ? <FlowFluxisLayout isAuthenticated={true}><Component {...props} /></FlowFluxisLayout>
        : <Redirect to='/login' />
    )} />
  )
}


