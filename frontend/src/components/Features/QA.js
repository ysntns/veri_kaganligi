import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const QAContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const QA = () => {
  const [context, setContext] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState({});

  const handleAskQuestion = async () => {
    if (!context || !question) return;

    try {
      const response = await axios.post("http://localhost:8000/answer-question/", {
        context,
        question,
      });
      setAnswer(response.data);
    } catch (error) {
      console.error("Soru-cevap hatası:", error);
    }
  };

  return (
    <QAContainer>
      <h3>Soru-Cevap</h3>
      <textarea
        rows="4"
        cols="50"
        value={context}
        onChange={(e) => setContext(e.target.value)}
        placeholder="Konteksti buraya girin..."
      />
      <textarea
        rows="2"
        cols="50"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Sorunuzu buraya yazın..."
      />
      <button onClick={handleAskQuestion}>Cevap Al</button>
      <div>
        <h4>Cevap:</h4>
        <p>{answer.answer}</p>
        <p>Skor: {answer.score}</p>
      </div>
    </QAContainer>
  );
};

export default QA;
