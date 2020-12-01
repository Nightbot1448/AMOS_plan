import Vue from 'vue';
import Router from 'vue-router';
import Preparation from '@/components/Preparation';
import Task from '@/components/Task';
import PlanningArea from '@/components/PlanningArea';
import Planning from '@/components/Planning';
import Conduct from '@/components/Conduct';
import Processing from '@/components/Processing';
import Experiment from '@/components/Experiment';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/preparation',
      name: 'Preparation',
      component: Preparation,
    },
    {
      path: '/task',
      name: 'Task',
      component: Task,
    },
    {
      path: '/planning_area',
      name: 'Planning Area',
      component: PlanningArea,
    },
    {
      path: '/planning',
      name: 'Planning',
      component: Planning,
    },
    {
      path: '/conduct',
      name: 'Conduct',
      component: Conduct,
    },
    {
      path: '/processing',
      name: 'Processing',
      component: Processing,
    },
    {
      path: '/experiment',
      name: 'Experiment',
      component: Experiment,
    },
  ],
});

