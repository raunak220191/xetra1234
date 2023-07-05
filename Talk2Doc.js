import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Grid,
  TextField,
  Typography,
  Fab,
  LinearProgress,
} from '@mui/material';
import { styled } from '@mui/system';

const useStyles = styled((theme) => ({
  fab: {
    position: 'fixed',
    bottom: theme.spacing(4),
    right: theme.spacing(4),
    zIndex: 1,
    transition: 'transform 0.3s',
    '&:hover': {
      transform: 'scale(1.1)',
    },
  },
}));

const TalkToDoc = () => {
  const classes = useStyles();
  const [files, setFiles] = useState([]);
  const [question, setQuestion] = useState('');
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [loadTTDResponse, setLoadTTDResponse] = useState(null);
  const [answerText, setAnswerText] = useState('');

  const handleFileChange = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setFiles(uploadedFiles);
    setLoading(true);
    loadTTDService(uploadedFiles);
  };

  const loadTTDService = async (files) => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:9099/load_ttd_service', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setUploadComplete(true);
        setLoading(false);
        setLoadTTDResponse(data);
      } else {
        console.log('Error:', response.status);
      }
    } catch (error) {
      console.log('Error:', error);
    }
  };

  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleAskQuestion = async () => {
    const formData = new FormData();
    formData.append('question', question);
    formData.append('loadTTDResponse', JSON.stringify(loadTTDResponse));
    formData.append('responses', JSON.stringify(responses));

    try {
      const response = await fetch('http://localhost:9099/ttd_service', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const responseData = await response.json();
        const data = responseData.data; // Access the 'data' array in the response
        const newResponse = {
          question,
          answer: data, // Use 'data' directly as the answer
          filename: data.filename, // Update the filename accordingly if needed
        };
        setResponses((prevResponses) => [...prevResponses, newResponse]);
        setQuestion('');
      } else {
        console.log('Error:', response.status);
      }
    } catch (error) {
      console.log('Error:', error);
    }
  };

  useEffect(() => {
    if (responses.length > 0) {
      const currentResponse = responses[responses.length - 1];
      printAnswer(currentResponse.answer);
    }
  }, [responses]);

  function printAnswer(answer) {
    setAnswerText('');
    let index = 0;
    const timer = setInterval(() => {
      setAnswerText((prevAnswer) => prevAnswer + answer[index]);
      index++;
      if (index >= answer.length) {
        clearInterval(timer);
      }
    }, 50);
  }

  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" align="center">
          Talk to Document Bot
        </Typography>
      </Box>

      {!uploadComplete && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6" component="h2" gutterBottom>
              Upload CVs in PDF format
            </Typography>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={6}>
                <input
                  accept="application/pdf"
                  id="file-upload"
                  type="file"
                  onChange={handleFileChange}
                  style={{ display: 'none' }}
                  multiple
                />
                <label htmlFor="file-upload">
                  <Fab
                    component="span"
                    color="primary"
                    variant="extended"
                    size="large"
                    className={classes.fab}
                  >
                    Choose File
                  </Fab>
                </label>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1" component="div">
                  {files.length > 0 ? files.map((file) => file.name).join(', ') : 'No files selected'}
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {loading && (
        <Box sx={{ mt: 4 }}>
          <LinearProgress />
        </Box>
      )}

      {uploadComplete && (
        <Box sx={{ mt: 4 }}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom>
                Ask a Question
              </Typography>
              <TextField
                id="question"
                label="Enter your question"
                variant="outlined"
                fullWidth
                value={question}
                onChange={handleQuestionChange}
              />
              <Box sx={{ mt: 2 }}>
                <Fab
                  color="primary"
                  variant="extended"
                  disabled={!question}
                  onClick={handleAskQuestion}
                >
                  Ask
                </Fab>
              </Box>
            </CardContent>
          </Card>
        </Box>
      )}

      {/* Section 3: Display the response */}
      {responses.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom>
                Response
              </Typography>
              {responses.map((qa, index) => (
                <Box key={index} sx={{ marginBottom: 2 }}>
                  <Typography variant="body1" component="div">
                    <strong>Question:</strong> {qa.question}
                  </Typography>
                  <Typography variant="body1" component="div">
                    <strong>Answer:</strong>
                  </Typography>
                  {Array.isArray(qa.answer) ? (
                    <Box sx={{ pl: 2 }}>
                      {qa.answer.map((response, index) => (
                        <Typography variant="body1" component="div" key={index}>
                          <strong>In {response.filename.toString()}:</strong> {response.answer.toString()}
                        </Typography>
                      ))}
                    </Box>
                  ) : (
                    qa.answer && (
                      <Typography variant="body1" component="div">
                        <strong>In {qa.filename.toString()}:</strong> {qa.answer.toString()}
                      </Typography>
                    )
                  )}
                </Box>
              ))}
            </CardContent>
          </Card>
        </Box>
      )}
    </Container>
  );
};

export default TalkToDoc;
