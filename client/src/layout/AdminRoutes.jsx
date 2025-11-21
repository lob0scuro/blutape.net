import React from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const AdminRoutes = () => {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  if (loading) return <p>Loading...</p>;
  if (!user.is_admin)
    return (
      <>
        <h2>Admin Panel</h2>
        <p>Unauthorized Access</p>
        <button onClick={() => navigate("/")}>Return to home screen</button>
      </>
    );
  return <Outlet />;
};

export default AdminRoutes;
