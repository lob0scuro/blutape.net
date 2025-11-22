import styles from "./MachineBar.module.css";
import React from "react";

const lala = [
  "fridge",
  "washer",
  "dryer",
  "range",
  "microwave",
  "water_heater",
  "stackable",
  "dishwasher",
];
const Machines = [
  { value: "fridge", label: "Fridge" },
  { value: "washer", label: "Washer" },
  { value: "dryer", label: "Dryer" },
  { value: "range", label: "Range" },
];

const MachineBar = ({ machineType, setMachineType }) => {
  return (
    <div className={styles.machineBarButtonBlock}>
      {Machines.map(({ value, label }, index) => (
        <button
          key={index}
          onClick={() => setMachineType(value)}
          className={machineType === value ? styles.activeButton : ""}
        >
          {label}
        </button>
      ))}
    </div>
  );
};

export default MachineBar;
