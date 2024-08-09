import React from "react";
import styled from "styled-components";

const FeatureCard = styled.div`
  width: 100%;
  height: 150px;
  background-color: rgba(255, 255, 255, 0.8);
  color: ${({ theme }) => theme.text};
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s;

  &:hover {
    transform: scale(1.05);
  }
`;

const NLPFeature = ({ title, onClick }) => {
  return <FeatureCard onClick={onClick}><h3>{title}</h3></FeatureCard>;
};

export default NLPFeature;
