import MachineBar from "../../components/MachineBar";
import styles from "./Home.module.css";
import React, { useState } from "react";
import { brands, colors, machineStyles } from "../../utils/Schemas";
import { MACHINE_CONDITIONS, STATUS, VENDORS } from "../../utils/Enums";

const Home = () => {
  const [machineType, setMachineType] = useState("fridge");
  const [formData, setFormData] = useState({
    brand: "",
    model: "",
    serial: "",
    style: "",
    color: "",
    condition: "",
    vendor: "",
    status: "",
    note: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const renderOptions = (obj) => {
    return Object.entries(obj).map(([value, label], index) => (
      <option value={value} key={index}>
        {label}
      </option>
    ));
  };

  return (
    <>
      <div className={styles.homePageHeader}>
        <MachineBar machineType={machineType} setMachineType={setMachineType} />
      </div>
      <form className={styles.machineFormHome}>
        <div>
          <label htmlFor="model">Model No.</label>
          <input
            type="text"
            name="model"
            value={formData.model}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="serial">Serial No.</label>
          <input
            type="text"
            name="serial"
            value={formData.serial}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="brand">Brand</label>
          <select name="brand" value={formData.brand} onChange={handleChange}>
            <option value="--Select a brand--">--Select a brand--</option>
            {renderOptions(brands)}
          </select>
        </div>
        <div>
          <label htmlFor="style">Style</label>
          <select name="style" value={formData.style} onChange={handleChange}>
            <option value="">--select a style</option>
            {renderOptions(machineStyles[machineType])}
          </select>
        </div>
        <div>
          <label htmlFor="color">Color</label>
          <select name="color" value={formData.color} onChange={handleChange}>
            <option value="">--select a color--</option>
            {renderOptions(colors)}
          </select>
        </div>
        <div>
          <label htmlFor="condition">Condition</label>
          <select
            name="condition"
            value={formData.condition}
            onChange={handleChange}
          >
            <option value="">--select condition--</option>
            {renderOptions(MACHINE_CONDITIONS)}
          </select>
        </div>
        <div>
          <label htmlFor="vendor">Vendor</label>
          <select name="vendor" value={formData.vendor} onChange={handleChange}>
            <option value="">--select vendor--</option>
            {renderOptions(VENDORS)}
          </select>
        </div>
        <div>
          <label htmlFor="status">Status</label>
          <select name="status" value={formData.status} onChange={handleChange}>
            <option value="">--select status--</option>
            {renderOptions(STATUS)}
          </select>
        </div>
        <div>
          <label htmlFor="note">Note</label>
          <textarea
            name="note"
            value={formData.note}
            onChange={handleChange}
          ></textarea>
        </div>
        <button type="submit">Submit</button>
      </form>
    </>
  );
};

export default Home;
