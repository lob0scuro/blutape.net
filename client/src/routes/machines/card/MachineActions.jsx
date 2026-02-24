import { memo } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const MachineActions = ({ actions }) => {
  return (
    <>
      {actions.map(({ icon, className, onClick, disabled }, idx) => (
        <button
          key={idx}
          className={className}
          onClick={onClick}
          disabled={disabled}
        >
          <FontAwesomeIcon icon={icon} />
        </button>
      ))}
    </>
  );
};

export default memo(MachineActions);
