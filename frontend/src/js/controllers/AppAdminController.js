import { Controller } from '../core/Controller'


export class AppAdminController extends Controller {
    // Registre central des entités gérées
    entities = {}

    // Méthode générique pour l'affichage de la grille (index)
    async _index(req, entityKey) {
        const config = this.entities[entityKey]
        console.log('AdminController > _index > ', this.entities)
        this.setTitle(config.titleIndex)

        // Récupération des colonnes/données dynamiques (ex: via ORM/BDD)
        const fields = config.fields || (config.model ? config.model.__table__.columns.map(col => col.name) : [])
        const data = await this._getData(entityKey)

        const ctx = {
            title: this.getTitle(),
            fields,
            data,
            link_edit_name: config.routeEdit,
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

    async _getOne(entityKey, id) { return {} }
    async _getFormDependencies(entityKey) { return {} }

    async _create(entityKey, payload) {
        console.log('Create', entityKey, payload)
    }
    async _update(entityKey, id, payload) { console.log('Update', entityKey, id, payload) }
}