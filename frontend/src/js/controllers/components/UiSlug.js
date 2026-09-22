export class UiSlug extends HTMLElement {
    #textarea = null
    #input = null
    #relation = null
    #onRelationInput = null

    static #slugify(str) {
        if (!str) return ''
        return str
            .toString()
            .normalize('NFD')                   // Sépare les caractères de leurs diacritiques (accents)
            // .replace(/[\u0300-\u03f]/g, '')     // Supprime les accents
            .toLowerCase()
            .trim()
            .replace(/[^a-z0-9 -]/g, '')        // Supprime les caractères spéciaux non autorisés
            .replace(/\s+/g, '-')               // Remplace les espaces par des tirets
            .replace(/-+/g, '-')                // Évite les tirets consécutifs
            .replace(/^-+|-+$/g, '')            // Supprime les tirets au début et à la fin
    }

    connectedCallback() {
        const relationId = this.getAttribute('relation')
        if (relationId) {
            this.#relation = document.getElementById(relationId)
        }

        this.#input = document.createElement('input')
        this.#input.type = 'text'

        if (this.getAttribute('className')) {
            this.#input.className = this.getAttribute('className')
        }

        if (this.hasAttribute('id')) {
            this.#input.id = this.getAttribute('id')
            this.removeAttribute('id') // Évite les conflits d'ID entre le Custom Element et l'input
        }

        if (this.hasAttribute('name')) {
            this.#input.name = this.getAttribute('name')
        }

        if (this.hasAttribute('readonly')) {
            this.#input.readOnly = true
        }

        if (this.hasAttribute('disabled')) {
            this.#input.disabled = true
        }

        if (this.hasAttribute('required')) {
            this.#input.required = true
        }

        const initialVal = this.getAttribute('value') || ''
        this.#input.value = UiSlug.#slugify(initialVal)

        this.appendChild(this.#input)
        this.#bindRelation()
    }

    disconnectedCallback() {
        if (this.#relation && this.#onRelationInput) {
            this.#relation.removeEventListener('input', this.#onRelationInput)
            this.#onRelationInput = null
        }
    }

    #bindRelation() {
        if (!this.#relation) return

        // Référence nommée pour pouvoir faire le removeEventListener proprement
        this.#onRelationInput = (e) => {
            const rawValue = e.target.value ?? ''
            this.#input.value = UiSlug.#slugify(rawValue)
        }

        this.#relation.addEventListener('input', this.#onRelationInput)

        // Si l'élément cible a déjà une valeur au chargement, on slugify immédiatement
        if (this.#relation.value && !this.#input.value) {
            this.#input.value = UiSlug.#slugify(this.#relation.value)
        }
    }

    get value() {
        return this.#input ? this.#input.value : ''
    }

    set value(val) {
        if (this.#input) {
            this.#input.value = UiSlug.#slugify(val)
        }
    }
}