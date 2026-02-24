import styles from "./Card.module.css";
import { brands, colors } from "../../../utils/Schemas";
import {
  VENDORS,
  MACHINE_CONDITIONS,
  FORM_FACTOR,
  COLORS,
} from "../../../utils/Enums";

const renderOptions = (obj) => {
  return Object.entries(obj).map(([value, label], index) => (
    <option value={value} key={index}>
      {label}
    </option>
  ));
};

const MachineDetailsForm = ({
  machine,
  editingMachine,
  formData,
  handleChange,
  handleSubmit,
}) => {
  return (
    <form className={styles.machineCardEditForm} onSubmit={handleSubmit}>
      <ul>
        <li>
          {editingMachine ? (
            <>
              <label htmlFor="model">Model No.</label>
              <input
                type="text"
                name="model"
                value={formData.model}
                onChange={handleChange}
              />
            </>
          ) : (
            <p>
              Model <span>{machine.model}</span>
            </p>
          )}
        </li>
        <li>
          {editingMachine ? (
            <>
              <label htmlFor="serial">Serial</label>
              <input
                type="text"
                name="serial"
                value={formData.serial}
                onChange={handleChange}
              />
            </>
          ) : (
            <p>
              Serial <span>{machine.serial}</span>
            </p>
          )}
        </li>
        <li>
          {editingMachine ? (
            <>
              <label htmlFor="brand">Brand</label>
              <select name="brand" value={formData.brand} onChange={handleChange}>
                <option value="">--select brand--</option>
                {renderOptions(brands)}
              </select>
            </>
          ) : (
            <p>
              Brand <span>{brands[machine.brand]}</span>
            </p>
          )}
        </li>
        <li>
          {editingMachine ? (
            <>
              <label htmlFor="form_factor">Style</label>
              <select
                name="form_factor"
                value={formData.form_factor}
                onChange={handleChange}
              >
                <option value="">--select style--</option>
                {Object.entries(FORM_FACTOR(machine.category)).map(
                  ([value, label], index) => (
                    <option value={value} key={index}>
                      {label}
                    </option>
                  ),
                )}
              </select>
            </>
          ) : (
            <p>
              Style <span>{FORM_FACTOR(machine.category)[machine.form_factor]}</span>
            </p>
          )}
        </li>
        <li>
          {editingMachine ? (
            <>
              <label htmlFor="color">Color</label>
              <select name="color" value={formData.color} onChange={handleChange}>
                <option value="">--select color--</option>
                {renderOptions(colors)}
              </select>
            </>
          ) : (
            <p>
              Color <span>{COLORS[machine.color]}</span>
            </p>
          )}
        </li>
        <li>
          {editingMachine ? (
            <>
              <label htmlFor="condition">Condition</label>
              <select
                name="condition"
                value={formData.condition}
                onChange={handleChange}
              >
                <option value="">--select condition--</option>
                {renderOptions(MACHINE_CONDITIONS)}
              </select>
            </>
          ) : (
            <p>
              Condition <span>{MACHINE_CONDITIONS[machine.condition]}</span>
            </p>
          )}
        </li>
        <li>
          {editingMachine ? (
            <>
              <label htmlFor="vendor">Vendor</label>
              <select name="vendor" value={formData.vendor} onChange={handleChange}>
                <option value="">--select vendor--</option>
                {renderOptions(VENDORS)}
              </select>
            </>
          ) : (
            <p>
              Vendor <span>{VENDORS[machine.vendor]}</span>
            </p>
          )}
        </li>
        {editingMachine && <button type="submit">Submit</button>}
      </ul>
    </form>
  );
};

export default MachineDetailsForm;
