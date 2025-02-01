import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import TDesign from 'tdesign-vue-next';
import router from './router'

import 'tdesign-vue-next/es/style/index.css';

createApp(App).use(router).use(TDesign).mount('#app')
