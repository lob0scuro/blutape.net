import styles from "./Metrics.module.css";
import React, { useEffect, useState, useRef } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import { formatDate, getToday, shiftDate } from "../../utils/Tools";
import { brands, machineStyles } from "../../utils/Schemas";
import { TYPES } from "../../utils/Enums";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faPrint } from "@fortawesome/free-solid-svg-icons";
import { useReactToPrint } from "react-to-print";
import UserMetricsPrintPage from "./prints/UserMetricsPrintPage";

const Metrics = () => {
  const [users, setUsers] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [params, setParams] = useState({
    start_date: getToday(),
    end_date: getToday(),
    user_id: null,
  });
  const navigate = useNavigate();
  const contentRef = useRef(null);

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
      setMetrics(data.metrics);
    };
    if (params.user_id !== "" && params.user_id !== null) {
      fetchMetrics();
    }
  }, [params]);

  useEffect(() => {
    if (params.user_id === "") {
      setMetrics(null);
    }
  }, [params.user_id]);

  const exportReport = async () => {
    if (!params.user_id) {
      toast.error("Please select a user first");
      return;
    }

    // Determine format based on window size
    const isMobile = window.matchMedia("(max-width: 500px)").matches;
    const format = isMobile ? "pdf" : "csv";

    // Build API base
    const API_BASE =
      import.meta.env.MODE === "development"
        ? ""
        : import.meta.env.VITE_SERVER_URL || "";

    const url = `${API_BASE}/api/export/user_report/${params.user_id}?start=${params.start_date}&end=${params.end_date}&format=${format}`;

    try {
      const response = await fetch(url, { credentials: "include" });
      if (!response.ok) {
        const err = await response.json();
        toast.error(err.message);
        return;
      }

      const blob = await response.blob();
      const filename = format === "csv" ? "user_report.csv" : "user_report.pdf";
      const blobURL = window.URL.createObjectURL(blob);

      if (format === "pdf") {
        // PDF: open in new tab only
        window.open(blobURL, "_blank");
      } else {
        // CSV: automatically download
        const a = document.createElement("a");
        a.href = blobURL;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(blobURL);
      }
    } catch (error) {
      console.error("[EXPORT ERROR]: ", error);
      toast.error("There was an error exporting the report");
    }
  };

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
              disabled={
                params.end_date === getToday() ||
                params.start_date !== params.end_date
              }
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
            value={params.user_id ?? ""}
            onChange={(e) => setParams({ ...params, user_id: e.target.value })}
          >
            <option value="">--select user--</option>
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
          <h1 className={styles.metricsTitle}>{metrics.user}</h1>
          <ul className={styles.inProgressMachines}>
            <li>
              <h2>
                <span>{metrics.in_progress.count}</span> In Progress
              </h2>
            </li>

            {metrics.in_progress.machines.map(
              ({ id, brand, model, serial, style }) => (
                <li key={id}>
                  <p>
                    {brands[brand]} {style}{" "}
                    <span>
                      <FontAwesomeIcon
                        icon={faEye}
                        onClick={() => navigate(`/machine/${id}`)}
                        className={styles.gotomachine}
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
            <li>
              <h2>
                <span>{metrics.completed.count}</span> Completed
              </h2>
              <p className={styles.machineListDate}>
                Between {formatDate(params.start_date)} and{" "}
                {formatDate(params.end_date)}
              </p>
            </li>
            {metrics.completed.machines.map(
              ({ id, brand, model, serial, style }) => (
                <li key={id}>
                  <p>
                    {brands[brand]} {style}{" "}
                    <span>
                      <FontAwesomeIcon
                        icon={faEye}
                        onClick={() => navigate(`/machine/${id}`)}
                        className={styles.gotomachine}
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
            <li>
              <h2>
                <span>{metrics.trashed.count}</span> Trashed
              </h2>
              <p className={styles.machineListDate}>
                Between {formatDate(params.start_date)} and{" "}
                {formatDate(params.end_date)}
              </p>
            </li>
            {metrics.trashed.machines.map(
              ({ id, brand, model, serial, style }) => (
                <li key={id}>
                  <p>
                    {brands[brand]} {style}{" "}
                    <span>
                      <FontAwesomeIcon
                        icon={faEye}
                        onClick={() => navigate(`/machine/${id}`)}
                        className={styles.gotomachine}
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
      {metrics && (
        <button className={styles.printMetricsButton} onClick={exportReport}>
          <FontAwesomeIcon icon={faPrint} />
        </button>
      )}
    </div>
  );
};

export default Metrics;
