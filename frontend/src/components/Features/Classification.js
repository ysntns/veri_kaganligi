import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const ClassificationContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const Classification = () => {
  const [text, setText] = useState("");
  const [classification, setClassification] = useState({});

  const handleClassifyText = async () => {
    if (!text) return;

    try {
      const response = await axios.post("http://localhost:8000/classify-text/", { text });
      setClassification(response.data);
    } catch (error) {
      console.error("Metin sınıflandırma hatası:", error);
    }
  };

  return (
    <ClassificationContainer>
      <h3>Metin Sınıflandırma</h3>
      <textarea
        rows="4"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Sınıflandırmak için metni buraya girin..."
      />
      <button onClick={handleClassifyText}>Sınıflandır</button>
      <div>
        <h4>Sınıflandırma Sonucu:</h4>
        <p>Sınıf: {classification.class}</p>
        <p>Skor: {classification.score}</p>
      </div>
    </ClassificationContainer>
  );
};

export default Classification;
