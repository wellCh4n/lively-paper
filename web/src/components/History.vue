<script setup>
import {Plus} from '@element-plus/icons-vue'
import {defineExpose, onMounted, ref} from 'vue'
import {get} from '@/utils/request'
import AreaHeader from "@/components/AreaHeader.vue";

const emit = defineEmits(['click-history', 'new-chat'])

const histories = ref([])
const activeIndex = ref('-1')

const onClickHistory = (item) => {
  activeIndex.value = item.id
  emit('click-history', item, false)
}

const onNewChat = () => {
  emit('new-chat', 'New Chat')
  activeIndex.value = '-1'
}

const addHistory = (item) => {
  histories.value.push(item)
  activeIndex.value = item.id
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
  <div style="display: flex; flex-direction: column; width: 300px; border-radius: var(--el-border-radius-base);">
    <AreaHeader title="Conversion" style="margin-top: 5px" />
    <el-button type="primary"
               :icon="Plus"
               size="large"
               style="margin: 5px 5px"
               @click="onNewChat"
    >
      New Chat
    </el-button>
    <el-scrollbar style="margin: 0 5px 5px 5px">
      <el-menu :default-active="activeIndex"
               ref="menu"
               style="border: none; background-color: var(--el-color-info-light-9)">
        <el-menu-item v-for="item in histories.slice().reverse()"
                      @click="onClickHistory(item)"
                      :index="item.id"
                      :key="item.id"
                      class="history-item">
          {{ item.title.length > 15 ? `${item.title.slice(0, 15)}...` : item.title }}
        </el-menu-item>
      </el-menu>
<!--      <HistoryItem @click="onClickHistory(item)"-->
<!--                   :title="item.title"-->
<!--                   v-for="item in histories.reverse()"-->
<!--                   :key="item.id"-->
<!--                   class="scrollbar-demo-item">-->
<!--        {{ item.title }}-->
<!--      </HistoryItem>-->
    </el-scrollbar>
  </div>
</template>

<style scoped>
.history-item {
  overflow: hidden;
  height: 40px;
  border: solid 1px var(--el-border-color);
  border-radius: var(--el-border-radius-base);
  margin-bottom: 5px;
  background-color: #fff;
}
.history-item:hover {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
.is-active {
  background-color: var(--el-color-primary-light-9);
}
</style>