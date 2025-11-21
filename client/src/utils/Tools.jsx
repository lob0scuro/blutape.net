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
