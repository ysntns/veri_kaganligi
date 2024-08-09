import React from "react";
import styled from "styled-components";

const NavbarContainer = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
`;

const Logo = styled.h1`
  color: #fff;
  font-size: 1.5rem;
  margin: 0;
`;

const ThemeToggle = styled.button`
  background: none;
  border: none;
  color: #fff;
  font-size: 1.5rem;
  cursor: pointer;
`;

const Navbar = ({ toggleTheme }) => {
  return (
    <NavbarContainer>
      <Logo>🇹🇷 Türkçe Doğal Dil İşleme Senaryosu 🇹🇷</Logo>
      <ThemeToggle onClick={toggleTheme}>🌓</ThemeToggle>
    </NavbarContainer>
  );
};

export default Navbar;