import React from 'react';
import styled from 'styled-components';

const ErrorContainer = styled.div`
  background-color: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
`;

const ErrorMessage = ({ message }) => (
  <ErrorContainer>
    <p>{message}</p>
  </ErrorContainer>
);

export default ErrorMessage;