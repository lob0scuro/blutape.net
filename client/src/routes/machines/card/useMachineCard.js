import { useCallback, useEffect, useState } from "react";
import toast from "react-hot-toast";
import {
  addMachineNote,
  getMachine,
  printMachineLabel,
  updateMachine,
  updateWorkOrderStatus,
} from "./machineApi";

export const useMachineCard = (id) => {
  const [machine, setMachine] = useState({});
  const [editing, setEditing] = useState({
    machine: false,
    notes: false,
  });
  const [formData, setFormData] = useState({
    brand: "",
    model: "",
    serial: "",
    form_factor: "",
    color: "",
    condition: "",
    vendor: "",
  });
  const [noteContent, setNoteContent] = useState("");

  useEffect(() => {
    const fetchMachine = async () => {
      try {
        const data = await getMachine(id);
        setMachine(data.machine);
        setFormData({
          brand: data.machine.brand,
          model: data.machine.model,
          serial: data.machine.serial,
          form_factor: data.machine.form_factor,
          color: data.machine.color,
          condition: data.machine.condition,
          vendor: data.machine.vendor,
        });
      } catch (error) {
        console.error("[MACHINE FETCH ERROR]: ", error);
        toast.error("Failed to load machine");
        setMachine(null);
      }
    };

    fetchMachine();
  }, [id]);

  const printLabel = useCallback(async () => {
    if (!confirm("Print Label?")) return;
    try {
      const data = await printMachineLabel({
        id,
        model: formData.model,
        serial: formData.serial,
        brand: formData.brand,
        form_factor: formData.form_factor,
        color: formData.color,
      });
      toast.success(data.message);
    } catch (error) {
      console.error("[LABEL ERROR]: ", error);
      toast.error(error.message);
    }
  }, [
    formData.brand,
    formData.color,
    formData.form_factor,
    formData.model,
    formData.serial,
    id,
  ]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleStatusChange = useCallback(
    async (new_status) => {
      const workOrderId = machine?.latest_work_order?.id;
      if (!workOrderId) {
        toast.error("No work order found for this machine");
        return;
      }

      if (!confirm(`Change status to ${new_status}?`)) return;
      try {
        const data = await updateWorkOrderStatus(workOrderId, new_status);
        toast.success(data.message);
        setMachine((prev) => ({
          ...prev,
          current_status: data.work_order?.current_status ?? prev.current_status,
          latest_work_order: data.work_order ?? prev.latest_work_order,
        }));
      } catch (error) {
        console.error("[ERROR]: ", error);
        toast.error(error.message);
      }
    },
    [machine?.latest_work_order?.id],
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!confirm("Submit?")) return;

    try {
      const data = editing.machine
        ? await updateMachine(id, formData)
        : await addMachineNote(id, noteContent);
      if (editing.machine) {
        setMachine(data.machine);
        toast.success(data.message);
        setEditing({ ...editing, machine: false });
      }
      if (editing.notes) {
        setMachine((prev) => ({
          ...prev,
          notes: [...prev.notes, data.note],
        }));
        toast.success(data.message);
        setEditing({ ...editing, notes: false });
        setNoteContent("");
      }
    } catch (error) {
      console.error("[ERROR]: ", error);
      toast.error(error.message);
    }
  };

  return {
    machine,
    editing,
    setEditing,
    formData,
    noteContent,
    setNoteContent,
    printLabel,
    handleChange,
    handleStatusChange,
    handleSubmit,
  };
};
