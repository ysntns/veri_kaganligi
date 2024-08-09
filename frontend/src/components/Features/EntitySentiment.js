import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const EntitySentimentContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const EntitySentiment = ({ inputText }) => {
  const [entitySentiments, setEntitySentiments] = useState([]);

  const handleAnalyzeEntitySentiment = async () => {
    if (!inputText) return;

    try {
      const response = await axios.post("http://localhost:8000/analyze-entity-sentiment/", { text: inputText });
      setEntitySentiments(response.data.results);
    } catch (error) {
      console.error("Varlık bazlı duygu analizi hatası:", error);
    }
  };

  return (
    <EntitySentimentContainer>
      <h3>Varlık Bazlı Duygu Analizi</h3>
      <textarea
        rows="4"
        cols="50"
        value={inputText}
        readOnly
        placeholder="Varlık bazlı duygu analizi için metni buraya girin..."
      />
      <button onClick={handleAnalyzeEntitySentiment}>Analiz Et</button>
      <div>
        <h4>Varlık Bazlı Duygu Analizi Sonuçları:</h4>
        <ul>
          {entitySentiments.map((item, index) => (
            <li key={index}>
              <strong>{item.entity}:</strong> {item.sentiment}
            </li>
          ))}
        </ul>
      </div>
    </EntitySentimentContainer>
  );
};

export default EntitySentiment;