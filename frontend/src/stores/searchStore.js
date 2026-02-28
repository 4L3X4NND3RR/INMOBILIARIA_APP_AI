import { defineStore } from "pinia";
import { searchProperties } from "../services/searchService";

export const useSearchStore = defineStore("search", {
  state: () => ({
    loading: false,
    messages: []
  }),
  actions: {
    async runSearch(query) {
      const normalizedQuery = (query || "").trim();
      if (!normalizedQuery) return;

      this.loading = true;
      this.messages.push({
        id: crypto.randomUUID(),
        role: "user",
        text: normalizedQuery
      });

      try {
        const data = await searchProperties(normalizedQuery);
        const sql = data.sql_query || data.generated_sql || "";
        this.messages.push({
          id: crypto.randomUUID(),
          role: "assistant",
          generatedSql: sql,
          results: data.results || [],
          count: data.count || 0
        });
      } catch (error) {
        this.messages.push({
          id: crypto.randomUUID(),
          role: "assistant",
          generatedSql: "",
          results: [],
          count: 0,
          error:
            error?.response?.data?.detail ||
            "No fue posible ejecutar la busqueda. Verifica el endpoint /api/search."
        });
      } finally {
        this.loading = false;
      }
    },
    clearChat() {
      this.loading = false;
      this.messages = [];
    }
  }
});
