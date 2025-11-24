import styles from "./Metrics.module.css";
import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import { formatDate, getToday, shiftDate } from "../../utils/Tools";
import { brands, machineStyles } from "../../utils/Schemas";
import { TYPES } from "../../utils/Enums";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faPrint } from "@fortawesome/free-solid-svg-icons";

const Metrics = () => {
  const [users, setUsers] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [params, setParams] = useState({
    start_date: getToday(),
    end_date: getToday(),
    date_column: null,
    user_id: null,
  });
  const navigate = useNavigate();

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
      const response = await fetch(
        `/api/read/metrics/${params.user_id}?start_date=${params.start_date}&end_date=${params.end_date}`
      );
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
  }, [params]);

  return (
    <div className={styles.metricsContainer}>
      <div className={styles.userSelect}>
        <div className={styles.metricsDateSelect}>
          <div>
            <button
              className={styles.shiftDayButton}
              onClick={() => {
                const d = shiftDate(params.start_date, -1);
                const dd = shiftDate(params.end_date, -1);
                setParams({ ...params, start_date: d, end_date: dd });
              }}
              disabled={params.start_date !== params.end_date}
            >
              prev
            </button>
            <button
              onClick={() =>
                setParams({
                  ...params,
                  start_date: getToday(),
                  end_date: getToday(),
                })
              }
              disabled={
                params.start_date == getToday() && params.end_date == getToday()
              }
            >
              Today
            </button>
            <button
              className={styles.shiftDayButton}
              onClick={() => {
                const d = shiftDate(params.start_date, 1);
                const dd = shiftDate(params.end_date, 1);
                setParams({ ...params, start_date: d, end_date: dd });
              }}
              disabled={params.end_date === getToday()}
            >
              next
            </button>
          </div>
          <div>
            <label htmlFor="start_date">Start Date</label>
            <input
              type="date"
              name="start_date"
              value={params.start_date}
              onChange={(e) =>
                setParams({ ...params, start_date: e.target.value })
              }
            />
          </div>

          <div>
            <label htmlFor="end_date">End Date</label>
            <input
              type="date"
              name="end_date"
              value={params.end_date}
              onChange={(e) =>
                setParams({ ...params, end_date: e.target.value })
              }
            />
          </div>
        </div>
        <div>
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
      </div>
      {metrics && (
        <div className={styles.metricsData}>
          <FontAwesomeIcon
            icon={faPrint}
            className={styles.printMetricsButton}
            onClick={() =>
              navigate(
                `/admin/metrics/print?user_id=${params.user_id}&start_date=${params.start_date}&end_date=${params.end_date}`
              )
            }
          />

          <ul className={styles.inProgressMachines}>
            <h2>
              <span>{metrics.in_progress.count}</span> In Progress
            </h2>

            {metrics.in_progress.machines.map(
              ({ id, brand, model, serial, style }) => (
                <li key={id}>
                  <p>
                    {brands[brand]} {style}{" "}
                    <span>
                      <FontAwesomeIcon
                        icon={faEye}
                        onClick={() => navigate(`/machine/${id}`)}
                      />
                    </span>
                  </p>
                  <p>
                    model:<small>[{model}]</small>
                  </p>
                  <p>
                    serial:<small>[{serial}]</small>
                  </p>
                </li>
              )
            )}
          </ul>
          <ul className={styles.completedMachines}>
            <h2>
              <span>{metrics.completed.count}</span> Completed
            </h2>
            <p className={styles.machineListDate}>
              Between {formatDate(params.start_date)} and{" "}
              {formatDate(params.end_date)}
            </p>
            {metrics.completed.machines.map(
              ({ id, brand, model, serial, style }) => (
                <li key={id}>
                  <p>
                    {brands[brand]} {style}{" "}
                    <span>
                      <FontAwesomeIcon
                        icon={faEye}
                        onClick={() => navigate(`/machine/${id}`)}
                      />
                    </span>
                  </p>
                  <p>
                    model:<small>[{model}]</small>
                  </p>
                  <p>
                    serial:<small>[{serial}]</small>
                  </p>
                </li>
              )
            )}
          </ul>
          <ul className={styles.trashedMachines}>
            <h2>
              <span>{metrics.trashed.count}</span> Trashed
            </h2>
            <p className={styles.machineListDate}>
              Between {formatDate(params.start_date)} and{" "}
              {formatDate(params.end_date)}
            </p>
            {metrics.trashed.machines.map(
              ({ id, brand, model, serial, style }) => (
                <li key={id}>
                  <p>
                    {brands[brand]} {style}{" "}
                    <span>
                      <FontAwesomeIcon
                        icon={faEye}
                        onClick={() => navigate(`/machine/${id}`)}
                      />
                    </span>
                  </p>
                  <p>
                    model:<small>[{model}]</small>
                  </p>
                  <p>
                    serial:<small>[{serial}]</small>
                  </p>
                </li>
              )
            )}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Metrics;
