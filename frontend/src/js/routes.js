export default [
    { path: '/:lang', action: 'home@PagesController', name: 'home', params: { lang: /[a-z]{2}/ } },
    { path: '/', action: 'home@PagesController', name: 'home' },
    { path: '/admin', action: 'admin_home@AdminController', name: 'admin_home' },
    { path: '/admin/language', action: 'admin_language@AdminController', name: 'admin_language' },
    { path: '/admin/category', action: 'admin_category@AdminController', name: 'admin_category' },
    { path: '/admin/post', action: 'admin_post@AdminController', name: 'admin_post' },
]