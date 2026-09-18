import { AppController } from './AppController'


export default class PagesController extends AppController {
    async home(req) {
        return this.render('pages/home')
    }

    async admin_home(req) {
        if (req.method === 'POST') {
            console.log('admin_home > ', req.body)
            console.log('admin_home > POST > ', req.method)
            return this.render('pages/admin_home')
        }
        return this.render('pages/admin_home')
    }
}