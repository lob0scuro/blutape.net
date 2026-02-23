import styles from "./Navbar.module.css";
import { useNavigate, useLocation } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faChartSimple,
  faHouse,
  faList,
  faMagnifyingGlass,
} from "@fortawesome/free-solid-svg-icons";

const Navbar = () => {
  const navi = useNavigate();
  const loc = useLocation();

  const goTo = (path) => {
    navi(path);
  };

  const PATHS = {
    "/": faHouse,
    "/search": faMagnifyingGlass,
    "/machines": faList,
    "/admin/metrics": faChartSimple,
  };

  return (
    <div className={styles.navbar}>
      {Object.entries(PATHS).map(([path, icon], index) => (
        <button
          key={index}
          onClick={() => goTo(path)}
          className={loc.pathname === path ? styles.active : ""}
        >
          <FontAwesomeIcon icon={icon} />
        </button>
      ))}
    </div>
  );
};

export default Navbar;
