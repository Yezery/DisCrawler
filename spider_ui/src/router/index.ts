import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '/',
      redirect: '/home/datas',
    },
    {
      path: '/home',
      name: 'home',
      redirect: '/home/datas',
      component: HomeView,
      children: [
        {
          path: 'datas',
          name: 'datas',
          component: () => import('../components/scrapyData/SelectScrapy.vue'),
        },
        {
          path: 'csdnData',
          name: 'csdnData',
          component: () => import('../components/scrapyData/CsdnData.vue'),
        },
        {
          path: 'bossData',
          name: 'bossData',
          component: () => import('../components/scrapyData/BossData.vue'),
        },
      ],
    },
    {
      path: '/dashBoard',
      name: 'dashBoard',
      component: () => import('../views/DashBoard.vue'),
    },
    {
      path: '/application',
      name: 'application',
      component: () => import('../views/ApplicationView.vue'),
    },

    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import('../views/AboutView.vue'),
    // },
  ],
})

export default router
