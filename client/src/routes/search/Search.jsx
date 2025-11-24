import styles from "./Search.module.css";
import React, { useState } from "react";

const Search = () => {
  const [criteria, setCriteria] = useState("manual");
  return (
    <div className={styles.searchContainer}>
      <div className={styles.searchToggler}>
        <button
          className={criteria === "manual" ? styles.activeButton : ""}
          onClick={() => setCriteria("manual")}
        >
          Manual Search
        </button>
        <button
          className={criteria === "qr" ? styles.activeButton : ""}
          onClick={() => setCriteria("qr")}
        >
          QR Search
        </button>
      </div>
      {criteria === "manual" ? (
        <div className={styles.searchHeader}>
          <div>
            <label htmlFor="model">Model</label>
            <input type="text" name="model" />
          </div>
          <div>
            <label htmlFor="serial">Serial</label>
            <input type="text" name="seiral" />
          </div>
          <div>
            <label htmlFor="brand">Brand</label>
            <select name="brand">
              <option value="">--select brand--</option>
            </select>
          </div>
        </div>
      ) : (
        <div className={styles.searchCamera}>
          <div className={styles.qrFiller}></div>
        </div>
      )}
    </div>
  );
};

export default Search;
