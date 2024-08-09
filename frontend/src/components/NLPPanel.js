import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Panel = styled.div`
  position: fixed;
  right: 0;
  top: 0;
  bottom: 0;
  width: 500px;
  background-color: #f8f9fa;
  padding: 20px;
  box-shadow: -2px 0 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow-y: auto;
`;

const CloseButton = styled.button`
  position: absolute;
  right: 10px;
  top: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #333;
`;

const Select = styled.select`
  margin-bottom: 15px;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ddd;
`;

const TextArea = styled.textarea`
  height: 200px;
  margin-bottom: 15px;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ddd;
  resize: vertical;
`;

const ButtonGroup = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
`;

const Button = styled.button`
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  &:hover {
    background-color: #0056b3;
  }
`;

const ResultArea = styled.div`
  flex: 1;
  overflow-y: auto;
  background-color: white;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
`;

const FileInput = styled.input`
  margin-bottom: 15px;
`;

const ExtractedText = styled.div`
  margin-top: 15px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  max-height: 200px;
  overflow-y: auto;
`;

const features = [
  'PDF Yükleme',
  'Metin Özetleme',
  'Anahtar Kelime Çıkarma',
  'Metin Sınıflandırma',
  'Duygu Analizi',
  'Varlık Bazlı Duygu Analizi',
  'Çeviri',
  'Çapraz Çeviri',
  'Soru-Cevap'
];

const languages = [
  { code: 'tr', name: '🇹🇷 Türkçe' },
  { code: 'en', name: '🇬🇧 İngilizce' },
  { code: 'de', name: '🇩🇪 Almanca' },
  { code: 'fr', name: '🇫🇷 Fransızca' },
  { code: 'es', name: '🇪🇸 İspanyolca' },
];

function NLPPanel({ onClose, activeFeature }) {
  const [language, setLanguage] = useState('tr');
  const [text, setText] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');

  useEffect(() => {
    const handleEsc = (event) => {
      if (event.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => {
      window.removeEventListener('keydown', handleEsc);
    };
  }, [onClose]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handlePDFUpload = async () => {
    if (!file) {
      alert('Lütfen bir PDF dosyası seçin.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload-pdf/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setExtractedText(response.data.text);
      setText(response.data.text);
      setResult('PDF başarıyla yüklendi ve işlendi.');
    } catch (error) {
      console.error('PDF yükleme hatası:', error);
      setResult('PDF yükleme sırasında bir hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const handleFeature = async (feature) => {
    setLoading(true);
    try {
      let response;
      switch (feature) {
        case 'PDF Yükleme':
          await handlePDFUpload();
          return;
        case 'Metin Özetleme':
          response = await axios.post('http://localhost:8000/summarize/', { text });
          setResult(response.data.summary);
          break;
        case 'Anahtar Kelime Çıkarma':
          response = await axios.post('http://localhost:8000/extract-keywords/', { text });
          setResult(response.data.keywords.join(', '));
          break;
        case 'Metin Sınıflandırma':
          response = await axios.post('http://localhost:8000/classify-text/', { text });
          setResult(`Sınıf: ${response.data.class}, Skor: ${response.data.score}`);
          break;
        case 'Duygu Analizi':
          response = await axios.post('http://localhost:8000/analyze-sentiment/', { text });
          setResult(`Duygu: ${response.data.sentiment}, Skor: ${response.data.score}`);
          break;
        case 'Varlık Bazlı Duygu Analizi':
          response = await axios.post('http://localhost:8000/analyze-entity-sentiment/', { text });
          setResult(JSON.stringify(response.data, null, 2));
          break;
        case 'Çeviri':
          response = await axios.post('http://localhost:8000/translate/', { text, source_language: language, target_language: 'en' });
          setResult(response.data.translated_text);
          break;
        case 'Çapraz Çeviri':
          response = await axios.post('http://localhost:8000/translate-multiple/', { text, target_languages: ['en', 'fr', 'de', 'es'] });
          setResult(JSON.stringify(response.data.translations, null, 2));
          break;
        case 'Soru-Cevap':
          const question = prompt("Lütfen sorunuzu girin:");
          if (question) {
            response = await axios.post('http://localhost:8000/answer-question/', { context: text, question });
            setResult(`Soru: ${question}\nCevap: ${response.data.answer}\nSkor: ${response.data.score}`);
          } else {
            setResult('Soru girilmedi.');
          }
          break;
        default:
          setResult('Geçersiz özellik seçildi.');
          return;
      }
    } catch (error) {
      console.error(`${feature} hatası:`, error);
      setResult(`${feature} işlemi sırasında bir hata oluştu: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Panel>
      <CloseButton onClick={onClose}>×</CloseButton>
      <Select value={language} onChange={(e) => setLanguage(e.target.value)}>
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>{lang.name}</option>
        ))}
      </Select>
      {activeFeature === 'PDF Yükleme' ? (
        <>
          <FileInput type="file" accept=".pdf" onChange={handleFileChange} />
          <Button onClick={handlePDFUpload} disabled={loading}>
            PDF Yükle ve İşle
          </Button>
          {extractedText && (
            <ExtractedText>
              <h4>Çıkarılan Metin:</h4>
              <p>{extractedText}</p>
            </ExtractedText>
          )}
        </>
      ) : (
        <TextArea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Metninizi buraya girin..."
        />
      )}
      <ButtonGroup>
        {features.map((feature) => (
          <Button
            key={feature}
            onClick={() => handleFeature(feature)}
            disabled={loading}
            style={{ backgroundColor: activeFeature === feature ? '#0056b3' : '#007bff' }}
          >
            {feature}
          </Button>
        ))}
      </ButtonGroup>
      <ResultArea>
        {loading ? 'İşleniyor...' : result}
      </ResultArea>
    </Panel>
  );
}

export default NLPPanel;