<script setup>
import {Plus} from '@element-plus/icons-vue'
import HistoryItem from '@/components/history/HistoryItem.vue'
import {defineExpose, onMounted, ref} from 'vue'
import {get} from '@/utils/request'

const emit = defineEmits(['click-history', 'new-chat'])

const histories = ref([])

const onClickHistory = (item) => {
  emit('click-history', item, false)
}
const addHistory = (item) => {
  histories.value.push(item)
}

onMounted(() => {
  get('/chat/histories').then((res) => {
    histories.value = res.map((item) => {
      return {
        id: item.SessionId,
        title: item.Title
      }
    })
  })
})

defineExpose({
  addHistory
})
</script>

<template>
  <div style="display: flex; flex-direction: column; width: 300px">
    <el-button type="primary"
               :icon="Plus"
               size="large"
               style="width: 300px;"
               @click="emit('new-chat', 'New Chat')"
    >
      New Chat
    </el-button>
    <el-scrollbar style="width: 300px;">
      <HistoryItem @click="onClickHistory(item)"
                   :title="item.title"
                   v-for="item in histories.reverse()"
                   :key="item.id"
                   class="scrollbar-demo-item">
        {{ item.title }}
      </HistoryItem>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.scrollbar-demo-item {
  display: flex;
}
</style>