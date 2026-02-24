import styles from "./Machines.module.css";
import { brands } from "../../../utils/Schemas";
import { VENDORS } from "../../../utils/Enums";

const MachineList = ({ machines, onSelectMachine }) => {
  return (
    <ul className={styles.machineList}>
      {machines?.map(
        ({ id, brand, model, serial, color, vendor, latest_work_order }) => (
          <li key={id} onClick={() => onSelectMachine(id)}>
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

              <small className={styles.machineAuthor}>
                {latest_work_order?.initiator?.first_name ?? "Unknown"}
              </small>
            </div>
          </li>
        ),
      )}
    </ul>
  );
};

export default MachineList;
