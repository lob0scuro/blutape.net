import styles from "./Search.module.css";
import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCircleInfo,
  faKeyboard,
  faQrcode,
} from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { brands, colors, machineStyles } from "../../utils/Schemas";
import { TYPES } from "../../utils/Enums";
import { Scanner } from "@yudiel/react-qr-scanner";

const Search = () => {
  const [serialSearch, setSerialSearch] = useState(true);
  const [machine, setMachine] = useState(null);
  const [serial, setSerial] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!serial) {
      setMachine(null);
      return;
    }

    const delayDebounce = setTimeout(async () => {
      const response = await fetch(`/api/read/serial/${serial}`);
      const data = await response.json();

      if (!data.success) {
        toast.error(data.message);
        setMachine(null);
        return;
      }

      setMachine(data.machine);
    }, 1000); // wait 500ms after user stops typing

    return () => clearTimeout(delayDebounce);
  }, [serial]);

  useEffect(() => {
    setMachine(null);
    setSerial("");
  }, [serialSearch]);

  const handleScan = (detetectedCodes) => {
    if (!detetectedCodes || detetectedCodes.length === 0) return;

    console.log(detetectedCodes[0].rawValue);
    const value = detetectedCodes[0].rawValue;
    if (!value) return;

    setSerial(value);
  };

  return (
    <div className={styles.searchContainer}>
      <div className={styles.searchToggler}>
        <button
          className={serialSearch ? styles.activeButton : ""}
          onClick={() => setSerialSearch(true)}
        >
          <FontAwesomeIcon icon={faKeyboard} />
        </button>
        <button
          className={!serialSearch ? styles.activeButton : ""}
          onClick={() => setSerialSearch(false)}
        >
          <FontAwesomeIcon icon={faQrcode} />
        </button>
      </div>
      {serialSearch ? (
        <div className={styles.serialSearchInput}>
          <label htmlFor="serial">Search by serial number</label>
          <input
            type="text"
            name="serial"
            value={serial}
            onChange={(e) => setSerial(e.target.value)}
          />
        </div>
      ) : (
        <div className={styles.searchCamera}>
          <p>QR Search</p>
          <div className={styles.qrFiller}>
            <Scanner
              onScan={handleScan}
              components={{ audio: true }}
              constraints={{ facingMode: "environment" }}
            />
          </div>
        </div>
      )}
      {machine && (
        <div className={styles.machineFound}>
          <div>
            <h2>
              {brands[machine.brand]} {TYPES[machine.type_of]}
            </h2>
            <p>Model: {machine.model}</p>
            <p>Serial: {machine.serial}</p>
            {/* <p>Color: {colors[machine.color]}</p> */}
            <p>Style: {machine.style}</p>
            <p>
              <small>Status: {machine.status}</small>
            </p>
          </div>
          <FontAwesomeIcon
            icon={faCircleInfo}
            onClick={() => navigate(`/machine/${machine.id}`)}
          />
        </div>
      )}
    </div>
  );
};

export default Search;
