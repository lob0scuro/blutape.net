import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { getMachines, getUsers } from "./machineTableApi";

export const useMachinesTable = (initialUserID = "") => {
  const [userID, setUserID] = useState(initialUserID);
  const [machineStatus, setMachineStatus] = useState("in_progress");
  const [machines, setMachines] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [users, setUsers] = useState([]);

  const handleUserChange = (e) => {
    setUserID(e.target.value);
    setPage(1);
  };

  const handleMachineStatusChange = (status) => {
    setMachineStatus(status);
    setPage(1);
  };

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await getUsers();
        setUsers(data.users);
      } catch (error) {
        console.error("[USER QUERY ERROR]: ", error);
        toast.error("Failed to load users");
        setUsers([]);
      }
    };
    fetchUsers();
  }, []);

  useEffect(() => {
    const fetchMachines = async () => {
      try {
        const data = await getMachines({ userID, machineStatus, page });
        setMachines(data.machines);
        setTotalPages(data.total_pages);
      } catch (error) {
        console.error("[MACHINE QUERY ERROR]: ", error);
        toast.error(error.message);
      }
    };
    fetchMachines();
  }, [machineStatus, page, userID]);

  return {
    userID,
    machineStatus,
    machines,
    page,
    totalPages,
    users,
    setPage,
    handleUserChange,
    handleMachineStatusChange,
  };
};
