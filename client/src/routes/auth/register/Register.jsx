import styles from "./Register.module.css";
import React, { useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import { ROLES } from "../../../utils/Enums";
import { requestJson } from "../../../utils/api";

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    role: "",
    email: "",
    password1: "",
    password2: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!confirm("Register new user?")) return;

    try {
      const data = await requestJson("/api/auth/register", {
        method: "POST",
        body: formData,
      });
      toast.success(data.message);
      navigate("/login");
    } catch (error) {
      console.error("[ERROR]: ", error);
      toast.error(error.message);
    }
  };
  return (
    <>
      <form onSubmit={handleSubmit} className={styles.registrationForm}>
        <div>
          <label htmlFor="first_name">First Name</label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="last_name">Last Name</label>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            required
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            required
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="role">Role</label>
          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
            required
          >
            <option value="">--Select Role--</option>
            {Object.entries(ROLES).map(([value, text], index) => (
              <option value={value} key={index}>
                {text}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="password1">Password</label>
          <input
            type="password"
            name="password1"
            value={formData.password1}
            required
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="password2">Re-Enter Password</label>
          <input
            type="password"
            name="password2"
            value={formData.password2}
            required
            onChange={handleChange}
          />
        </div>
        <button>Register</button>
      </form>
    </>
  );
};

export default Register;
