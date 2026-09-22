import { AppAdminController } from "./AppAdminController"


export default class AdminController extends AppAdminController {

    init() {
        this.categories = [
            { id: 1, name: 'Category 1' },
            { id: 2, name: 'Category 2' },
            { id: 3, name: 'Category 3' },
            { id: 4, name: 'Category 4' },
            { id: 5, name: 'Category 5' },
        ]
        this.languages = [
            { id: 1, name: 'English' },
            { id: 2, name: 'French' },
        ]
    }

    async admin_home(req) {
        if (req.method === 'POST') {
            console.log('AdminController > admin_home > ', req.body)
            console.log('AdminController >admin_home > POST > ', req.method)
            return this.render('admin/admin_home')
        }
        return this.render('admin/admin_home')
    }

    async admin_language(req) {
        this.setTitle('languages')
        const ctx = {
            title: this.getTitle(),
            fields: ['id', 'name', 'abbr'],
            data: [
                { id: 1, name: 'English', abbr: 'en' },
                { id: 2, name: 'French', abbr: 'fr' },
            ],
            link_add_name: 'admin_language_add',
            link_text: "Ajouter une langue",
        }
        return this.render('admin/home_gridview', ctx)
    }

    async admin_language_add(req) {
        this.setTitle("Éditer une langue")
        const ctx = {
            title: this.getTitle(),
            formtype: 'form_languages',
        }
        if (req.method === 'POST') {
            console.log('AdminController > admin_language_add > ', req.body)
            console.log('AdminController >admin_language_add > POST > ', req.method)
            return this.redirect(this.urlFor('admin_language'))
        }
        return this.render('admin/edit', ctx)
    }

    async admin_category(req) {
        this.setTitle('categories')
        const ctx = {
            title: this.getTitle(),
            fields: [],
            data: [],
            link_add_name: 'admin_category_add',
            link_text: "Ajouter une catégorie",
        }
        return this.render('admin/home_gridview', ctx)
    }

    async admin_category_add(req) {
        this.setTitle("Éditer une catégorie")
        const ctx = {
            title: this.getTitle(),
            formtype: 'form_categories',
            languages: this.languages,
            categories: this.categories,
        }
        if (req.method === 'POST') {
            console.log('AdminController > admin_category_add > ', req.body)
            console.log('AdminController >admin_category_add > POST > ', req.method)
            return this.redirect(this.urlFor('admin_category'))
        }
        return this.render('admin/edit', ctx)
    }

    async admin_post(req) {
        this.setTitle('articles')
        const ctx = {
            title: this.getTitle(),
            fields: [],
            data: [],
            link_add_name: 'admin_post_add',
            link_text: "Ajouter un article",
        }
        return this.render('admin/home_gridview', ctx)
    }

    async admin_post_add(req) {
        this.setTitle("Éditer un article")
        const ctx = {
            title: this.getTitle(),
            formtype: 'form_posts',
            languages: this.languages,
            categories: this.categories,
        }
        if (req.method === 'POST') {
            console.log('AdminController > admin_post_add > ', req.body)
            console.log('AdminController >admin_post_add > POST > ', req.method)
            return this.redirect(this.urlFor('admin_post'))
        }
        return this.render('admin/edit', ctx)

    }
}