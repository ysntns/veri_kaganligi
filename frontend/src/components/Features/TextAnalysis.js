// src/components/TextAnalysis.js

import React, { useState } from 'react';
import axios from 'axios';
import { Button, TextField, Paper, Grid } from '@mui/material';
import { Summarize, Label, Mood, Category } from '@mui/icons-material';

function TextAnalysis({ apiBaseUrl, setResults, setDrawerOpen }) {
  const [text, setText] = useState('');

  const handleSummarize = async () => {
    try {
      const response = await axios.post(`${apiBaseUrl}/summarize/`, { text });
      setResults((prevResults) => ({
        ...prevResults,
        summarize: response.data.summary,
      }));
      setDrawerOpen(true);
    } catch (error) {
      console.error('Özetleme hatası:', error);
    }
  };

  const handleKeywordExtraction = async () => {
    try {
      const response = await axios.post(`${apiBaseUrl}/extract-keywords/`, { text });
      setResults((prevResults) => ({
        ...prevResults,
        keywords: response.data.keywords,
      }));
      setDrawerOpen(true);
    } catch (error) {
      console.error('Anahtar kelime çıkarma hatası:', error);
    }
  };

  const handleSentimentAnalysis = async () => {
    try {
      const response = await axios.post(`${apiBaseUrl}/analyze-sentiment/`, { text });
      setResults((prevResults) => ({
        ...prevResults,
        sentiment: response.data,
      }));
      setDrawerOpen(true);
    } catch (error) {
      console.error('Duygu analizi hatası:', error);
    }
  };

  const handleClassification = async () => {
    try {
      const response = await axios.post(`${apiBaseUrl}/classify-text/`, { text });
      setResults((prevResults) => ({
        ...prevResults,
        classification: response.data,
      }));
      setDrawerOpen(true);
    } catch (error) {
      console.error('Sınıflandırma hatası:', error);
    }
  };

  return (
    <Paper style={{ padding: 16 }}>
      <TextField
        variant="outlined"
        margin="normal"
        fullWidth
        multiline
        rows={4}
        label="Metin Girin"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <Grid container spacing={1}>
        <Grid item xs={12} sm={6}>
          <Button
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleSummarize}
            startIcon={<Summarize />}
          >
            Özetle
          </Button>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Button
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleKeywordExtraction}
            startIcon={<Label />}
          >
            Anahtar Kelimeler
          </Button>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Button
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleSentimentAnalysis}
            startIcon={<Mood />}
          >
            Duygu Analizi
          </Button>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Button
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleClassification}
            startIcon={<Category />}
          >
            Sınıflandır
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
}

export default TextAnalysis;
