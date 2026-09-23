import { AppAdminController } from "./AppAdminController"


export default class AdminController extends AppAdminController {

    constructor(container) {
        super(container)
        this.categories = [
            { id: 1, name: 'Category 1' },
            { id: 2, name: 'Category 2' },
        ]
        this.languages = [
            { id: 1, name: 'English', abbr: 'en' },
            { id: 2, name: 'French', abbr: 'fr' },
        ]

        // Configuration déclarative du CRUD
        this.entities = {
            language: {
                titleIndex: 'Languages',
                titleAdd: 'Ajouter une langue',
                titleEdit: 'Éditer une langue',
                formtype: 'form_languages',
                routeIndex: 'admin_language',
                routeEdit: 'admin_language_edit',
                routeDelete: 'admin_language_delete',
                addText: 'Ajouter une langue',
                fields: ['id', 'name', 'abbr'],
                endpoint: '/api/v1/languages',
            },
            category: {
                titleIndex: 'Catégories',
                titleAdd: 'Ajouter une catégorie',
                titleEdit: 'Éditer une catégorie',
                formtype: 'form_categories',
                routeIndex: 'admin_category',
                routeEdit: 'admin_category_edit',
                addText: 'Ajouter une catégorie',
            },
            post: {
                titleIndex: 'Articles',
                titleAdd: 'Ajouter un article',
                titleEdit: 'Éditer un article',
                formtype: 'form_posts',
                routeIndex: 'admin_post',
                routeEdit: 'admin_post_edit',
                addText: 'Ajouter un article',
            }
        }
    }

    // Injection des dépendances pour les formulaires (selects, etc.)
    async _getFormDependencies(entityKey) {
        if (entityKey === 'category' || entityKey === 'post') {
            return {
                languages: this.languages,
                categories: this.categories,
            }
        }
        return {}
    }


    async admin_home(req) {
        let ctx = {}
        try {
            ctx = {
                data: await this.api.get('/api/health')
            }
            console.log('AdminController > admin_home > ', ctx.data)
        } catch (error) {
            ctx = {
                data: { status: 'unhealthy', error: error.message }
            }
        }
        return this.render('admin/admin_home', ctx)
    }

    async admin_language(req) {
        return this._index(req, 'language')
    }

    async admin_language_edit(req) {
        return this._edit(req, 'language')
    }

    async admin_language_delete(req) {
        return this._destroy(req, 'language')
    }

    async admin_category(req) {
        return this._index(req, 'category')
    }

    async admin_category_edit(req) {
        return this._edit(req, 'category')
    }

    async admin_post(req) {
        return this._index(req, 'post')
    }

    async admin_post_edit(req) {
        return this._edit(req, 'post')
    }
}