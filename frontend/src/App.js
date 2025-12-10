import React, { useState } from "react";
import styled, { ThemeProvider } from "styled-components";
import { GlobalStyle } from "./styles/GlobalStyle";
import { lightTheme, darkTheme } from "./styles/themes";
import Navbar from "./components/Navbar";
import LanguageSelector from "./components/LanguageSelector";
import NLPPanel from "./components/NLPPanel";

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  z-index: 1;
  padding: 60px 20px;
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  margin-top: 40px;
`;

const VideoBackground = styled.video`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
  filter: brightness(50%);
`;

const App = () => {
  const [theme, setTheme] = useState("light");
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [activeFeature, setActiveFeature] = useState(null);

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  const features = [
    "PDF Yükleme",
    "Metin Özetleme",
    "Anahtar Kelime Çıkarma",
    "Metin Sınıflandırma",
    "Duygu Analizi",
    "Varlık Bazlı Duygu Analizi",
    "Çeviri",
    "Çapraz Çeviri",
    "Soru-Cevap",
  ];

  const handleFeatureClick = (feature) => {
    setActiveFeature(feature);
    setIsPanelOpen(true);
  };

  return (
    <ThemeProvider theme={theme === "light" ? lightTheme : darkTheme}>
      <GlobalStyle />
      <VideoBackground autoPlay muted loop>
        <source src="/background.mp4" type="video/mp4" />
      </VideoBackground>
      <Navbar toggleTheme={toggleTheme} />
      <AppContainer>
        <h1 style={{ color: '#fff' }}>🇹🇷 Metin, PDF, Özetleme ve Çeviri Sistemi 🇹🇷</h1>
        <LanguageSelector />
        <FeatureGrid>
          {features.map((feature) => (
            <div
              key={feature}
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "150px",
                backgroundColor: "rgba(255, 255, 255, 0.8)",
                borderRadius: "10px",
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                cursor: "pointer",
                transition: "transform 0.3s",
              }}
              onClick={() => handleFeatureClick(feature)}
            >
              <h3>{feature}</h3>
            </div>
          ))}
        </FeatureGrid>
      </AppContainer>
      {isPanelOpen && (
        <NLPPanel
          onClose={() => setIsPanelOpen(false)}
          activeFeature={activeFeature}
        />
      )}
    </ThemeProvider>
  );
};

export default App;