export const renderOptions = (obj) => {
  return Object.entries(obj).map(([k, val]) => (
    <option key={k} value={k}>
      {val}
    </option>
  ));
};

export const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC", // forces UTC interpretation
  });
};

export const dateForDB = (date = new Date()) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
};
