import { requestJson } from "../../../utils/api";

export const getUsers = async () => {
  return requestJson("/api/read/users");
};

export const getMachines = async ({ userID, machineStatus, page }) => {
  return requestJson(
    `/api/read/machines?user_id=${userID}&status=${machineStatus}&page=${page}`,
  );
};
