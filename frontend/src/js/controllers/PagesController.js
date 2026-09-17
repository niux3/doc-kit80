import { AppController } from './AppController'


export default class PagesController extends AppController {
    async home(req) {
        return this.render('pages/home')
    }

    async admin_home(req) {
        if (req.method === 'POST') {
            console.log('admin_home > POST > ', req)
            console.log('admin_home > CONTENT > ', req.body.get('content'))
            return this.render('pages/admin_home')
        }
        return this.render('pages/admin_home')
    }
}