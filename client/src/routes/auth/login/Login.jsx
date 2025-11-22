import styles from "./Login.module.css";
import React, { useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../context/AuthContext";

const Login = () => {
  const { setUser } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (!data.success) {
        throw new Error(data.message);
      }
      setUser(data.user);
      toast.success(data.message);
      navigate("/");
    } catch (error) {
      console.error("[LOGIN ERROR]: ", error);
      toast.error(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.loginForm}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          type="email"
          name="email"
          value={email}
          required
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input
          type="password"
          name="password"
          value={password}
          required
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;
