import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import 'element-plus/theme-chalk/el-message-box.css'

const app = createApp(App)

app.use(router)
app.use(ElMessage)

app.mount('#app')
