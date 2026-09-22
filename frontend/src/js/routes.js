export default [
    { path: '/:lang', action: 'home@PagesController', name: 'home', params: { lang: /[a-z]{2}/ } },
    { path: '/', action: 'home@PagesController', name: 'home' },
    { path: '/admin', action: 'admin_home@AdminController', name: 'admin_home' },

    { path: '/admin/language', action: 'admin_language@AdminController', name: 'admin_language' },
    { path: '/admin/language/add', action: 'admin_language_add@AdminController', name: 'admin_language_add' },

    { path: '/admin/category', action: 'admin_category@AdminController', name: 'admin_category' },
    { path: '/admin/category/add', action: 'admin_category_add@AdminController', name: 'admin_category_add' },

    { path: '/admin/post', action: 'admin_post@AdminController', name: 'admin_post' },
    { path: '/admin/post/add', action: 'admin_post_add@AdminController', name: 'admin_post_add' },
]