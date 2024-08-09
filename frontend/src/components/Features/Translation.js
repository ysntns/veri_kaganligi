import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";
import ErrorMessage from '../common/ErrorMessage';
import LoadingSpinner from '../common/LoadingSpinner';
import { apiRequest } from '../../utils/api';


const TranslationContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const Translation = ({ inputText, setInputText }) => {
  const [translatedText, setTranslatedText] = useState("");
  const [targetLanguage, setTargetLanguage] = useState("en");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleTranslate = async () => {
    if (!inputText) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post("http://localhost:8000/translate/", {
        text: inputText,
        target_language: targetLanguage,
      });
      setTranslatedText(response.data.translated_text);
    } catch (error) {
      console.error("Çeviri hatası:", error);
      setError("Çeviri işlemi sırasında bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <TranslationContainer>
      <h3>Çeviri</h3>
      <textarea
        rows="4"
        cols="50"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Çevirmek için metni buraya girin..."
      />
      <select value={targetLanguage} onChange={(e) => setTargetLanguage(e.target.value)}>
        <option value="en">İngilizce</option>
        <option value="de">Almanca</option>
        <option value="fr">Fransızca</option>
        <option value="es">İspanyolca</option>
      </select>
      <button onClick={handleTranslate} disabled={isLoading}>
        {isLoading ? <LoadingSpinner /> : 'Çevir'}
      </button>
      {error && <ErrorMessage message={error} />}
      {!isLoading && !error && translatedText && (
        <div>
          <h4>Çeviri Sonucu:</h4>
          <p>{translatedText}</p>
        </div>
      )}
    </TranslationContainer>
  );
};

export default Translation;