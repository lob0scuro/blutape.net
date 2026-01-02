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
          <img src={LOGO} alt="bluTape logo" className="header-logo" />
        </Link>
        {user && (
          <>
            <FontAwesomeIcon
              icon={menuOpen ? faBarsStaggered : faBars}
              onClick={() => setMenuOpen(!menuOpen)}
              ref={buttonRef}
            />
            <div
              id="nav-links"
              className={menuOpen ? "" : "hidden"}
              ref={menuRef}
            >
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
              <Link
                to={"/read-parts"}
                className={
                  location.pathname === "/read-parts" ? "active-link" : ""
                }
              >
                Parts List
              </Link>

              {user.is_admin && (
                <>
                  <Link
                    to={"/admin/metrics"}
                    className={
                      location.pathname === "/admin/metrics"
                        ? "active-link"
                        : ""
                    }
                  >
                    Metrics
                  </Link>
                  <Link
                    to={"/admin/export"}
                    className={
                      location.pathname === "/admin/export" ? "active-link" : ""
                    }
                  >
                    Export
                  </Link>
                  <Link
                    to={"/admin/add-parts"}
                    className={
                      location.pathname === "/admin/add-parts"
                        ? "active-link"
                        : ""
                    }
                  >
                    Add Parts
                  </Link>
                  <Link
                    to={"/admin/register"}
                    className={
                      location.pathname === "/admin/register"
                        ? "active-link"
                        : ""
                    }
                  >
                    Register
                  </Link>
                </>
              )}
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
