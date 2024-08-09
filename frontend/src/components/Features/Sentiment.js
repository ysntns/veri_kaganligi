import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const SentimentContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const Sentiment = () => {
  const [text, setText] = useState("");
  const [sentiment, setSentiment] = useState({});

  const handleAnalyzeSentiment = async () => {
    if (!text) return;

    try {
      const response = await axios.post("http://localhost:8000/analyze-sentiment/", { text });
      setSentiment(response.data);
    } catch (error) {
      console.error("Duygu analizi hatası:", error);
    }
  };

  return (
    <SentimentContainer>
      <h3>Duygu Analizi</h3>
      <textarea
        rows="4"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Duygu analiz etmek için metni buraya girin..."
      />
      <button onClick={handleAnalyzeSentiment}>Analiz Et</button>
      <div>
        <h4>Duygu Analizi Sonucu:</h4>
        <p>Duygu: {sentiment.sentiment}</p>
        <p>Skor: {sentiment.score}</p>
      </div>
    </SentimentContainer>
  );
};

export default Sentiment;
