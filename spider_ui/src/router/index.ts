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
          component: () => import('../components/scrapyData/selectScrapy.vue'),
        },
        {
          path: 'csdnData',
          name: 'csdnData',
          component: () => import('../components/scrapyData/csdnData.vue'),
        },
      ],
    },
    {
      path: '/dashBoard',
      name: 'dashBoard',
      component: () => import('../views/dashBoard.vue'),
    },
    {
      path: '/scrapyTest',
      name: 'scrapyTest',
      component: () => import('../views/scrapyTest.vue'),
    },

    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import('../views/AboutView.vue'),
    // },
  ],
})

export default router
