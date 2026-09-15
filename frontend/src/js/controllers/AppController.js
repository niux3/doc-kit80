import { Controller } from '../core/Controller'
import { marked } from 'marked'


export class AppController extends Controller {
    init() {
        const unsubscribe = this.subscribeAll((fullState, key, oldValue) => {
            // console.log(`${key} changed: ${oldValue} → ${fullState[key]}`)
            if (key === 'theme') {
                document.documentElement.dataset.theme = fullState[key]
                localStorage.setItem('theme', fullState[key])
            }
        })
        this.helperMarkdown()
    }

    async afterLoad(ctx) {
        const saved = localStorage.getItem('theme')
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        const theme = saved || (systemDark ? 'dark' : 'light')
        this.setCtx('theme', theme)

        window.addEventListener('ui_selector:select', e => {
            if (e.detail?.value) {
                this.#setCurrentLanguage(e.detail.value)
            }
        })

        window.addEventListener('ui_toggle:change', e => {
            const theme = e.detail.checked ? 'dark' : 'light'
            this.setCtx('theme', theme)
        })
    }

    async beforeRender(ctx) {
        const lang = this.#setCurrentLanguage(
            ctx?.params?.lang || localStorage.getItem('lang') || 'en'
        )

        this.setMultipleCtx({
            'currentPath': window.location.pathname,
            'languages': ['fr', 'en'],
            'currentLanguage': lang,
            'currentRouteName': ctx?.route?.route?.name,
            'menu': {
                "fr": {
                    "home": "Accueil",
                    "about": "À propos"
                },
                "en": {
                    "home": "Home",
                    "about": "About"
                }
            },
            'theme': localStorage.getItem('theme') || 'dark'
        })
    }

    async afterRender(ctx) {
        // ...
    }

    #setCurrentLanguage(lang) {
        localStorage.setItem('lang', lang)
        document.documentElement.setAttribute('lang', lang)
        return lang
    }

    helperMarkdown() {
        const engine = this.container.get('templateEngine')
        if (engine && typeof engine.helper === 'function') {
            engine.helper('markdown', (content) => {
                if (!content) return ''
                return marked.parse(content)
            })
        }
    }
}