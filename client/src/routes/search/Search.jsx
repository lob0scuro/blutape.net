import styles from "./Search.module.css";
import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCircleInfo,
  faKeyboard,
  faQrcode,
} from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { brands } from "../../utils/Schemas";
import { APPLIANCE_CATEGORIES, COLORS, FORM_FACTOR, STATUS } from "../../utils/Enums";
import { Scanner } from "@yudiel/react-qr-scanner";
import { requestJson } from "../../utils/api";

const Search = () => {
  const [serialSearch, setSerialSearch] = useState(true);
  const [machine, setMachine] = useState(null);
  const [serial, setSerial] = useState("");
  const navigate = useNavigate();
  const toggleSearchMode = (useSerialSearch) => {
    setSerialSearch(useSerialSearch);
    setMachine(null);
    setSerial("");
  };
  const handleSerialChange = (value) => {
    const next = value.toUpperCase();
    if (!next.trim()) {
      setMachine(null);
    }
    setSerial(next);
  };

  useEffect(() => {
    const normalizedSerial = serial.trim();
    if (!normalizedSerial) {
      return;
    }

    let isActive = true;

    const delayDebounce = setTimeout(async () => {
      try {
        const data = await requestJson(
          `/api/read/serial/${encodeURIComponent(normalizedSerial)}`,
        );

        if (!isActive) return;

        setMachine(data.machine);
      } catch (error) {
        console.error("[SERIAL SEARCH ERROR]: ", error);
        toast.error("Failed to search serial number");
        setMachine(null);
      }
    }, 600);

    return () => {
      isActive = false;
      clearTimeout(delayDebounce);
    };
  }, [serial]);

  const handleScan = (detectedCodes) => {
    if (!detectedCodes || detectedCodes.length === 0) return;
    const value = detectedCodes[0].rawValue;
    if (!value) return;

    setSerial(value.trim());
  };

  return (
    <div className={styles.searchContainer}>
      <div className={styles.searchToggler}>
        <button
          className={serialSearch ? styles.activeButton : ""}
          onClick={() => toggleSearchMode(true)}
        >
          <FontAwesomeIcon icon={faKeyboard} />
        </button>
        <button
          className={!serialSearch ? styles.activeButton : ""}
          onClick={() => toggleSearchMode(false)}
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
            onChange={(e) => handleSerialChange(e.target.value)}
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
              {brands[machine.brand]} {APPLIANCE_CATEGORIES[machine.category]}
            </h2>
            <p>Model: {machine.model}</p>
            <p>Serial: {machine.serial}</p>
            <p>Color: {COLORS[machine.color] ?? machine.color}</p>
            <p>
              Style:{" "}
              {FORM_FACTOR(machine.category)[machine.form_factor] ??
                machine.form_factor}
            </p>
            <p>
              <small>
                Status: {STATUS[machine.current_status] ?? machine.current_status}
              </small>
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
