import React, { useState } from "react";
import styled from "styled-components";

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

const SelectorContainer = styled.div`
  margin: 20px;
  padding: 10px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const LanguageSelector = () => {
  const [selectedLanguage, setSelectedLanguage] = useState("tr");

  const handleLanguageChange = (e) => {
    setSelectedLanguage(e.target.value);
  };

  return (
    <SelectorContainer>
      <label htmlFor="language-selector">Dil Seçin: </label>
      <select id="language-selector" value={selectedLanguage} onChange={handleLanguageChange}>
        {Object.entries(LANGUAGES).map(([key, label]) => (
          <option key={key} value={key}>
            {label}
          </option>
        ))}
      </select>
    </SelectorContainer>
  );
};

export default LanguageSelector;
