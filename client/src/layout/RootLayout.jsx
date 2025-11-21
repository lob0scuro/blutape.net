import React from "react";
import { Outlet } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import LOGO from "../assets/blutape-logo.svg";

const RootLayout = () => {
  return (
    <>
      <header>
        <img src={LOGO} alt="bluTape logo" className="header-logo" />
      </header>
      <main>
        <Outlet />
      </main>
      <footer></footer>
      <Toaster position="bottom-right" reverseOrder={true} />
    </>
  );
};

export default RootLayout;
