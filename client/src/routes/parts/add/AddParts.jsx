import styles from "./AddParts.module.css";
import React, { useState } from "react";
import { useAuth } from "../../../context/AuthContext";
import toast from "react-hot-toast";

const AddParts = () => {
  const [formData, setFormData] = useState({
    part_no: "",
    price: "",
    quantity: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  return (
    <form className={styles.partsForm}>
      <fieldset>
        <legend>Add new part</legend>
        <div>
          <label htmlFor="part_no">Part No.</label>
          <input type="text" name="part_no" id="part_no" />
        </div>
        <div>
          <label htmlFor="price">Price</label>
          <input type="number" name="price" id="price" />
        </div>
        <div>
          <label htmlFor="quantity">QTY</label>
          <input type="number" name="quantity" id="quantity" />
        </div>
      </fieldset>
      <button type="submit">Submit</button>
    </form>
  );
};

export default AddParts;
