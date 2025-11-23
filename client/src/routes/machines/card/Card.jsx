import styles from "./Card.module.css";
import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import toast from "react-hot-toast";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPenClip,
  faPenToSquare,
  faPrint,
  faRecycle,
  faRotateLeft,
  faScrewdriverWrench,
  faSquareCheck,
  faTrashCan,
} from "@fortawesome/free-solid-svg-icons";
import { brands, colors, machineStyles } from "../../../utils/Schemas";
import { VENDORS, MACHINE_CONDITIONS, TYPES } from "../../../utils/Enums";
import { formatDate } from "../../../utils/Tools";

{
  /* <h1
  style={{ textAlign: "center", marginTop: "3rem", fontSize: "1.8rem" }}
>
  Machine Not Found
</h1> */
}

{
  /* <FontAwesomeIcon icon={faPrint} /> */
}
{
  /* <FontAwesomeIcon icon={faSquareCheck} /> */
}
{
  /* <FontAwesomeIcon icon={faScrewdriverWrench} /> */
}
{
  /* <FontAwesomeIcon icon={faPenClip} /> */
}
{
  /* <FontAwesomeIcon icon={faRecycle} /> */
}

const Card = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [machine, setMachine] = useState({});
  const [editing, setEditing] = useState({
    machine: false,
    notes: false,
  });
  const [formData, setFormData] = useState({
    brand: "",
    model: "",
    serial: "",
    style: "",
    color: "",
    condition: "",
    vendor: "",
  });
  const [noteContent, setNoteContent] = useState("");

  useEffect(() => {
    const fetchMachine = async () => {
      const response = await fetch(`/api/read/machine/${id}`);
      const data = await response.json();

      if (!data.success) {
        toast.error(data.message);
        setMachine(null);
        return;
      }
      setMachine(data.machine);
      setFormData({
        brand: data.machine.brand,
        model: data.machine.model,
        serial: data.machine.serial,
        style: data.machine.style,
        color: data.machine.color,
        condition: data.machine.condition,
        vendor: data.machine.vendor,
      });
    };

    fetchMachine();
  }, [id]);

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

  const handleStatusChange = async (new_status) => {
    if (!confirm(`Change status to ${new_status}?`)) return;
    try {
      const response = await fetch(`/api/update/update/${id}`, {
        method: "PATCH",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status: new_status }),
      });
      const data = await response.json();
      if (!data.success) {
        throw new Error(data.message);
      }
      toast.success(data.message);
      setMachine(data.machine);
    } catch (error) {
      console.error("[ERROR]: ", error);
      toast.error(error.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!confirm("Submit?")) return;
    const URL = editing.machine
      ? `/api/update/update/${id}`
      : `/api/create/add_note`;

    const ADDERS = {
      method: editing.machine ? "PATCH" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        editing.machine ? formData : { note: noteContent, machine_id: id }
      ),
    };

    try {
      const response = await fetch(URL, ADDERS);
      const data = await response.json();
      if (!data.success) {
        throw new Error(data.message);
      }
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

  return (
    <div>
      <div className={styles.cardHeader}>
        <button
          className={
            machine.status !== "completed"
              ? styles.completeMachine
              : styles.printMachine
          }
          onClick={() =>
            handleStatusChange(
              machine.status === "completed" ? "in_progress" : "completed"
            )
          }
          style={{ display: machine.status === "trashed" ? "none" : "flex" }}
        >
          <FontAwesomeIcon
            icon={
              machine.status !== "completed"
                ? faSquareCheck
                : faScrewdriverWrench
            }
          />
        </button>
        <button
          className={styles.editMachine}
          onClick={() =>
            setEditing({ ...editing, machine: !editing.machine, notes: false })
          }
          disabled={machine.status === "trashed"}
        >
          <FontAwesomeIcon
            icon={editing.machine ? faRotateLeft : faPenToSquare}
          />
        </button>
        <button className={styles.printMachine}>
          <FontAwesomeIcon icon={faPrint} />
        </button>
        <button
          className={
            machine.status !== "trashed"
              ? styles.trashMachine
              : styles.recycleMachine
          }
          onClick={() =>
            handleStatusChange(
              machine.status === "trashed" ? "in_progress" : "trashed"
            )
          }
        >
          <FontAwesomeIcon
            icon={machine.status !== "trashed" ? faTrashCan : faRecycle}
          />
        </button>
      </div>

      <form className={styles.machineCardEditForm} onSubmit={handleSubmit}>
        <ul>
          <li>
            {editing.machine ? (
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
            {editing.machine ? (
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
            {editing.machine ? (
              <>
                <label htmlFor="brand">Brand</label>
                <select
                  name="brand"
                  value={formData.brand}
                  onChange={handleChange}
                >
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
            {editing.machine ? (
              <>
                <label htmlFor="style">Style</label>
                <select
                  name="style"
                  value={formData.style}
                  onChange={handleChange}
                >
                  <option value="">--select style--</option>
                  {renderOptions(machineStyles[machine.type_of])}
                </select>
              </>
            ) : (
              <p>
                Style <span>{machine.style}</span>
              </p>
            )}
          </li>
          <li>
            {editing.machine ? (
              <>
                <label htmlFor="color">Color</label>
                <select
                  name="color"
                  value={formData.color}
                  onChange={handleChange}
                >
                  <option value="">--select color--</option>
                  {renderOptions(colors)}
                </select>
              </>
            ) : (
              <p>
                Color <span>{colors[machine.color]}</span>
              </p>
            )}
          </li>
          <li>
            {editing.machine ? (
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
            {editing.machine ? (
              <>
                <label htmlFor="vendor">Vendor</label>
                <select
                  name="vendor"
                  value={formData.vendor}
                  onChange={handleChange}
                >
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
          {editing.machine && <button type="submit">Submit</button>}
        </ul>
      </form>
      <div className={styles.notesBlock}>
        <h3>
          Notes{" "}
          <button
            onClick={() =>
              setEditing({ ...editing, notes: !editing.notes, machine: false })
            }
            type="button"
          >
            <FontAwesomeIcon icon={editing.notes ? faRotateLeft : faPenClip} />
          </button>
        </h3>
        <ul>
          {editing.notes && (
            <li className={styles.addNote}>
              <form onSubmit={handleSubmit}>
                <textarea
                  name="note"
                  value={noteContent}
                  onChange={(e) => setNoteContent(e.target.value)}
                ></textarea>
                <button type="submit">Submit</button>
              </form>
            </li>
          )}
          {machine.notes
            ?.slice()
            .reverse()
            .map(({ id, content, date, author_name }) => (
              <li key={id}>
                <p>{content}</p>
                <div>
                  <p>{author_name}</p>
                  <p>{formatDate(date)}</p>
                </div>
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
};

export default Card;
