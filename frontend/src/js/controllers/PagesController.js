import { AppController } from './AppController'


export default class PagesController extends AppController {
    async home(req) {
        return this.render('pages/home')
    }
}