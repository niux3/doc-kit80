export default [
    { path: '/:lang', action: 'home@PagesController', name: 'home', params: { lang: /[a-z]{2}/ } },
    { path: '/', action: 'home@PagesController', name: 'home' },
    { path: '/admin', action: 'admin_home@AdminController', name: 'admin_home' },

    { path: '/admin/language', action: 'admin_language@AdminController', name: 'admin_language' },
    { path: '/admin/language/edit/:id', action: 'admin_language_edit@AdminController', name: 'admin_language_edit', params: { id: /[0-9]*/ } },

    { path: '/admin/category', action: 'admin_category@AdminController', name: 'admin_category' },
    { path: '/admin/category/edit/:id', action: 'admin_category_edit@AdminController', name: 'admin_category_edit', params: { id: /[0-9]*/ } },

    { path: '/admin/post', action: 'admin_post@AdminController', name: 'admin_post' },
    { path: '/admin/post/edit/:id', action: 'admin_post_edit@AdminController', name: 'admin_post_edit', params: { id: /[0-9]*/ } },
]