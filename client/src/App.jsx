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

const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<RootLayout />}>
        <Route element={<ProtectedRoutes />}>
          <Route index element={<Home />} />
          <Route path="machines" element={<Machines />} />
          <Route path="machine/:id" element={<Card />} />
        </Route>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
      </Route>
    )
  );
  return <RouterProvider router={router} />;
};

export default App;
