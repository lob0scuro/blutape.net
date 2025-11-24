import React, { useEffect, useRef, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import LOGO from "../assets/blutape-logo.svg";
import { useAuth } from "../context/AuthContext";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faBarsStaggered } from "@fortawesome/free-solid-svg-icons";

const RootLayout = () => {
  const { user, setUser } = useAuth();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    setMenuOpen(false);
  }, [location]);

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
          <img src={LOGO} alt="bluTape logo" className="header-logo" />
        </Link>
        {user && (
          <>
            <FontAwesomeIcon
              icon={menuOpen ? faBarsStaggered : faBars}
              onClick={() => setMenuOpen(!menuOpen)}
            />
            <div id="nav-links" className={menuOpen ? "" : "hidden"}>
              <Link
                to={"/"}
                className={location.pathname === "/" ? "active-link" : ""}
              >
                Home
              </Link>
              <Link
                to={"/machines"}
                className={
                  location.pathname === "/machines" ? "active-link" : ""
                }
              >
                Machines
              </Link>
              <Link
                to={"/search"}
                className={location.pathname === "/search" ? "active-link" : ""}
              >
                Search
              </Link>
            </div>
          </>
        )}
      </header>
      <main>
        <Outlet />
      </main>
      <footer>
        {user && (
          <button id="logout-button" onClick={logout}>
            LOGOUT
          </button>
        )}
        <p>
          <b>bluTape/</b>
        </p>
        <p>Matt's Appliances, LLC</p>
      </footer>
      <Toaster position="bottom-right" reverseOrder={true} />
    </>
  );
};

export default RootLayout;
