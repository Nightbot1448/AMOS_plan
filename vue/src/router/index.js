import Vue from 'vue';
import Router from 'vue-router';
import Preparation from '@/components/Preparation';
import Task from '@/components/Task';
import PlanningArea from '@/components/PlanningArea';
import Planning from '@/components/Planning';
import Conduct from '@/components/Conduct';
import Processing from '@/components/Processing';
import Experiment from '@/components/Experiment';
import Mean_Var from '@/components/Mean_Var';
import Reproducibility from '@/components/Reproducibility';
import Parameter_estimation from '@/components/Parameter_estimation';
import Significance from '@/components/Significance';

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
    {
      path: '/mean_var',
      name: 'Mean_Var',
      component: Mean_Var,
    },
    {
      path: '/reproducibility',
      name: 'Reproducibility',
      component: Reproducibility,
    },
    {
      path: '/parameter_estimation',
      name: 'Parameter_estimation',
      component: Parameter_estimation,
    },
    {
      path: '/significance',
      name: 'Significance',
      component: Significance,
    },
  ],
});

