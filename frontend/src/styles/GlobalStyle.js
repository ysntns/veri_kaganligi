import { createGlobalStyle } from "styled-components";

export const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    background-color: ${({ theme }) => theme.body};
    color: ${({ theme }) => theme.text};
    transition: all 0.3s ease-in-out;
    overflow-x: hidden;
  }

  h1, h2, h3, h4, h5, h6 {
    font-weight: bold;
    color: ${({ theme }) => theme.title};
    transition: color 0.3s ease-in-out;
  }

  button {
    background-color: ${({ theme }) => theme.buttonBackground};
    color: ${({ theme }) => theme.buttonText};
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
    margin-top: 10px;
    transition: all 0.3s ease-in-out;

    &:hover {
      background-color: ${({ theme }) => theme.buttonHover};
    }
  }
  
  .container {
    padding: 20px;
    margin: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-in-out;
  }

     .nlp-panel {
    position: fixed;
    right: 0;
    top: 0;
    bottom: 0;
    width: 400px;
    background-color: ${({ theme }) => theme.body};
    color: ${({ theme }) => theme.text};
    z-index: 1000;
    padding: 20px;
    box-shadow: -2px 0 5px rgba(0,0,0,0.1);
  }

  .nlp-panel textarea, .nlp-panel select, .nlp-panel button {
    width: 100%;
    margin-bottom: 10px;
  }

  .nlp-panel textarea {
    min-height: 150px;
  }
`;