<script setup>
import {defineProps, defineEmits} from 'vue'
import {Delete} from '@element-plus/icons-vue'

const emit = defineEmits(['remove'])

const props = defineProps({
  func: {
    type: Object,
    required: true
  },
  that: {
    type: Object,
    required: true
  }
})

const ready = (event) => {
  props.func.ready(props.that, props.func.params, event)
}

</script>

<template>
  <el-popover placement="top-start"
              trigger="hover"
              :width="200"
  >
    <template #reference>
      <el-button-group style="margin-right: 12px;">
        <el-button size="small" style="margin-left: 0" @click="ready">
          {{ props.func.name }}
        </el-button>
        <el-button size="small" type="primary" @click="emit('remove')">
          <el-icon><Delete /></el-icon>
        </el-button>
      </el-button-group>
    </template>
    <template #default>
      {{ props.func.params }}
    </template>

  </el-popover>
</template>

<style scoped>

</style>