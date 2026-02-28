<template>
  <main class="chat-page">
    <section class="chat-shell">
      <header class="chat-header">
        <h1>Buscador Inteligente de Propiedades</h1>
        <p>Escribe tu consulta y te respondo como chat.</p>
      </header>

      <section ref="chatBody" class="chat-body">
        <article
          v-for="message in store.messages"
          :key="message.id"
          class="bubble"
          :class="message.role"
        >
          <template v-if="message.role === 'user'">
            <p class="bubble-text">{{ message.text }}</p>
          </template>

          <template v-else>
            <p v-if="message.error" class="error">{{ message.error }}</p>
            <p v-else class="assistant-summary">
              {{ message.count }} resultado(s) encontrado(s).
            </p>

            <div v-if="message.generatedSql" class="sql-box">
              <span>SQL generado</span>
              <pre>{{ message.generatedSql }}</pre>
            </div>

            <div v-if="message.results?.length" class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Titulo</th>
                    <th>Tipo</th>
                    <th>Precio</th>
                    <th>Habitaciones</th>
                    <th>Banos</th>
                    <th>Area m2</th>
                    <th>Ubicacion</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in message.results" :key="item.id">
                    <td>{{ item.titulo }}</td>
                    <td>{{ item.tipo }}</td>
                    <td>{{ formatPrice(item.precio) }}</td>
                    <td>{{ item.habitaciones }}</td>
                    <td>{{ item.banos }}</td>
                    <td>{{ item.area_m2 }}</td>
                    <td>{{ item.ubicacion }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </article>

        <article v-if="store.loading" class="bubble assistant typing">
          Procesando consulta...
        </article>

        <p v-if="!store.messages.length && !store.loading" class="empty-state">
          Aun no hay mensajes. Escribe tu primera consulta.
        </p>
      </section>

      <footer class="composer">
        <form class="composer-form" @submit.prevent="onSubmit">
          <textarea
            v-model="query"
            rows="2"
            placeholder="Ej: casas de 3 habitaciones en zona 10 por menos de 150000"
            :disabled="store.loading"
          />
          <div class="actions">
            <button type="button" class="btn-secondary" @click="store.clearChat()">
              Limpiar chat
            </button>
            <button type="submit" class="btn-primary" :disabled="store.loading || !query.trim()">
              Enviar
            </button>
          </div>
        </form>
      </footer>
    </section>
  </main>
</template>

<script setup>
import { nextTick, ref, watch } from "vue";
import { useSearchStore } from "./stores/searchStore";

const store = useSearchStore();
const query = ref("");
const chatBody = ref(null);

const formatPrice = (value) =>
  new Intl.NumberFormat("es-GT", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(Number(value));

const scrollToBottom = async () => {
  await nextTick();
  if (chatBody.value) {
    chatBody.value.scrollTop = chatBody.value.scrollHeight;
  }
};

const onSubmit = async () => {
  const text = query.value.trim();
  if (!text) return;
  query.value = "";
  await scrollToBottom();
  await store.runSearch(text);
  await scrollToBottom();
};

watch(
  () => [store.messages.length, store.loading],
  async () => {
    await scrollToBottom();
  }
);
</script>
