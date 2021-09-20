import * as React from 'react';
import { Table, TableHead, TableRow, TableCell, TableBody, makeStyles, CardActions, TablePagination, TableContainer, Divider, Box, Typography } from "@material-ui/core";
import _ from 'lodash';
import { COLUMN_TYPES_MAPPING } from '../../core/@types';

const useStyles = makeStyles(theme => ({
  root: {
    height: '100%',
    width: '100%',
  },
  actions: {
    justifyContent: 'flex-end',
    height: '15%'
  },
  container: {
    height: '85%'
  }
}));

// We use memo and always return true for areEqual as the data in the Table won't change
// If we rerun we get an entirely new DataTable with the new data
// If we don't do this there are severe performance problems because the tables get
// rerendered everytime something changes for some reason. Even when a node is moved
function areEqual(prevProps: any, nextProps: any) {
  return true
}
export default React.memo(DataTable, areEqual);

function DataTable(props: any) {
  const { data } = props
  const { column_types, values } = data

  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(50);

  const classes = useStyles();
  const colNames = Object.keys(values)
  const columnVals: any[][] = Object.values(values)

  return (
    <Box className={classes.root}>
      <TableContainer className={classes.container}>
        <Table size='small' stickyHeader>
          <TableHead>
            <TableRow>
              {colNames.map((key) =>
                <TableCell key={key}><Box>
                  <Box>{key}</Box>
                  <Typography variant='caption'>{COLUMN_TYPES_MAPPING[column_types[key]]}</Typography>
                </Box>
                </TableCell>
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {_.range(page * rowsPerPage, Math.min(columnVals[0].length, (page + 1) * rowsPerPage)).map((row, x) => {
              return (
                <TableRow
                  key={row}
                >
                  {_.range(columnVals.length).map((col, x) =>
                    <TableCell key={col}>{columnVals[col][row]}</TableCell>
                  )}
                </TableRow>
              )
            }
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <Divider />
      <CardActions className={classes.actions}>
        <TablePagination
          component="div"
          count={columnVals[0].length}
          onChangePage={(event, page) => setPage(page)}
          onChangeRowsPerPage={(event) => setRowsPerPage(parseInt(event.target.value))}
          page={page}
          rowsPerPage={rowsPerPage}
          rowsPerPageOptions={[10, 25, 50, 100]}
        />
      </CardActions>
    </Box>
  )
}