import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ToolView from '../views/ToolsView.vue'
import ChecklistView from '../views/tools/ChecklistView.vue'
import SousgridView from '../views/tools/SousgridView.vue'
import RessourceinfoView from '@/views/tools/RessourceinfoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/tools',
      name: 'tools',
      component: ToolView,
    },
    {
      path: '/tools/checklist',
      name: 'tools_checklist',
      component: ChecklistView,
    },
    {
      path: '/tools/ressource-info',
      name: 'tools_ressource_info',
      component: RessourceinfoView,
    },
    {
      path: '/tools/sous-grid',
      name: 'tools_sous_grid',
      component: SousgridView,
    },
    {
      path: '/tools/differentiel',
      name: 'tools_differentiel',
      component: ChecklistView,
    },
  ],
})

export default router
