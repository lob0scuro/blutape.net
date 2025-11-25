import toast from "react-hot-toast";
import styles from "./Export.module.css";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faFileExport } from "@fortawesome/free-solid-svg-icons";
import { brands } from "../../../utils/Schemas";
import { TYPES } from "../../../utils/Enums";

const Export = () => {
  const [machines, setMachines] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMachines = async () => {
      const response = await fetch("/api/read/export");
      const data = await response.json();
      if (!data.success) {
        toast.error(data.message);
      }
      if (data.success && data.message) {
        toast.success(data.message);
      }
      setMachines(data.machines);
    };
    fetchMachines();
  }, []);

  const handleExport = async () => {
    if (!confirm("Export machine list?")) return;
    try {
      const response = await fetch("/api/print/export");
      const data = await response.json();
      if (!data.success) {
        throw new Error(data.message);
      }
      toast.success(data.message);
      navigate("/admin/metrics");
    } catch (error) {
      console.error("[ERROR]: ", error);
      toast.error(error.message);
    }
  };

  return (
    <>
      <div className={styles.exportHeader}>
        <h3>Export</h3>
        <button
          onClick={handleExport}
          disabled={machines?.length === 0 || !machines}
        >
          <FontAwesomeIcon icon={faFileExport} />
        </button>
      </div>
      <div className={styles.exportData}>
        {machines?.map(({ id, brand, model, serial, type_of }) => (
          <div key={id} className={styles.exportMachine}>
            <strong>
              {brands[brand]} {TYPES[type_of]}
              <span>
                <FontAwesomeIcon icon={faEye} />
              </span>
            </strong>
            <p>
              <small>Model: </small>
              {model}
            </p>
            <p>
              <small>Serial: </small>
              {serial}
            </p>
          </div>
        ))}
      </div>
    </>
  );
};

export default Export;
