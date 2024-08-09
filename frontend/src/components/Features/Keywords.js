import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const KeywordsContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const Keywords = () => {
  const [text, setText] = useState("");
  const [keywords, setKeywords] = useState([]);

  const handleExtractKeywords = async () => {
    if (!text) return;

    try {
      const response = await axios.post("http://localhost:8000/extract-keywords/", { text });
      setKeywords(response.data.keywords);
    } catch (error) {
      console.error("Anahtar kelime çıkarma hatası:", error);
    }
  };

  return (
    <KeywordsContainer>
      <h3>Anahtar Kelime Çıkarma</h3>
      <textarea
        rows="4"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Anahtar kelime çıkarmak için metni buraya girin..."
      />
      <button onClick={handleExtractKeywords}>Anahtar Kelime Çıkar</button>
      <div>
        <h4>Anahtar Kelimeler:</h4>
        <ul>
          {keywords.map((keyword, index) => (
            <li key={index}>{keyword}</li>
          ))}
        </ul>
      </div>
    </KeywordsContainer>
  );
};

export default Keywords;
