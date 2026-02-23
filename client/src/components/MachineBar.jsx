import styles from "./MachineBar.module.css";
import { APPLIANCE_CATEGORIES } from "../utils/Enums";

const MachineBar = ({ machineType, setMachineType }) => {
  return (
    <div className={styles.machineBarButtonBlock}>
      {Object.entries(APPLIANCE_CATEGORIES).map(([value, label], index) => (
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
