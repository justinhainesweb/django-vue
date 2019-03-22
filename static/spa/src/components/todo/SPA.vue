<template>
  <div class="wrapper">
    <project-list
      :projects="projects"
      :tasks="tasks"
      :getProjects="getProjects"
      :getTasks="getTasks"
      :tasksTodayCount="tasksTodayCount"
    />
    <div id="content">
      <task-list
        :projects="projects"
        :tasks="tasks"
        :getTasks="getTasks"
        :filter="filter"
      />
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import moment from 'moment'
  import ProjectList from './project/ProjectList.vue'
  import TaskList from './task/TaskList.vue'

  export default {
    name: 'SPA',
    components: {
      ProjectList,
      TaskList,
    },
    beforeCreate: function () {
      document.body.classList.remove('auth')
    },
    mounted () {
      const jwtToken = this.$store.state.jwt;
      axios.defaults.headers.common['Authorization'] = `Bearer ${jwtToken}`;
      axios.defaults.headers.common['Content-Type'] = 'application/json';

      this.getProjects()
    },
    data () {
      return {
        projects: [],
        tasks: [],
        tasksTodayCount: 0,
        filter: {} // declare filters
      }
    },
    methods: {
      /**
       * Fetch(GET) collection of Projects Models
       */
      getProjects: function () {
        axios.get('/api/v1/project/').then((response) => {
          this.projects = response.data.projects;

          if (typeof this.tasks != 'undefined') {
            this.tasks = response.data.tasks;
            this.tasksTodayCount = this.tasks.length;
          }

          // init or reset filters
          this.filter = {
            project_id: 0, // selected project
            state: '', // it means 'all'
            period: 'today',
            title: 'Recent tasks'
          }
        }).catch(error => {
          if (error.response.data.detail) {
            this.$router.push('login');
          }
        })
      },

      /**
       * Fetch(GET) collection of Tasks Models
       */
      getTasks: function (params) {
        axios.get('/api/v1/task/', {params: params}).then((response) => {
          this.tasks = response.data ? response.data : [];
          this.filter.project_id = params.project_id;
          this.filter.period = params.filter_period ? params.filter_period : '';

          if (this.filter.period === 'today') {
            this.tasksTodayCount = this.tasks.length;
            this.filter.title = 'Recent tasks for today';
          } else if (this.filter.period === 'last_week') {
            this.filter.title = 'Recent tasks for next week';
          }

          if (params.project_id) {
            let project = this.projects.find(x => parseInt(x.id) === parseInt(params.project_id));
            this.filter.title = project.name + ' - ' + moment(project.created).format('MMMM Do');
          }
        }).catch(error => {
            if (error.response.data.detail) {
              this.$router.push('login')
            }
          })
      }
  }
}
</script>
