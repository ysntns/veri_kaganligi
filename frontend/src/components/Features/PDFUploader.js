import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const PDFUploaderContainer = styled.div`
  margin: 20px;
  padding: 20px;
  background-color: ${({ theme }) => theme.body};
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const PDFUploader = () => {
  const [pdfFile, setPdfFile] = useState(null);
  const [text, setText] = useState("");

  const handleFileChange = (e) => {
    setPdfFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!pdfFile) return;
    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      const response = await axios.post("http://localhost:8000/upload-pdf/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setText(response.data.text);
    } catch (error) {
      console.error("PDF yükleme hatası:", error);
    }
  };

  return (
    <PDFUploaderContainer>
      <h3>PDF Yükleme ve İşleme</h3>
      <input type="file" onChange={handleFileChange} accept=".pdf" />
      <button onClick={handleUpload}>PDF Yükle</button>
      <div>
        <h4>Çıkarılan Metin:</h4>
        <p>{text}</p>
      </div>
    </PDFUploaderContainer>
  );
};

export default PDFUploader;
