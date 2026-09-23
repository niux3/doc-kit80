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
                addText: 'Ajouter un article',
                endpoint: '/api/v1/posts',
                dependencies: ['language', 'category'],
            }
        }
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

    /*
    * Languages
    */
    async admin_language(req) {
        return this._index(req, 'language')
    }

    async admin_language_edit(req) {
        return this._edit(req, 'language')
    }

    async admin_language_delete(req) {
        return this._destroy(req, 'language')
    }

    /*
    * Categories
    */
    async admin_category(req) {
        return this._index(req, 'category')
    }

    async admin_category_edit(req) {
        return this._edit(req, 'category')
    }

    async admin_category_delete(req) {
        return this._destroy(req, 'category')
    }

    /*
    * Posts
    */
    async admin_post(req) {
        return this._index(req, 'post')
    }

    async admin_post_edit(req) {
        return this._edit(req, 'post')
    }
}