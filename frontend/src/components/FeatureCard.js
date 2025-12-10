import React from "react";
import styled from "styled-components";

const Card = styled.div`
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }
`;

const Icon = styled.span`
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
`;

const Title = styled.h3`
  font-size: 1.2rem;
  color: #fff;
  text-align: center;
  margin: 0;
`;

const FeatureCard = ({ title, icon, onClick }) => {
  return (
    <Card onClick={onClick}>
      <Icon>{icon}</Icon>
      <Title>{title}</Title>
    </Card>
  );
};

export default FeatureCard;