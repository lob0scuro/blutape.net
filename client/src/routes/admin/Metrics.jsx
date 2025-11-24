import styles from "./Metrics.module.css";
import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";

const Metrics = () => {
  const [users, setUsers] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [params, setParams] = useState({
    start_date: null,
    end_date: null,
    date_column: null,
    user_id: null,
  });

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await fetch(`/api/read/users`);
      const data = await response.json();
      if (!data.success) {
        toast.error(data.message);
        return;
      }
      setUsers(data.users);
    };
    fetchUsers();
  }, []);

  useEffect(() => {
    const fetchMetrics = async () => {
      const response = await fetch(`/api/read/metrics/${params.user_id}`);
      const data = await response.json();
      if (!data.success) {
        toast.error(data.message);
      }
      console.log(data.metrics);
      setMetrics(data.metrics);
    };
    if (params.user_id !== "") {
      fetchMetrics();
    }
  }, [params.user_id]);

  return (
    <div className={styles.metricsContainer}>
      <div className={styles.userSelect}>
        <select
          name="userID"
          value={params.user_id}
          onChange={(e) => setParams({ ...params, user_id: e.target.value })}
        >
          <option value={null}>--select user--</option>
          {users?.map(({ id, first_name, last_name }) => (
            <option value={id} key={id}>
              {first_name} {last_name}
            </option>
          ))}
        </select>
      </div>
      {metrics && (
        <div className={styles.metricsData}>
          <ul className={styles.inProgressMachines}>
            <h2>
              <span>{metrics.in_progress.count}</span> In Progress
            </h2>
            {metrics.in_progress.machines.map(
              ({ id, brand, model, serial }) => (
                <li key={id}>{brand}</li>
              )
            )}
          </ul>
          <ul className={styles.completedMachines}>
            <h2>
              <span>{metrics.completed.count}</span> Completed
            </h2>
            {metrics.completed.machines.map(({ id, brand, model, serial }) => (
              <li key={id}>{brand}</li>
            ))}
            <li>{metrics.completed.count}</li>
          </ul>
          <ul className={styles.trashedMachines}>
            <h2>
              <span>{metrics.trashed.count}</span> Trashed
            </h2>
            {metrics.trashed.machines.map(({ id, brand, model, serial }) => (
              <li key={id}>{brand}</li>
            ))}
            <li>{metrics.trashed.count}</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default Metrics;
