<script setup>
import { ref } from "vue"
import Chat from "@/components/Chat.vue";
import History from "@/components/History.vue";
import Repository from "@/components/Repository.vue"

const record = ref({})
const historyRef = ref()
const clickHistory = (item) => {
  record.value = item
}

const newChat = (prompt) => {
  const id = new Date().getTime()
  historyRef.value.addHistory(id, prompt)
}

</script>

<template>
  <div style="display: flex">
    <History @click-history="clickHistory"
             @new-chat="newChat"
             style="height: 100vh; background-color: #f8f8f8"
             ref="historyRef"
    />
    <Chat @new-chat="newChat"
          :record="record"
          style="height: 100vh"
    />
    <Repository style="height: 100vh; background-color: #f8f8f8"/>
  </div>
</template>

<style scoped>
</style>
