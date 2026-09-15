import { AppController } from './AppController'


export default class PagesController extends AppController {
    async home(req) {
        return this.render('pages/home')
    }

    async admin_home() {
        return this.render('pages/admin_home')
    }
}