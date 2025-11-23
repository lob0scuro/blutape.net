import styles from "./StatusBar.module.css";
import React from "react";
import { STATUS } from "../utils/Enums";

const StatusBar = ({ machineStatus, setMachineStatus }) => {
  return (
    <div className={styles.statusBar}>
      {Object.entries(STATUS).map(([value, label], index) => (
        <button
          key={index}
          className={value === machineStatus ? styles.activeButton : ""}
          onClick={() => setMachineStatus(value)}
        >
          {label}
        </button>
      ))}
    </div>
  );
};

export default StatusBar;
