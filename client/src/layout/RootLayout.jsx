import React, { useEffect, useRef, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import LOGO from "../assets/blutape-logo.svg";
import { useAuth } from "../context/AuthContext";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faBarsStaggered } from "@fortawesome/free-solid-svg-icons";
import Navbar from "../components/Navbar";

const RootLayout = () => {
  const { user, setUser } = useAuth();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);
  const buttonRef = useRef(null);

  useEffect(() => {
    setMenuOpen(false);
  }, [location]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      const clickedInsideMenu =
        menuRef.current && menuRef.current.contains(event.target);

      const clickedMenuButton =
        buttonRef.current && buttonRef.current.contains(event.target);

      if (!clickedInsideMenu && !clickedMenuButton) {
        setMenuOpen(false);
      }
    };

    const handleScroll = () => {
      setMenuOpen(false);
    };

    if (menuOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      window.addEventListener("scroll", handleScroll);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
      window.removeEventListener("scroll", handleScroll);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      window.removeEventListener("scroll", handleScroll);
    };
  }, [menuOpen]);

  const logout = async () => {
    if (!confirm("Logout?")) return;

    const response = await fetch("/api/auth/logout");
    const data = await response.json();
    toast.success(data.message);
    setUser(null);
  };
  return (
    <>
      <header>
        <Link to={"/"}>
          <img
            src="/blu-logo-512.png"
            alt="bluTape logo"
            className="header-logo"
          />
        </Link>
      </header>
      <main>
        <Outlet />
      </main>
      <Navbar />

      <Toaster position="bottom-right" reverseOrder={true} />
    </>
  );
};

export default RootLayout;
