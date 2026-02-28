import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8010",
  timeout: 30000
});

export async function searchProperties(query) {
  const { data } = await api.post("/api/search", { query });
  return data;
}
