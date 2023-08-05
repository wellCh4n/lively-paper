<script setup>
import {Plus} from '@element-plus/icons-vue'
import {defineExpose, onMounted, ref} from 'vue'
import {get} from '@/utils/request'

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
  <div style="display: flex; flex-direction: column; width: 300px">
    <el-button type="primary"
               :icon="Plus"
               size="large"
               style="width: 300px;"
               @click="onNewChat"
    >
      New Chat
    </el-button>
    <el-scrollbar style="width: 300px;">
      <el-menu :default-active="activeIndex" ref="menu">
        <el-menu-item v-for="item in histories"
                      @click="onClickHistory(item)"
                      :index="item.id"
                      :key="item.id">
          {{ item.title }} - {{ item.id }}
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
.scrollbar-demo-item {
  display: flex;
}
</style>