import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const AdminRoutes = () => {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  if (loading) return <p>Loading...</p>;

  const restrictedAdminRoute =
    location.pathname.startsWith("/admin/metrics") ||
    location.pathname.startsWith("/admin/register");
  const canAccessMetrics = user?.role === "admin";

  if (restrictedAdminRoute && !canAccessMetrics)
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
