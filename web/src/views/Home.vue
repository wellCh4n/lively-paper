<script setup>
import {onMounted, ref} from "vue"
import Chat from "@/components/Chat.vue"
import History from "@/components/History.vue"
import Repository from "@/components/Repository.vue"
import { postData } from '@/utils/request'
import {useRoute} from "vue-router";

const historyRef = ref()
const chatRef = ref()
const clickHistory = (item, isNew) => {
  chatRef.value.onHistorySwitch(item, isNew)
}

const newChat = (title) => {
  const id = crypto.randomUUID()
  const item = {
    id: id,
    title: title
  }
  clickHistory(item, true)
}

const addChat = (item) => {
  postData('/chat/new', item).then((res) => {
    historyRef.value.addHistory(item)
  })
}

</script>

<template>
  <div style="display: flex">
    <div>
      <History @click-history="clickHistory"
               @new-chat="newChat"
               style="height: 50vh; background-color: var(--el-color-info-light-9);"
               ref="historyRef"
      />
      <Repository style="height: 50vh; background-color: var(--el-color-info-light-9)"/>
    </div>
    <Chat @new-chat="newChat"
          @add-chat="addChat"
          style="height: 100vh;"
          ref="chatRef"
    />

  </div>
</template>

<style scoped>
</style>
