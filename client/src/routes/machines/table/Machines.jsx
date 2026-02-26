import styles from "./Machines.module.css";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../context/AuthContext";
import TableControls from "./TableControls";
import MachineList from "./MachineList";
import { useMachinesTable } from "./useMachinesTable";

const Machines = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const {
    userID,
    machineStatus,
    machines,
    page,
    totalPages,
    users,
    setPage,
    handleUserChange,
    handleMachineStatusChange,
  } = useMachinesTable(user?.id ?? "");

  return (
    <div className={styles.machineTableContainer}>
      <TableControls
        userID={userID}
        users={users}
        handleUserChange={handleUserChange}
        page={page}
        totalPages={totalPages}
        setPage={setPage}
        machineStatus={machineStatus}
        handleMachineStatusChange={handleMachineStatusChange}
      />
      <MachineList
        machines={machines}
        onSelectMachine={(machineId) => navigate(`/machine/${machineId}`)}
      />
    </div>
  );
};

export default Machines;
