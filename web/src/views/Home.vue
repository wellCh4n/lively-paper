<script setup>
import {onMounted, ref} from "vue"
import Chat from "@/components/Chat.vue"
import History from "@/components/History.vue"
import Repository from "@/components/Repository.vue"
import { postData } from '@/utils/request'
import {useRouter} from "vue-router";
import {get} from '@/utils/request'
import {ElMessage} from "element-plus";

const historyRef = ref()
const chatRef = ref()
const router = useRouter()


const clickHistory = (item, isNew) => {
  router.push(`/chat/${item.id}`)
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

onMounted(() => {
  const id = router.currentRoute.value.params.id
  if (id) {
    get(`/chat/history/${id}/find`).then((res) => {
      clickHistory({ id, title: res.Title }, false)
    }).catch((err) => {
      ElMessage('History is not exists~')
    })
  }
})

</script>

<template>
  <div style="display: flex">
    <div>
      <History @click-history="clickHistory"
               @new-chat="newChat"
               style="height: 60vh; background-color: var(--el-color-info-light-9);"
               ref="historyRef"
      />
      <Repository style="height: 40vh; background-color: var(--el-color-info-light-9)"/>
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
