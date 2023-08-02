<script setup>
import { Plus } from '@element-plus/icons-vue'
import HistoryItem from "@/components/history/HistoryItem.vue"
import { ref } from 'vue'

const emit = defineEmits(['click-history', 'new-chat'])

const histories = ref([])

const historyClick = (item) => {
  emit('click-history', item)
}
const addHistory = (id, title) => {
  const item = {
    id: id,
    title: title
  }
  histories.value.push(item)
  historyClick(item)
}

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
               @click="addHistory(new Date().getTime(), 'New Chat')"
    >
      New Chat
    </el-button>
    <el-scrollbar style="width: 300px;">
      <HistoryItem @click="historyClick(item)" :title="item.title" v-for="item in histories" :key="item.id" class="scrollbar-demo-item">{{ item.title }}</HistoryItem>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.scrollbar-demo-item {
  display: flex;
}
</style>