<script setup>
import { Plus } from '@element-plus/icons-vue'
import HistoryItem from "@/components/history/HistoryItem.vue"
import { ref, defineExpose } from 'vue'

const emit = defineEmits(['click-history', 'new-chat'])

const histories = ref([])

const onClickHistory = (item) => {
  emit('click-history', item)
}
const addHistory = (item) => {
  histories.value.push(item)
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
               @click="emit('new-chat', 'New Chat')"
    >
      New Chat
    </el-button>
    <el-scrollbar style="width: 300px;">
      <HistoryItem @click="onClickHistory(item)" :title="item.title" v-for="item in histories" :key="item.id" class="scrollbar-demo-item">{{ item.title }}</HistoryItem>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.scrollbar-demo-item {
  display: flex;
}
</style>