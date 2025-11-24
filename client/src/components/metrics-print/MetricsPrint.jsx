import styles from "./MetricsPrint.module.css";
import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { formatDate } from "../../utils/Tools";
import { brands } from "../../utils/Schemas";

const MetricsPrint = () => {
  const [metrics, setMetrics] = useState(null);
  const [user, setUser] = useState(null);

  const params = new URLSearchParams(useLocation().search);
  const user_id = params.get("user_id");
  const start_date = params.get("start_date");
  const end_date = params.get("end_date");

  useEffect(() => {
    const fetchData = async () => {
      const u = await fetch(`/api/read/user/${user_id}`).then((r) => r.json());
      const m = await fetch(
        `/api/read/metrics/${user_id}?start_date=${start_date}&end_date=${end_date}`
      ).then((r) => r.json());

      if (u.success) setUser(u.user);
      if (m.success) setMetrics(m.metrics);

      setTimeout(() => window.print(), 250);
    };

    fetchData();
  }, []);

  if (!metrics || !user) return <p>Loading...</p>;

  return (
    <div className="printPage">
      <h1>
        {user.first_name} {user.last_name}
      </h1>
      <p>
        Machine Metrics • {formatDate(start_date)} → {formatDate(end_date)}
      </p>

      <h2>In Progress ({metrics.in_progress.count})</h2>
      <ul>
        {metrics.in_progress.machines.map(({ id, brand, model, serial }) => (
          <li key={id}>
            {brands[brand]} — Model: {model} — Serial: {serial}
          </li>
        ))}
      </ul>

      <h2>Completed ({metrics.completed.count})</h2>
      <ul>
        {metrics.completed.machines.map(({ id, brand, model, serial }) => (
          <li key={id}>
            {brands[brand]} — Model: {model} — Serial: {serial}
          </li>
        ))}
      </ul>

      <h2>Trashed ({metrics.trashed.count})</h2>
      <ul>
        {metrics.trashed.machines.map(({ id, brand, model, serial }) => (
          <li key={id}>
            {brands[brand]} — Model: {model} — Serial: {serial}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MetricsPrint;
