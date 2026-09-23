const adminEntities = ['language', 'category', 'post']

const adminCrudRoutes = adminEntities.flatMap(entity => [
    {
        path: `/admin/${entity}`,
        action: `admin_${entity}@AdminController`,
        name: `admin_${entity}`
    },
    {
        path: `/admin/${entity}/edit/:id`,
        action: `admin_${entity}_edit@AdminController`,
        name: `admin_${entity}_edit`,
        params: { id: /[0-9]*/ }
    },
    {
        path: `/admin/${entity}/delete/:id`,
        action: `admin_${entity}_delete@AdminController`,
        name: `admin_${entity}_delete`,
        params: { id: /[0-9]+/ }
    }
])
export default [
    { path: '/:lang', action: 'home@PagesController', name: 'home', params: { lang: /[a-z]{2}/ } },
    { path: '/', action: 'home@PagesController', name: 'home' },
    { path: '/admin', action: 'admin_home@AdminController', name: 'admin_home' },
    ...adminCrudRoutes
]