import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const CrossTranslationContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const LANGUAGES = {
  tr: "🇹🇷 Türkçe",
  en: "🇬🇧 İngilizce",
  "zh-cn": "🇨🇳 Çince",
  es: "🇪🇸 İspanyolca",
  hi: "🇮🇳 Hintçe",
  ar: "🇸🇦 Arapça",
  bn: "🇧🇩 Bengalce",
  fr: "🇫🇷 Fransızca",
  de: "🇩🇪 Almanca",
  ja: "🇯🇵 Japonca",
  ru: "🇷🇺 Rusça",
  pt: "🇵🇹 Portekizce",
  ko: "🇰🇷 Korece",
  it: "🇮🇹 İtalyanca",
  nl: "🇳🇱 Felemenkçe",
};

const CrossTranslation = () => {
  const [text, setText] = useState("");
  const [translations, setTranslations] = useState({});
  const [targetLanguages, setTargetLanguages] = useState(["en", "de", "fr"]);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleCrossTranslate = async () => {
    if (!text) return;

    try {
      const response = await axios.post("http://localhost:8000/translate-multiple/", {
        text,
        target_languages: targetLanguages,
      });
      setTranslations(response.data.translations);
      setDrawerOpen(true);
    } catch (error) {
      console.error("Çapraz çeviri hatası:", error);
    }
  };

  return (
    <CrossTranslationContainer>
      <h2>Çapraz Çeviri</h2>
      <textarea
        rows="4"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Çapraz çevirmek için metni buraya girin..."
      />
      <div>
        <label>
          Hedef Diller:
          <select
            multiple
            value={targetLanguages}
            onChange={(e) => setTargetLanguages([...e.target.selectedOptions].map((option) => option.value))}
          >
            {Object.entries(LANGUAGES).map(([key, label]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </select>
        </label>
      </div>
      <button onClick={handleCrossTranslate}>Çapraz Çevir</button>
      <div>
        <h4>Çapraz Çeviri Sonuçları:</h4>
        <ul>
          {Object.entries(translations).map(([lang, translation], index) => (
            <li key={index}>
              <strong>{LANGUAGES[lang]}:</strong> {translation}
            </li>
          ))}
        </ul>
      </div>
    </CrossTranslationContainer>
  );
};

export default CrossTranslation;
