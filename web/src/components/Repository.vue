<script setup>
import { Upload } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { genFileId } from 'element-plus'
import AreaHeader from "@/components/AreaHeader.vue";

const uploader = ref()
const upload = (file) => {
  console.log(file.file)
  const data = new FormData()
  data.append('file', file.file)
  return new Promise((resolve, reject) => {
    fetch('http://127.0.0.1:8000/file', {
      method: 'POST',
      body: data
    }).then((res) => {
      resolve()
    })
  })
}

const cancel = (files) => {
  uploader.value.clearFiles()
  const file = files[0]
  file.uid = genFileId()
  uploader.value.handleStart(file)
}

</script>

<template>
  <div style="width: 300px; border-radius: var(--el-border-radius-base)">
    <AreaHeader title="Repository" />
    <el-upload style="width: 100%; display: inline-grid;"
               :http-request="upload"
               :multiple="false"
               :on-exceed="cancel"
               :limit="1"
               ref="uploader"
               class="uploader">
      <el-button type="primary"
                 style="width: 100%; margin: 5px 5px"
                 size="large"
                 :icon="Upload">
        Click to upload file
      </el-button>
    </el-upload>
  </div>
</template>

<style scoped>
</style>