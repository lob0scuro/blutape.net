import StatusBar from "../../../components/StatusBar";
import styles from "./Machines.module.css";
import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../context/AuthContext";
import { brands } from "../../../utils/Schemas";
import { VENDORS } from "../../../utils/Enums";

const Machines = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [userID, setUserID] = useState(user.id);
  const [machineStatus, setMachineStatus] = useState("in_progress");
  const [machines, setMachines] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await fetch("/api/read/users");
      const data = await response.json();
      if (!data.success) {
        toast.error(data.message);
        setUsers(null);
        return;
      }
      setUsers(data.users);
    };
    fetchUsers();
  }, []);

  useEffect(() => {
    const fetchMachines = async () => {
      try {
        const response = await fetch(
          `/api/read/machines?user_id=${userID}&status=${machineStatus}&page=${page}`
        );
        const data = await response.json();
        if (!data.success) {
          throw new Error(data.message);
        }
        setMachines(data.machines);
        setTotalPages(data.total_pages);
        setTotalItems(data.total_items);
      } catch (error) {
        console.error("[MACHINE QUERY ERROR]: ", error);
        toast.error(error.message);
      }
    };
    fetchMachines();
  }, [machineStatus, userID, page]);

  return (
    <div className={styles.machineTableContainer}>
      <div className={styles.machineTableHeader}>
        <div className={styles.tableController}>
          <select
            name="user_id"
            value={userID}
            onChange={(e) => setUserID(e.target.value)}
            className={styles.machineTableUserSelect}
          >
            <option value="">All</option>
            {users.map(({ id, first_name, last_name }) => (
              <option value={id} key={id}>
                {first_name} {last_name}
              </option>
            ))}
          </select>
          <div className={styles.paginator}>
            <button
              disabled={page === 1}
              onClick={() => setPage((prev) => prev - 1)}
            >
              prev
            </button>
            <span>
              {page} / {totalPages}
            </span>
            <button
              disabled={page === totalPages}
              onClick={() => setPage((prev) => prev + 1)}
            >
              next
            </button>
          </div>
        </div>
        <StatusBar
          machineStatus={machineStatus}
          setMachineStatus={setMachineStatus}
        />
      </div>
      <ul className={styles.machineList}>
        {machines?.map(
          ({ id, brand, model, serial, color, vendor, tech_name, notes }) => (
            <li key={id} onClick={() => navigate(`/machine/${id}`)}>
              <h2>
                {brands[brand]} - <small>[{model}]</small>
              </h2>
              <div>
                <p>
                  Serial: <span>{serial}</span>
                </p>
                <p>
                  Color: <span>{color}</span>
                </p>
                <p>
                  Vendor: <span>{VENDORS[vendor]}</span>
                </p>
                <p>
                  Notes: <span>{notes.length - 1}</span>
                </p>
                <small className={styles.machineAuthor}>{tech_name}</small>
              </div>
            </li>
          )
        )}
      </ul>
    </div>
  );
};

export default Machines;
