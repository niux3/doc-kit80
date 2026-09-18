import EasyMDE from 'easymde'
import cssUrl from 'easymde/dist/easymde.min.css?url'
import { withKit80 } from '../../core/ComponentMixin.js'

export class UiMarkdownEdit extends withKit80(HTMLElement) {
    static formAssociated = true

    #textarea = null
    #easymde = null
    #linkStyle = null
    #internals = null

    constructor() {
        super()
        this.#internals = this.attachInternals()
    }

    static get observedAttributes() {
        return ['value', 'name', 'placeholder', 'required']
    }

    connectedCallback() {
        if (this.#easymde) return

        if (!this.hasAttribute('tabindex')) {
            this.setAttribute('tabindex', '0')
        }

        this.#injectStylesheet()

        this.#textarea = document.createElement('textarea')
        this.#textarea.name = this.getAttribute('name') || ''
        this.#textarea.value = this.getAttribute('value') ?? ''
        this.appendChild(this.#textarea)

        this.#easymde = new EasyMDE({
            element: this.#textarea,
            autofocus: false,
            spellChecker: false,
            status: true,
            placeholder: this.getAttribute('placeholder') || '',
            toolbar: [
                { name: 'bold', action: EasyMDE.toggleBold, className: 'fa fa-bold', title: 'Gras' },
                { name: 'italic', action: EasyMDE.toggleItalic, className: 'fa fa-italic', title: 'Italique' },
                { name: 'heading', action: EasyMDE.toggleHeadingSmaller, className: 'fa fa-header', title: 'Titre' },
                '|',
                { name: 'code', action: EasyMDE.drawCode, className: 'fa fa-code', title: 'Code en ligne' },
                { name: 'code-block', action: EasyMDE.toggleCodeBlock, className: 'fa fa-terminal', title: 'Bloc de code' },
                '|',
                { name: 'quote', action: EasyMDE.toggleBlockquote, className: 'fa fa-quote-left', title: 'Citation' },
                { name: 'unordered-list', action: EasyMDE.toggleUnorderedList, className: 'fa fa-list-ul', title: 'Liste' },
                { name: 'ordered-list', action: EasyMDE.toggleOrderedList, className: 'fa fa-list-ol', title: 'Liste numérotée' },
                '|',
                { name: 'link', action: EasyMDE.drawLink, className: 'fa fa-link', title: 'Lien' },
                { name: 'image', action: EasyMDE.drawImage, className: 'fa fa-picture-o', title: 'Image' },
                '|',
                { name: 'preview', action: EasyMDE.togglePreview, className: 'fa fa-eye no-disable', title: 'Aperçu' },
                { name: 'side-by-side', action: EasyMDE.toggleSideBySide, className: 'fa fa-columns no-disable no-mobile', title: 'Côte à côte' },
                { name: 'fullscreen', action: EasyMDE.toggleFullScreen, className: 'fa fa-arrows-alt no-disable no-mobile', title: 'Plein écran' }
            ]
        })

        this.#easymde.codemirror.on('change', () => {
            this.#handleMarkdownChange()
        })

        // Redirige le focus vers CodeMirror en cas d'erreur de validation à la soumission
        this.addEventListener('invalid', () => {
            this.#easymde?.codemirror?.focus()
        })

        this.#updateFormValue()
    }

    disconnectedCallback() {
        if (this.#easymde) {
            this.#easymde.toTextArea()
            this.#easymde = null
        }

        if (this.#linkStyle && document.querySelectorAll('ui-markdown-edit').length === 0) {
            this.#linkStyle.remove()
            this.#linkStyle = null
        }

        if (this.#textarea) {
            this.#textarea.remove()
            this.#textarea = null
        }
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue === newValue) return

        if (name === 'value') {
            this.value = newValue
        } else if (name === 'required' || name === 'name') {
            this.#updateFormValue()
        }
    }

    get value() {
        return this.#easymde ? this.#easymde.value() : (this.#textarea?.value || '')
    }

    set value(val) {
        const strVal = val ?? ''
        if (this.#easymde && this.#easymde.value() !== strVal) {
            this.#easymde.value(strVal)
        }
        if (this.#textarea) {
            this.#textarea.value = strVal
        }
        this.#updateFormValue()
    }

    // --- Getters et méthodes requis pour l'API Form Associated ---
    get validity() { return this.#internals.validity }
    get validationMessage() { return this.#internals.validationMessage }
    get willValidate() { return this.#internals.willValidate }

    checkValidity() { return this.#internals.checkValidity() }
    reportValidity() { return this.#internals.reportValidity() }

    formResetCallback() {
        this.value = this.getAttribute('value') || ''
    }

    #injectStylesheet() {
        const existingLink = document.querySelector(`link[href="${cssUrl}"]`)
        if (!existingLink) {
            this.#linkStyle = document.createElement('link')
            this.#linkStyle.rel = 'stylesheet'
            this.#linkStyle.href = cssUrl
            document.head.appendChild(this.#linkStyle)
        } else {
            this.#linkStyle = existingLink
        }
    }

    #updateFormValue() {
        const val = this.value

        this.#internals.setFormValue(val)

        if (this.hasAttribute('required') && !val.trim()) {
            // Suppression du 3e argument pour éviter la DOMException
            this.#internals.setValidity(
                { valueMissing: true },
                'Veuillez remplir ce champ.'
            )
        } else {
            this.#internals.setValidity({})
        }
    }

    #handleMarkdownChange() {
        const val = this.value

        if (this.#textarea) {
            this.#textarea.value = val
        }

        this.#updateFormValue()

        this.dispatchEvent(new CustomEvent('ui_markdown_edit:change', {
            bubbles: true,
            composed: true,
            detail: { value: val }
        }))
    }
}