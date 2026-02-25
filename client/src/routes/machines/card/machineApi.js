import { requestJson } from "../../../utils/api";

export const getMachine = async (id) => {
  return requestJson(`/api/read/machine/${id}`);
};

export const printMachineLabel = async ({
  id,
  model,
  serial,
  brand,
  form_factor,
  color,
}) => {
  return requestJson("/api/print/label", {
    method: "POST",
    body: {
      id,
      model,
      serial,
      brand,
      form_factor,
      color,
    },
  });
};

export const updateWorkOrderStatus = async (workOrderId, new_status) => {
  return requestJson(`/api/update/work_order/${workOrderId}/status`, {
    method: "PATCH",
    body: { new_status },
  });
};

export const updateMachine = async (id, formData) => {
  return requestJson(`/api/update/machine/${id}`, {
    method: "PATCH",
    body: formData,
  });
};

export const addMachineNote = async (id, note) => {
  return requestJson(`/api/create/note/${id}`, {
    method: "POST",

    body: { content: note },
  });
};
