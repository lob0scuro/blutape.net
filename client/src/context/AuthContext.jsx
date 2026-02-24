import React, { useContext, createContext, useEffect, useState } from "react";
import { requestJson } from "../utils/api";

const UserContext = createContext();

export const AuthContext = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await requestJson("/api/auth/hydrate");
        setUser(data.user);
      } catch (error) {
        console.error("Error when fetching user: ", error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser, loading, setLoading }}>
      {children}
    </UserContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(UserContext);
