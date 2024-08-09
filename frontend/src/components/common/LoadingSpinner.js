import React from 'react';
import styled, { keyframes } from 'styled-components';

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const SpinnerContainer = styled.div`
  display: inline-block;
  width: 30px;
  height: 30px;
  border: 3px solid rgba(0,0,0,.1);
  border-radius: 50%;
  border-top-color: #007bff;
  animation: ${spin} 1s ease-in-out infinite;
`;

const LoadingSpinner = () => <SpinnerContainer />;

export default LoadingSpinner;