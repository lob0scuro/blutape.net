import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPenClip, faRotateLeft } from "@fortawesome/free-solid-svg-icons";
import styles from "./Card.module.css";
import { formatDate } from "../../../utils/Tools";

const MachineNotes = ({
  editing,
  setEditing,
  noteContent,
  setNoteContent,
  handleSubmit,
  notes,
}) => {
  return (
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
        {notes
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
  );
};

export default MachineNotes;
