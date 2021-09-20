import React, { useState, useEffect } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { Link } from 'react-router-dom';
import { Box, Card, Table, TableCell, TableRow, TableHead, TableBody, CardHeader, Divider, makeStyles, MenuItem, Select, InputLabel, DialogContentText, Tab, Tabs, CircularProgress, Typography } from '@material-ui/core';

import { getAllCredentials, sendDeleteCredentials, getOAuth2URL, getOAuth2CredentialServices, getDatabaseCredentialServices, sendCreateCredentials } from '../../core/apiCalls';
import { Credentials, CredentialsService } from '../../core/@types';
import { TabContext, TabPanel } from '@material-ui/lab';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3),
  },
}));


export default function CredentialsList() {
  const classes = useStyles()

  const [loading, setLoading] = useState(true);

  const [credentials, setCredentials] = useState<Credentials[]>([])
  const [dialogOpen, setDialogOpen] = useState(false)

  const [createCredentialsTab, setCreateCredentialsTab] = useState<"oauth" | "database">("database")
  const [createCredentialsType, setCreateCredentialsType] = useState("")
  const [deleteCredentialsId, setDeleteCredentialsId] = useState("")
  const [dialogAction, setDialogAction] = useState<"" | "create" | "delete">("")

  const [oauth2CredentialServices, setOauth2CredentialServices] = useState<CredentialsService[]>([])
  const [databaseCredentialServices, setDatabaseCredentialServices] = useState<CredentialsService[]>([])
  const [authUrl, setAuthUrl] = useState("")


  function handleCreateDatabaseCredentials(e: any) {
    e.preventDefault();
    setDialogOpen(false)
    sendCreateCredentials(createCredentialsType, e.target.username.value, e.target.password.value, e.target.host.value, e.target.port.value, e.target.database.value)
      .then(resp => {
        setCredentials([resp.data, ...credentials])
      })
  }

  function handleDelete() {
    setDialogOpen(false)
    sendDeleteCredentials(deleteCredentialsId).then((res) => {
      setCredentials(credentials.filter((credentials) => credentials.id !== deleteCredentialsId))
    })
    setDeleteCredentialsId("")
  }

  function openDialog() {
    setCreateCredentialsType("")
    setAuthUrl("")
    setDialogOpen(true)
  }

  useEffect(() => {
    getOAuth2CredentialServices().then(res => {
      setOauth2CredentialServices(res.data)
    })
    getDatabaseCredentialServices().then(res => {
      setDatabaseCredentialServices(res.data)
    })
    getAllCredentials().then(res => {
      setCredentials(res.data)
    }).finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <div className={classes.root}>
        <Card>
          <CardHeader
            action={
              <Button
                color="primary"
                variant="contained"
                onClick={() => {
                  setDialogAction("create")
                  openDialog()
                }}
              >
                Add Credentials
              </Button>
            }
            title="Your Credentials"
          />
          <Divider />
          {credentials.length === 0 ?
            <Box minHeight='20vh' minWidth='100%' display='flex' flexDirection='column' justifyContent='center' alignItems='center'>
              {loading ? <CircularProgress />
                :
                <Box>
                  <Typography variant='h5'>
                    No Credentials yet...
                  </Typography>
                  <Typography variant='subtitle1'>
                    Click the 'Add Credentials' button to get started
                  </Typography>
                </Box>
              }
            </Box>
            :
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Service</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {credentials.map((credentials: any) => (
                  <TableRow
                    hover
                    key={credentials.id}
                  >
                    <TableCell>
                      {oauth2CredentialServices.concat(databaseCredentialServices).find(service => service.key === credentials.service)?.name}
                    </TableCell>
                    <TableCell>
                      <Box display='flex' flexDirection='row'>
                        <Button variant="contained" color="default" onClick={() => {
                          setDialogAction("delete")
                          setDeleteCredentialsId(credentials.id)
                          openDialog()
                        }}>Delete</Button>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          }
        </Card>
      </div>
      <div>
        <Dialog
          fullWidth={true}
          maxWidth={'sm'}
          open={dialogOpen}
          onClose={() => setDialogOpen(false)}
          aria-labelledby="form-dialog-title"
        >
          {
            dialogAction === 'delete' ?
              <Box>
                <DialogTitle id="form-dialog-title">Delete Credentials</DialogTitle>
                <DialogContent>
                  Are you sure you want to delete these credentials? This can not be undone.
                </DialogContent>
                <DialogActions>
                  <Button onClick={() => setDialogOpen(false)} color="primary">
                    Cancel
            </Button>
                  <Button onClick={handleDelete} color="default">
                    Delete
            </Button>
                </DialogActions>
              </Box>
              :
              <Box>
                <DialogTitle id="form-dialog-title">Create new Credentials</DialogTitle>
                <TabContext value={createCredentialsTab}>
                  <Tabs value={createCredentialsTab} onChange={(e, newVal) => setCreateCredentialsTab(newVal)} >
                    <Tab label="Database" value="database" />
                    <Tab label="3rd Party Service" value="oauth" />
                  </Tabs>
                  <TabPanel value={"database"}>
                    <form onSubmit={handleCreateDatabaseCredentials}>
                      <DialogContent>
                        <InputLabel id='select-label'>Select database type</InputLabel>
                        <Select
                          required
                          id="type"
                          style={{ width: '100%' }}
                          labelId='select-label'
                          value={createCredentialsType}
                          onChange={(e: any) => {
                            setCreateCredentialsType(e.target.value)
                          }}
                        >
                          {databaseCredentialServices.map(service =>
                            <MenuItem value={service.key}>{service.name}</MenuItem>
                          )}
                        </Select>
                        <TextField id="host" label="Host" required fullWidth />
                        <TextField id="port" label="Port" required type="number" />
                        <TextField id="database" label="Database" required fullWidth />
                        <TextField id="username" label="Username" required fullWidth />
                        <TextField id="password" label="Password" required fullWidth type="password" />
                      </DialogContent>
                      <DialogActions>
                        <Button onClick={() => setDialogOpen(false)} color="default">
                          Cancel
                      </Button>
                        <Button type='submit' color="primary" disabled={createCredentialsType === ""}>
                          Create
                      </Button>
                      </DialogActions>
                    </form>
                  </TabPanel>
                  <TabPanel value={"oauth"} >
                    <DialogContent>
                      <InputLabel id='select-label'>Select service</InputLabel>
                      <Select
                        style={{ width: '100%' }}
                        labelId='select-label'
                        value={createCredentialsType}
                        onChange={(e: any) => {
                          setAuthUrl("")
                          setCreateCredentialsType(e.target.value)
                          getOAuth2URL(e.target.value).then(res => {
                            setAuthUrl(res.data.url)
                          })
                        }}
                      >
                        {oauth2CredentialServices.map(service =>
                          <MenuItem value={service.key}>{service.name}</MenuItem>
                        )}
                      </Select>
                  You will be redirected to the service's login page
                </DialogContent>
                    <DialogActions>
                      <Button onClick={() => setDialogOpen(false)} color="default">
                        Cancel
                      </Button>
                      <Button href={authUrl} color="primary" disabled={authUrl === ''}>
                        Sign in with service
                      </Button>
                    </DialogActions>
                  </TabPanel>
                </TabContext>
              </Box>
          }
        </Dialog>
      </div>
    </div >
  );
}
