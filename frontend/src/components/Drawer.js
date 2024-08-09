import React from 'react';
import styled from 'styled-components';

const DrawerOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end;
  z-index: 1000;
`;

const DrawerContent = styled.div`
  width: 300px;
  background-color: ${({ theme }) => theme.body};
  height: 100%;
  padding: 2rem;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
`;

const CloseButton = styled.button`
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: ${({ theme }) => theme.text};
`;

const Drawer = ({ children, onClose }) => {
  return (
    <DrawerOverlay>
      <DrawerContent>
        <CloseButton onClick={onClose}>&times;</CloseButton>
        {children}
      </DrawerContent>
    </DrawerOverlay>
  );
};

export default Drawer;