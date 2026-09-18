import { AppAdminController } from "./AppAdminController"


export default class AdminController extends AppAdminController {

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
            link_add_name: 'admin_language',
        }
        return this.render('admin/home_gridview', ctx)
    }

    async admin_category(req) {
        this.setTitle('categories')
        const ctx = {
            title: this.getTitle(),
            fields: [],
            data: [],
            link_add_name: 'admin_language',
        }
        return this.render('admin/home_gridview', ctx)
    }

    async admin_post(req) {
        this.setTitle('articles')
        const ctx = {
            title: this.getTitle(),
            fields: [],
            data: [],
            link_add_name: 'admin_language',
        }
        return this.render('admin/home_gridview', ctx)
    }
}