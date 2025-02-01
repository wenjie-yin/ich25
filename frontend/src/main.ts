import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { VBtn, VTextField, VForm, VContainer, VRow, VCol, VCard, VCardTitle, VCardText, VCardActions, VTextarea, VIcon, VApp, VMain, VAppBar } from 'vuetify/components'
import { mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
    components: {
        VBtn,
        VTextField,
        VForm,
        VContainer,
        VRow,
        VCol,
        VCard,
        VCardTitle,
        VCardText,
        VCardActions,
        VTextarea,
        VIcon,
        VApp,
        VMain,
        VAppBar
    },
    directives,
    icons: {
        defaultSet: 'mdi',
        sets: {
            mdi,
        },
    },
    theme: {
        themes: {
            light: {
                colors: {
                    primary: '#10a37f',
                    secondary: '#0e906f',
                },
            },
        },
    },
})

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app')
