import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const SummaryContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const Summary = ({ inputText, setInputText }) => {
  const [summary, setSummary] = useState("");

  const handleSummarize = async () => {
    if (!inputText) return;

    try {
      const response = await axios.post("http://localhost:8000/summarize/", { text: inputText });
      setSummary(response.data.summary);
    } catch (error) {
      console.error("Özetleme hatası:", error);
    }
  };

  return (
    <SummaryContainer>
      <h3>Metin Özetleme</h3>
      <textarea
        rows="4"
        cols="50"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Özetlemek için metni buraya girin..."
      />
      <button onClick={handleSummarize}>Özetle</button>
      {summary && (
        <div>
          <h4>Özet:</h4>
          <p>{summary}</p>
        </div>
      )}
    </SummaryContainer>
  );
};

export default Summary;
