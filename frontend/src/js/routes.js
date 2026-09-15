export default [
    { path: '/:lang', action: 'home@PagesController', name: 'home', params: { lang: /[a-z]{2}/ } },
    { path: '/', action: 'home@PagesController', name: 'home' },
    { path: '/admin', action: 'admin_home@PagesController', name: 'admin_home' },
]