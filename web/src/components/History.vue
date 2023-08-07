<script setup>
import {Plus, Delete, WarningFilled} from '@element-plus/icons-vue'
import {defineExpose, onMounted, ref} from 'vue'
import {get} from '@/utils/request'
import AreaHeader from '@/components/AreaHeader.vue'
import {useRouter} from 'vue-router'

const emit = defineEmits(['click-history', 'new-chat'])

const histories = ref([])
const activeIndex = ref('-1')

const router = useRouter()

const onClickHistory = (item) => {
  activeIndex.value = item.id
  router.push(`/chat/${item.id}`)
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

const deleteHistory = (item) => {
  get(`/chat/history/${item.id}/delete`).then((res) => {
    histories.value = histories.value.filter((history) => history.id !== item.id)
  })
}

onMounted(() => {
  const id = router.currentRoute.value.params.id
  if (id) {
    activeIndex.value = id
  }
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
                      @click="onClickHistory(item);"
                      :index="item.id"
                      :key="item.id"
                      class="history-item">
          <template #title>
            {{ item.title.length > 15 ? `${item.title.slice(0, 15)}...` : item.title }}
            <el-popconfirm :title="`Delete conversation?`"
                           @confirm="deleteHistory(item)"
                           width="200px"
                           :hide-after="0"
                           confirm-button-text="Delete"
                           :icon="WarningFilled"
                           icon-color="#F56C6C"
                           cancel-button-text="Cancel"
                           confirm-button-type="danger"
            >
              <template #reference>
                <el-link :underline="false"
                         style="position: absolute; right: 0;"
                         @click.native.stop
                >
                  <el-icon class="delete-btn"><Delete /></el-icon>
                </el-link>
              </template>
            </el-popconfirm>
          </template>
        </el-menu-item>
      </el-menu>
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