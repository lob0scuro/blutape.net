import clsx from "clsx";
import styles from "./Card.module.css";

const STATUS_MAP = {
  in_progress: {
    className: styles.ipHead,
    label: "In Progress",
  },
  completed: {
    className: styles.cHead,
    label: "Complete",
  },
  trashed: {
    className: styles.tHead,
    label: "Trashed",
  },
  exported: {
    className: styles.eHead,
    label: "Exported",
  },
};

const MachineStatusBadge = ({ currentStatus }) => {
  const statusConfig = STATUS_MAP[currentStatus];

  return (
    <div className={clsx(styles.statusDisplay, statusConfig?.className ?? "")}>
      {statusConfig?.label ?? ""}
    </div>
  );
};

export default MachineStatusBadge;
