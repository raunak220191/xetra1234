import React, { useState, useEffect, useCallback } from "react";
import {
  Box,
  Button,
  CircularProgress,
  FormControlLabel,
  IconButton,
  Paper,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TextField,
  Toolbar,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import HomeIcon from "@mui/icons-material/Home";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import MenuItem from "@mui/material/MenuItem";

const Vault = () => {
  const navigate = useNavigate();
  const [rowData, setRowData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedFileId, setSelectedFileId] = useState("");
  const [openDocumentViewer, setOpenDocumentViewer] = useState(false);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [contextualSearch, setContextualSearch] = useState(false);
  const [documentViewerUrl, setDocumentViewerUrl] = useState("");
  const [searchType, setSearchType] = useState("contextual");
  const [searchString, setSearchString] = useState("");
  const [startWord, setStartWord] = useState("");
  const [endWord, setEndWord] = useState("");
  const [columnNames, setColumnNames] = useState([]);

  useEffect(() => {
    searchService("");
  }, []);

  const handleSearch = () => {
    searchService(searchString, startWord, endWord);
  };

  const handleView = useCallback((fileId) => {
    setSelectedFileId(fileId);

    // Call document_viewer_service to get the viewer URL
    const url = "http://localhost:9099/doc_viewer_service";
    const data = { fileId: fileId };

    axios
      .post(url, data)
      .then((response) => {
        const viewerUrl = response.data.viewerUrl;
        setDocumentViewerUrl(viewerUrl);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const handleHomeIconClick = () => {
    navigate("/home");
  };

  const searchService = (query, startWord, endWord) => {
    setLoading(true);
    const url = "http://localhost:9099/vault_service";
    const data = {
      query: query,
      startWord: startWord,
      endWord: endWord,
      isContextual: contextualSearch,
      contextualType: searchType,
    };

    axios
      .post(url, data)
      .then((response) => {
        const results = response.data;
        const transformedData = results.map((item) => {
          return {
            ...item,
            link: (
              <a href={item.link} target="_blank" rel="noopener noreferrer">
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

        const keys = Object.keys(results[0]);
        setColumnNames(keys);

        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
      });
  };

  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number
  ) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const emptyRows =
    rowsPerPage - Math.min(rowsPerPage, rowData.length - page * rowsPerPage);

  return (
    <div>
      <Toolbar>
        <IconButton onClick={handleHomeIconClick} edge="start">
          <HomeIcon />
        </IconButton>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Vault
        </Typography>
      </Toolbar>

      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          marginTop: 2,
          marginBottom: 2,
        }}
      >
        {!contextualSearch && (
          <>
            <TextField
              label="Search"
              variant="outlined"
              value={searchString}
              onChange={(e) => setSearchString(e.target.value)}
            />
            <Button
              variant="contained"
              onClick={handleSearch}
              startIcon={<SearchIcon />}
            >
              Search
            </Button>
          </>
        )}

        {contextualSearch && searchType === "contextual" && (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              marginTop: 2,
              marginBottom: 2,
            }}
          >
            <TextField
              label="Search String"
              variant="outlined"
              value={searchString}
              onChange={(e) => setSearchString(e.target.value)}
            />
            <TextField
              label="In Context Of"
              variant="outlined"
              value={startWord}
              onChange={(e) => setStartWord(e.target.value)}
            />
            <Button
              variant="contained"
              onClick={handleSearch}
              startIcon={<SearchIcon />}
            >
              Search
            </Button>
          </Box>
        )}

        {contextualSearch && searchType === "inBetween" && (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              marginTop: 2,
              marginBottom: 2,
            }}
          >
            <TextField
              label="Search"
              variant="outlined"
              value={searchString}
              onChange={(e) => setSearchString(e.target.value)}
            />
            <TextField
              label="Start Word"
              variant="outlined"
              value={startWord}
              onChange={(e) => setStartWord(e.target.value)}
            />
            <TextField
              label="End Word"
              variant="outlined"
              value={endWord}
              onChange={(e) => setEndWord(e.target.value)}
            />
            <Button
              variant="contained"
              onClick={handleSearch}
              startIcon={<SearchIcon />}
            >
              Search
            </Button>
          </Box>
        )}
      </Box>

      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          marginBottom: 2,
        }}
      >
        <FormControlLabel
          control={
            <Switch
              checked={contextualSearch}
              onChange={() => setContextualSearch(!contextualSearch)}
            />
          }
          label="Contextual Search"
        />
        {contextualSearch && (
          <TextField
            select
            label="Search Type"
            value={searchType}
            onChange={(e) => setSearchType(e.target.value)}
            sx={{ marginLeft: 2 }}
          >
            <MenuItem value="contextual">Contextual</MenuItem>
            <MenuItem value="inBetween">In Between</MenuItem>
          </TextField>
        )}
      </Box>

      {loading ? (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "50vh",
          }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                {columnNames.map((columnName) => (
                  <TableCell key={columnName}>{columnName}</TableCell>
                ))}
                <TableCell>View</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(rowsPerPage > 0
                ? rowData.slice(
                    page * rowsPerPage,
                    page * rowsPerPage + rowsPerPage
                  )
                : rowData
              ).map((row) => (
                <TableRow key={row.file_id}>
                  {columnNames.map((columnName) => (
                    <TableCell key={columnName}>{row[columnName]}</TableCell>
                  ))}
                  <TableCell>{row.viewButton}</TableCell>
                </TableRow>
              ))}

              {emptyRows > 0 && (
                <TableRow style={{ height: 53 * emptyRows }}>
                  <TableCell colSpan={columnNames.length + 1} />
                </TableRow>
              )}
            </TableBody>
          </Table>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={rowData.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </TableContainer>
      )}

      {openDocumentViewer && (
        <iframe
          src={documentViewerUrl}
          title="Document Viewer"
          width="100%"
          height="500px"
        />
      )}
    </div>
  );
};

export default Vault;
