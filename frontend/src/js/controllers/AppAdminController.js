import { Controller } from '../core/Controller'


export class AppAdminController extends Controller {
    // Registre central des entités gérées
    entities = {}

    // Méthode générique pour l'affichage de la grille (index)
    async _index(req, entityKey) {
        const config = this.entities[entityKey]
        this.setTitle(config.titleIndex)

        // Récupération des colonnes/données dynamiques (ex: via ORM/BDD)
        const fields = config.fields || (config.model ? config.model.__table__.columns.map(col => col.name) : [])
        const data = await this._getData(entityKey)

        const ctx = {
            title: this.getTitle(),
            fields,
            data,
            link_edit_name: config.routeEdit,
            link_delete_name: config.routeDelete,
            link_text: config.addText,
        }
        return this.render('admin/home_gridview', ctx)
    }

    // Méthode générique pour l'édition/création (formulaire)
    async _edit(req, entityKey) {
        const config = this.entities[entityKey]
        const isUpdate = Boolean(req.params?.id)

        this.setTitle(isUpdate ? config.titleEdit : config.titleAdd)

        if (req.method === 'POST') {
            if (isUpdate) {
                await this._update(entityKey, req.params.id, req.body)
            } else {
                await this._create(entityKey, req.body)
            }
            return this.redirect(this.urlFor(config.routeIndex))
        }

        // Chargement du record existant si édition
        const record = isUpdate ? await this._getOne(entityKey, req.params.id) : {}

        const ctx = {
            title: this.getTitle(),
            formtype: config.formtype,
            data: record,
            ...await this._getFormDependencies(entityKey) // Injecte languages, categories, etc.
        }

        return this.render('admin/edit', ctx)
    }

    // Handlers BDD surchargables
    async _getData(entityKey) {
        const config = this.entities[entityKey]

        if (config?.endpoint) {
            try {
                return await this.api.get(config.endpoint)
            } catch (error) {
                console.error(`Erreur lors du chargement des données pour ${entityKey}:`, error)
                return []
            }
        }

        return []
    }

    async _getOne(entityKey, id) {
        const config = this.entities[entityKey]
        if (config?.endpoint) {
            try {
                return await this.api.get(`${config.endpoint}/${id}`)
            } catch (error) {
                console.error(`Erreur lors de la récupération de l'élément ${id} pour ${entityKey} :`, error)
                return {}
            }
        }
        return {}
    }

    async _getFormDependencies(entityKey) { return {} }

    async _create(entityKey, payload) {
        const config = this.entities[entityKey]

        if (config?.endpoint) {
            try {
                // Conversion de FormData en objet JS
                let bodyData = payload
                if (payload instanceof FormData) {
                    bodyData = Object.fromEntries(payload.entries())
                } else if (typeof payload === 'object' && payload !== null && !Array.isArray(payload)) {
                    // Si payload est un objet de type URLSearchParams ou similaire
                    bodyData = { ...payload }
                }
                return await this.api.post(config.endpoint, bodyData)
            } catch (error) {
                console.error(`Erreur lors de la création de l'entité ${entityKey} :`, error)
                throw error
            }
        }
    }

    async _update(entityKey, id, payload) {
        const config = this.entities[entityKey]

        if (config?.endpoint) {
            try {
                // 1. Conversion de FormData en objet JS simple
                let bodyData = payload
                if (payload instanceof FormData) {
                    bodyData = Object.fromEntries(payload.entries())
                } else if (typeof payload === 'object' && payload !== null) {
                    bodyData = { ...payload }
                }

                // 2. Conversion de l'ID en nombre si c'est une chaîne numérique
                const numericId = !isNaN(id) ? Number(id) : id

                // 3. Optionnel : Si l'ID est dans le body et doit être un entier
                if (bodyData.id !== undefined && !isNaN(bodyData.id)) {
                    bodyData.id = Number(bodyData.id)
                }

                return await this.api.put(`${config.endpoint}/${numericId}`, bodyData)
            } catch (error) {
                console.error(`Erreur lors de la mise à jour de l'élément ${id} pour ${entityKey} :`, error)
                throw error
            }
        }
    }

    async _delete(entityKey, id) {
        const config = this.entities[entityKey]

        if (config?.endpoint) {
            try {
                const numericId = !isNaN(id) ? Number(id) : id
                return await this.api.delete(`${config.endpoint}/${numericId}`)
            } catch (error) {
                console.error(`Erreur lors de la suppression de l'élément ${id} pour ${entityKey} :`, error)
                throw error
            }
        }
    }

    // Action appelée par la route de suppression
    async _destroy(req, entityKey) {
        const id = req.params?.id
        if (id) {
            await this._delete(entityKey, id)
        }
        const config = this.entities[entityKey]
        return this.redirect(this.urlFor(config.routeIndex))
    }
}