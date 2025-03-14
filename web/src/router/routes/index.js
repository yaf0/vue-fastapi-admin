import i18n from '~/i18n'
const { t } = i18n.global

const Layout = () => import('@/layout/index.vue')

export const basicRoutes = [
  {
    path: '/',
    redirect: '/workbench', // 默认跳转到首页
    meta: { order: 0 },
  },
  {
    name: t('views.workbench.label_workbench'),
    path: '/workbench',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/workbench/index.vue'),
        name: `${t('views.workbench.label_workbench')}Default`,
        meta: {
          title: t('views.workbench.label_workbench'),
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
    meta: { order: 1 },
  },
  {
    name: t('views.profile.label_profile'),
    path: '/profile',
    component: Layout,
    isHidden: true,
    children: [
      {
        path: '',
        component: () => import('@/views/profile/index.vue'),
        name: `${t('views.profile.label_profile')}Default`,
        meta: {
          title: t('views.profile.label_profile'),
          icon: 'user',
          affix: true,
        },
      },
    ],
    meta: { order: 99 },
  },
  {
    name: 'ErrorPage',
    path: '/error-page',
    isHidden: true,
    component: Layout,
    redirect: '/error-page/404',
    meta: {
      title: t('views.errors.label_error'),
      icon: 'mdi:alert-circle-outline',
      order: 99,
    },
    children: [
      {
        name: 'ERROR-401',
        path: '401',
        component: () => import('@/views/error-page/401.vue'),
        meta: {
          title: '401',
          icon: 'material-symbols:authenticator',
        },
      },
      {
        name: 'ERROR-403',
        path: '403',
        component: () => import('@/views/error-page/403.vue'),
        meta: {
          title: '403',
          icon: 'solar:forbidden-circle-line-duotone',
        },
      },
      {
        name: 'ERROR-404',
        path: '404',
        component: () => import('@/views/error-page/404.vue'),
        meta: {
          title: '404',
          icon: 'tabler:error-404',
        },
      },
      {
        name: 'ERROR-500',
        path: '500',
        component: () => import('@/views/error-page/500.vue'),
        meta: {
          title: '500',
          icon: 'clarity:rack-server-outline-alerted',
        },
      },
    ],
  },
  {
    name: '403',
    path: '/403',
    component: () => import('@/views/error-page/403.vue'),
    isHidden: true,
  },
  {
    name: '404',
    path: '/404',
    component: () => import('@/views/error-page/404.vue'),
    isHidden: true,
  },
  {
    name: 'Login',
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    isHidden: true,
    meta: {
      title: '登录页',
    },
  },
  {
    path: '/business/total',
    name: 'TotalManagement',
    meta: { title: '总表数据'},
    isHidden: false,
    component: Layout,
    children: [
      {
        path: 'total',
        component: () => import('@/views/business/total/index.vue'),
        name: `totaldata`,
        meta: {
          title: '总表数据',
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
  },
  {
    path: '/business/own_business',
    name: 'own_business',
    meta: { title: '我的数据'},
    isHidden: false,
    component: Layout,
    children: [
      {
        path: 'total',
        component: () => import('@/views/business/own_business/index.vue'),
        name: `owndata`,
        meta: {
          title: '我的数据',
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
  },
  {
    path: '/business/yyfs',
    name: 'YY外勤',
    meta: { title: 'YY外勤'},
    isHidden: false,
    component: Layout,
    children: [
      {
        path: 'yyfs',
        component: () => import('@/views/business/yyfs/index.vue'),
        name: `yyfsdata`,
        meta: {
          title: 'YY外勤',
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
  },
  {
    path: '/business/field_work',
    name: 'FieldWorkManagement',
    meta: { title: '外勤人员'},
    component: Layout,
    isHidden: true,
    children: [
      {
        path: '',
        component: () => import('@/views/business/field_work/index.vue'),
        name: `field_work_data`,
        meta: {
          title: '外勤人员',
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
  },
  {
    path: '/business/duty_staff',
    name: 'DutyStaffManagement',
    meta: { title: '勤务管理'},
    component: Layout,
    isHidden: false,
    children: [
      {
        path: '',
        component: () => import('@/views/business/duty_staff/index.vue'),
        name: `duty_staff_data`,
        meta: {
          title: '勤务管理',
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
  },
  {
    path: '/business/manage_business',
    name: 'ManageBusinessStatics',
    meta: { title: '业务统计'},
    component: Layout,
    isHidden: false,
    children: [
      {
        path: '',
        component: () => import('@/views/business/manage_business/index.vue'),
        name: `business`,
        meta: {
          title: '业务统计',
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
  },
  {
    name: 'curd',
    path: '/curd',
    isHidden: true,
    meta: {
      title: 'CURD示例',
    },
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/curd/index.vue'),
        name: `test`,
        meta: {
          title: 'CURD示例',
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
  },
]

export const NOT_FOUND_ROUTE = {
  name: 'NotFound',
  path: '/:pathMatch(.*)*',
  redirect: '/404',
  isHidden: true,
}

export const EMPTY_ROUTE = {
  name: 'Empty',
  path: '/:pathMatch(.*)*',
  component: null,
}

const modules = import.meta.glob('@/views/**/route.js', { eager: true })
const asyncRoutes = []
Object.keys(modules).forEach((key) => {
  asyncRoutes.push(modules[key].default)
})

// 加载 views 下每个模块的 index.vue 文件
const vueModules = import.meta.glob('@/views/**/index.vue')

export { asyncRoutes, vueModules }
