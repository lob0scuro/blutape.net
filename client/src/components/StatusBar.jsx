import styles from "./StatusBar.module.css";
import { STATUS } from "../utils/Enums";

const StatusBar = ({ machineStatus, setMachineStatus }) => {
  return (
    <div className={styles.statusBar}>
      <label htmlFor="machine_status" className={styles.statusLabel}>
        Status
      </label>
      <select
        id="machine_status"
        name="machine_status"
        value={machineStatus}
        onChange={(e) => setMachineStatus(e.target.value)}
        className={styles.statusSelect}
      >
        {Object.entries(STATUS).map(([value, label]) => (
          <option value={value} key={value}>
            {label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default StatusBar;
