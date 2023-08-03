<script setup>
import {onMounted, ref} from "vue"
import Chat from "@/components/Chat.vue"
import History from "@/components/History.vue"
import Repository from "@/components/Repository.vue"
import { postData } from '@/utils/request'

const historyRef = ref()
const chatRef = ref()
const clickHistory = (item) => {
  chatRef.value.onHistorySwitch(item)
}

const newChat = (title) => {
  const id = crypto.randomUUID()
  const item = {
    id: id,
    title: title
  }
  clickHistory(item)
}

const addChat = (item) => {
  postData('/chat/new', item).then((res) => {
    historyRef.value.addHistory(item)
  })
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
          @add-chat="addChat"
          style="height: 100vh"
          ref="chatRef"
    />
<!--    <Repository style="height: 100vh; background-color: #f8f8f8"/>-->
  </div>
</template>

<style scoped>
</style>
