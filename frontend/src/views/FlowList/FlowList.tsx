import React, { useState, useEffect } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { Link } from 'react-router-dom';
import { Box, Card, Table, TableCell, TableRow, TableHead, TableBody, CardHeader, Divider, makeStyles, CircularProgress, Typography } from '@material-ui/core';

import { getAllFlows, sendCreateFlow, sendDeleteFlow } from '../../core/apiCalls';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3),
  },
}));


export default function FlowList() {
  const classes = useStyles()
  const [flows, setFlows] = useState<any[]>([])
  const [dialogOpen, setDialogOpen] = useState(false)
  const [createFlowName, setCreateFlowName] = useState("")
  const [deleteFlowId, setDeleteFlowId] = useState("")
  const [dialogAction, setDialogAction] = useState<"" | "create" | "delete">("")
  const [loading, setLoading] = useState(true);

  function handleCreate() {
    setDialogOpen(false)
    sendCreateFlow(createFlowName).then((res) => {
      setFlows([res.data, ...flows])
    })
  }

  function handleDelete() {
    setDialogOpen(false)
    sendDeleteFlow(deleteFlowId).then((res) => {
      setFlows(flows.filter((flow) => flow.id !== deleteFlowId))
    })
    setDeleteFlowId("")
  }

  useEffect(() => {
    getAllFlows().then(res => {
      setFlows(res.data)
    })
      .finally(() => {
        setLoading(false)
      })
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
                  setDialogOpen(true)
                }}
              >
                Add Flow
              </Button>
            }
            title="Your Flows"
          />
          <Divider />
          {flows.length === 0 ?
            <Box minHeight='20vh' minWidth='100%' display='flex' flexDirection='column' justifyContent='center' alignItems='center'>
              {loading ? <CircularProgress />
                :
                <Box>
                  <Typography variant='h5'>
                    No Flows yet...
                  </Typography>
                  <Typography variant='subtitle1'>
                    Click the 'Add Flow' button to get started
                  </Typography>
                </Box>
              }
            </Box>
            :
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Unique Identifier</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {flows.map((flow: any) => (
                  <TableRow
                    hover
                    key={flow.id}
                  >
                    <TableCell>
                      {flow.name}
                    </TableCell>
                    <TableCell>
                      {flow.id}
                    </TableCell>
                    <TableCell>
                      <Box display='flex' flexDirection='row'>
                        <Button variant="contained" color="primary" component={Link} to={`/flows/${flow.id}/`}>Edit</Button>
                        <Box width={20}></Box>
                        <Button variant="contained" color="default" onClick={() => {
                          setDialogAction("delete")
                          setDeleteFlowId(flow.id)
                          setDialogOpen(true)
                        }}>Delete</Button>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))
                }
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
                <DialogTitle id="form-dialog-title">Delete Flow</DialogTitle>
                <DialogContent>
                  Are you sure you want to delete this flow? This can not be undone.
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
                <DialogTitle id="form-dialog-title">Create new Flow</DialogTitle>
                <DialogContent>
                  <TextField
                    autoFocus
                    margin="dense"
                    id="name"
                    label="Name"
                    type="text"
                    fullWidth
                    value={createFlowName}
                    onChange={(e) => setCreateFlowName(e.target.value)}
                  />
                </DialogContent>
                <DialogActions>
                  <Button onClick={() => setDialogOpen(false)} color="default">
                    Cancel
            </Button>
                  <Button onClick={handleCreate} color="primary">
                    Create
            </Button>
                </DialogActions>
              </Box>
          }

        </Dialog>
      </div>
    </div >
  );
}
