import React, { useState, useEffect } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { Link } from 'react-router-dom';
import { Box, Card, Table, TableCell, TableRow, TableHead, TableBody, CardHeader, Divider, makeStyles, CircularProgress, Typography } from '@material-ui/core';

import { getAllFiles, sendCreateFile, sendDeleteFile } from '../../core/apiCalls';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3),
  },
}));


export default function FileList() {
  const classes = useStyles()
  const [files, setFiles] = useState<any[]>([])
  const [dialogOpen, setDialogOpen] = useState(false)
  const [createFileName, setCreateFileName] = useState("")
  const [deleteFileId, setDeleteFileId] = useState("")
  const [dialogAction, setDialogAction] = useState<"" | "create" | "delete">("")
  const [loading, setLoading] = useState(true);
  const [uploadFiles, setUploadFiles] = useState<File[]>([])

  function handleCreate() {
    setDialogOpen(false)
    sendCreateFile(createFileName).then((res) => {
      setFiles([res.data, ...files])
    })
  }

  function handleDelete() {
    setDialogOpen(false)
    sendDeleteFile(deleteFileId).then((res) => {
      setFiles(files.filter((file) => file.id !== deleteFileId))
    })
    setDeleteFileId("")
  }

  useEffect(() => {
    /*
    getAllFiles().then(res => {
      setFiles(res.data)
    })
      .finally(() => {
        setLoading(false)
      })
      */
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
                Add File
              </Button>
            }
            title="Your Files"
          />
          <Divider />
          {files.length === 0 ?
            <Box minHeight='20vh' minWidth='100%' display='flex' flexDirection='column' justifyContent='center' alignItems='center'>
              {loading ? <CircularProgress />
                :
                <Box>
                  <Typography variant='h5'>
                    No Files yet...
                  </Typography>
                  <Typography variant='subtitle1'>
                    Click the 'Add Files' button to get started
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
                {files.map((file: any) => (
                  <TableRow
                    hover
                    key={file.id}
                  >
                    <TableCell>
                      {file.name}
                    </TableCell>
                    <TableCell>
                      {file.id}
                    </TableCell>
                    <TableCell>
                      <Box display='flex' flexDirection='row'>
                        <Button variant="contained" color="primary" component={Link} to={`/files/${file.id}/`}>Edit</Button>
                        <Box width={20}></Box>
                        <Button variant="contained" color="default" onClick={() => {
                          setDialogAction("delete")
                          setDeleteFileId(file.id)
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
                <DialogTitle id="form-dialog-title">Delete File</DialogTitle>
                <DialogContent>
                  Are you sure you want to delete this file? This can not be undone.
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
                <DialogTitle id="form-dialog-title">Upload new Files</DialogTitle>
                <DialogContent>
                  <TextField
                    autoFocus
                    margin="dense"
                    id="name"
                    label="Name"
                    type="text"
                    fullWidth
                    value={createFileName}
                    onChange={(e) => setCreateFileName(e.target.value)}
                  />
                  <Button
                    variant="contained"
                    component="label"
                  >
                    Select Files
                  <input
                      onChange={(e) => {
                        if (e.target.files !== null) {
                          setUploadFiles(Array.from(e.target.files))
                          console.log(uploadFiles)
                        }
                      }}
                      type="file"
                      multiple
                      hidden
                    />
                  </Button>
                </DialogContent>
                <DialogActions>
                  <Button onClick={() => setDialogOpen(false)} color="default">
                    Cancel
            </Button>
                  <Button onClick={handleCreate} color="primary">
                    Upload
            </Button>
                </DialogActions>
              </Box>
          }

        </Dialog>
      </div>
    </div >
  );
}
