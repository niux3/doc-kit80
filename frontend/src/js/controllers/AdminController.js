import { AppAdminController } from "./AppAdminController"


export default class AdminController extends AppAdminController {

    constructor(container) {
        super(container)

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
                dependencies: [],
            },
            category: {
                titleIndex: 'Catégories',
                titleAdd: 'Ajouter une catégorie',
                titleEdit: 'Éditer une catégorie',
                formtype: 'form_categories',
                routeIndex: 'admin_category',
                routeEdit: 'admin_category_edit',
                routeDelete: 'admin_category_delete',
                addText: 'Ajouter une catégorie',
                fields: ['id', 'name'],
                endpoint: '/api/v1/categories',
                dependencies: ['language', 'category'],
            },
            post: {
                titleIndex: 'Articles',
                titleAdd: 'Ajouter un article',
                titleEdit: 'Éditer un article',
                formtype: 'form_posts',
                routeIndex: 'admin_post',
                routeEdit: 'admin_post_edit',
                routeDelete: 'admin_post_delete',
                addText: 'Ajouter un article',
                fields: ['id', 'title', 'language_id', 'category_id'],
                endpoint: '/api/v1/posts',
                dependencies: ['language', 'category'],
            }
        }

        this.#registerCrudMethods()
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

    #registerCrudMethods() {
        for (const entity of Object.keys(this.entities)) {
            this[`admin_${entity}`] = async (req) => this._index(req, entity)
            this[`admin_${entity}_edit`] = async (req) => this._edit(req, entity)
            this[`admin_${entity}_delete`] = async (req) => this._destroy(req, entity)
        }
    }
}