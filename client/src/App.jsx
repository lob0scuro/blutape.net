import React from "react";
import {
  Route,
  RouterProvider,
  createBrowserRouter,
  createRoutesFromElements,
} from "react-router-dom";
import RootLayout from "./layout/RootLayout";
import ProtectedRoutes from "./layout/ProtectedLayout";
import AdminRoutes from "./layout/AdminRoutes";
import Home from "./routes/home/Home";
import Login from "./routes/auth/login/Login";
import Register from "./routes/auth/register/Register";
import Machines from "./routes/machines/table/Machines";
import Card from "./routes/machines/card/Card";
import Search from "./routes/search/Search";
import Metrics from "./routes/admin/Metrics";

const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<RootLayout />}>
        <Route element={<ProtectedRoutes />}>
          <Route index element={<Home />} />
          <Route path="machines" element={<Machines />} />
          <Route path="machine/:id" element={<Card />} />
          <Route path="search" element={<Search />} />
          <Route path="admin" element={<AdminRoutes />}>
            <Route path="metrics" element={<Metrics />} />
            <Route path="register" element={<Register />} />
          </Route>
        </Route>
        <Route path="login" element={<Login />} />
      </Route>
    )
  );
  return <RouterProvider router={router} />;
};

export default App;
