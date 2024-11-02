import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import loadingDirective from './directives/loading'
import 'animate.css'
const app = createApp(App)
app.directive('loading', loadingDirective)
app.use(createPinia())
app.use(router)

app.mount('#app')
