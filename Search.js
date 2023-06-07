import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Button,
  Box,
  IconButton,
  Paper,
  Toolbar,
  Typography,
} from "@mui/material";
import axios from "axios";
import CircularProgress from "@mui/material/CircularProgress";
import bn1 from "./bg1.jpg";
import { useTheme } from "@mui/material/styles";
import FirstPageIcon from "@mui/icons-material/FirstPage";
import KeyboardArrowLeft from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";
import LastPageIcon from "@mui/icons-material/LastPage";
import TablePagination from "@mui/material/TablePagination";
import HomeIcon from "@mui/icons-material/Home";

interface TablePaginationActionsProps {
  count: number;
  page: number;
  rowsPerPage: number;
  onPageChange: (
    event: React.MouseEvent<HTMLButtonElement>,
    newPage: number
  ) => void;
}

function TablePaginationActions(props: TablePaginationActionsProps) {
  const theme = useTheme();
  const { count, page, rowsPerPage, onPageChange } = props;

  const handleFirstPageButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onPageChange(event, 0);
  };

  const handleBackButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onPageChange(event, page - 1);
  };

  const handleNextButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onPageChange(event, page + 1);
  };

  const handleLastPageButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onPageChange(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
  };

  return (
    <Box sx={{ flexShrink: 0, ml: 2.5 }}>
      <IconButton
        onClick={handleFirstPageButtonClick}
        disabled={page === 0}
        aria-label="first page"
      >
        {theme.direction === "rtl" ? <LastPageIcon /> : <FirstPageIcon />}
      </IconButton>
      <IconButton
        onClick={handleBackButtonClick}
        disabled={page === 0}
        aria-label="previous page"
      >
        {theme.direction === "rtl" ? (
          <KeyboardArrowRight />
        ) : (
          <KeyboardArrowLeft />
        )}
      </IconButton>
      <IconButton
        onClick={handleNextButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="next page"
      >
        {theme.direction === "rtl" ? (
          <KeyboardArrowLeft />
        ) : (
          <KeyboardArrowRight />
        )}
      </IconButton>
      <IconButton
        onClick={handleLastPageButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="last page"
      >
        {theme.direction === "rtl" ? <FirstPageIcon /> : <LastPageIcon />}
      </IconButton>
    </Box>
  );
}

function Vault() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [rowData, setRowData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedFileId, setSelectedFileId] = useState("");
  const [openDocumentViewer, setOpenDocumentViewer] = useState(false);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  useEffect(() => {
    searchService("");
  }, []);

  const handleSearch = () => {
    searchService(query);
  };

  const handleView = (fileId) => {
    setSelectedFileId(fileId);
    setOpenDocumentViewer(true);
  };

  const handleHomeIconClick = () => {
    navigate("/home");
  };

  const searchService = (query) => {
    setLoading(true);
    const url = "http://localhost:9099/vault_service";
    const data = { query: query };

    axios
      .post(url, data)
      .then((response) => {
        const results = response.data;
        const transformedData = results.map((item) => {
          return {
            name: item.filename,
            id: item.file_id,
            link: (
              <a
                href={item.link}
                target="_blank"
                rel="noopener noreferrer"
              >
                {item.link}
              </a>
            ),
            viewButton: (
              <Button
                variant="contained"
                onClick={() => handleView(item.file_id)}
              >
                View
              </Button>
            ),
          };
        });
        setRowData(transformedData);
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
      });
  };

  const handleChangePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const emptyRows = rowsPerPage - Math.min(rowsPerPage, rowData.length - page * rowsPerPage);
  useEffect(() => {
    if (openDocumentViewer) {
      document.getElementById("documentViewerForm").submit();
      setOpenDocumentViewer(false);
    }
  }, [openDocumentViewer]);

  return (
    <div>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Vault
        </Typography>
        <IconButton
          edge="end"
          color="inherit"
          aria-label="home"
          onClick={handleHomeIconClick}
        >
          <HomeIcon />
        </IconButton>
      </Toolbar>

      <div style={{ display: "flex", justifyContent: "center", marginTop: 20 }}>
        <TextField
          label="Search"
          variant="outlined"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button variant="contained" onClick={handleSearch}>
          Search
        </Button>
      </div>

      <TableContainer component={Paper} style={{ marginTop: 20 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>File Name</TableCell>
              <TableCell>View</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {(rowsPerPage > 0
              ? rowData.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              : rowData
            ).map((row) => (
              <TableRow key={row.id}>
                <TableCell>{row.name}</TableCell>
                <TableCell>{row.viewButton}</TableCell>
              </TableRow>
            ))}

            {emptyRows > 0 && (
              <TableRow style={{ height: 53 * emptyRows }}>
                <TableCell colSpan={2} />
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={[5, 10, 25, { label: 'All', value: -1 }]}
        component="div"
        count={rowData.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        ActionsComponent={TablePaginationActions}
        style={{ marginTop: 20 }}
      />

      {loading && (
        <div style={{ display: "flex", justifyContent: "center", marginTop: 20 }}>
          <CircularProgress />
        </div>
      )}

      {openDocumentViewer && (
        <form
          id="documentViewerForm"
          action="http://localhost:9099/doc_viewer_service"
          method="POST"
          target="_blank"
        >
          <input type="hidden" name="file_id" value={selectedFileId} />
        </form>
      )}
    </div>
  );
}

export default Vault;
