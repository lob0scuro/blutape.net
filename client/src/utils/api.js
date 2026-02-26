export const requestJson = async (url, options = {}) => {
  const {
    method = "GET",
    headers = {},
    body,
    credentials = "include",
    ...rest
  } = options;

  const isFormData = typeof FormData !== "undefined" && body instanceof FormData;
  const finalHeaders = { ...headers };

  let finalBody = body;
  if (body && !isFormData && typeof body !== "string") {
    finalBody = JSON.stringify(body);
    if (!finalHeaders["Content-Type"]) {
      finalHeaders["Content-Type"] = "application/json";
    }
  }

  const response = await fetch(url, {
    method,
    credentials,
    headers: finalHeaders,
    body: finalBody,
    ...rest,
  });

  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const payload = isJson ? await response.json() : null;

  if (!response.ok) {
    throw new Error(payload?.message || `Request failed (${response.status})`);
  }

  if (payload && payload.success === false) {
    throw new Error(payload.message || "Request failed");
  }

  return payload;
};
