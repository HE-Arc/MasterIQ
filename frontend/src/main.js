import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const API_SERVER = import.meta.env.VITE_API_SERVER;
axios.defaults.baseURL = API_SERVER;
axios.defaults.withCredentials = true;

const app = createApp(App)

app.use(router)

app.mount('#app')
