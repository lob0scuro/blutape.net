import React from "react";
import { Link, Outlet } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import { useAuth } from "../context/AuthContext";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faRightFromBracket,
} from "@fortawesome/free-solid-svg-icons";
import Navbar from "../components/Navbar";
import { requestJson } from "../utils/api";

const RootLayout = () => {
  const { user, setUser } = useAuth();

  const logout = async () => {
    if (!confirm("Logout?")) return;
    try {
      const data = await requestJson("/api/auth/logout");
      toast.success(data.message || "Logged out");
      setUser(null);
    } catch (error) {
      console.error("[LOGOUT ERROR]: ", error);
      toast.error(error.message || "Failed to logout");
    }
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
        {user && (
          <button className="logout-button" onClick={logout}>
            <FontAwesomeIcon icon={faRightFromBracket} />
          </button>
        )}
      </header>
      <main>
        <Outlet />
      </main>
      {user && <Navbar />}

      <Toaster position="top-center" reverseOrder={true} />
    </>
  );
};

export default RootLayout;
