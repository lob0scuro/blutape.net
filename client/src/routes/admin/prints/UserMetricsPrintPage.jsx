import { brands } from "../../../utils/Schemas";
import { formatDate } from "../../../utils/Tools";
import styles from "./UserMetricsPrintPage.module.css";
import React, { forwardRef } from "react";

const UserMetricsPrintPage = forwardRef(
  ({ start_date, end_date, metrics }, ref) => {
    if (!metrics) return <p>sike!!</p>;
    return (
      <div className={styles.metricPrintData} ref={ref}>
        <h1>
          {metrics.user.first_name} {metrics.user.last_name}
        </h1>
        <div>
          <h3>In-Progress</h3>
          <ul>
            {metrics.in_progress.machines.map(({ id, brand, style, model }) => (
              <li key={id}>
                {brands[brand]} {style} <strong>{model}</strong>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3>Completed</h3>
          <p>
            Between {formatDate(start_date)} and {formatDate(end_date)}
          </p>
          <ul>
            {metrics.completed.machines.map(({ id, brand, style, model }) => (
              <li key={id}>
                {brands[brand]} {style} <strong>{model}</strong>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3>Trashed</h3>
          <p>
            Between {formatDate(start_date)} and {formatDate(end_date)}
          </p>
          <ul>
            {metrics.trashed.machines.map(({ id, brand, style, model }) => (
              <li key={id}>
                {brands[brand]} {style} <strong>{model}</strong>
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
);

export default UserMetricsPrintPage;
