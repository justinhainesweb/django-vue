<template>
  <div class="wrapper">
    <project-list
      :projects="projects"
      :tasks="tasks"
      :getProjects="getProjects"
      :getTasks="getTasks"
      :tasksTodayCount="tasksTodayCount"
    ></project-list>

    <div id="content">
      <task-list
        :projects="projects"
        :tasks="tasks"
        :getTasks="getTasks"
        :filter="filter"
        :total_tasks="totalRows"
      ></task-list>

      <b-pagination
        size="md"
        align="right"
        :totalRows="totalRows"
        v-model="currentPage"
        :perPage="perPage"
        @input="getTasks(filter, currentPage)">
      </b-pagination>

    </div>

    <footer class="footer">
      <div class="container">
        <span class="text-muted">Oleksii Velychko <i class="fab fa-python"></i> Django SPA</span>
      </div>
    </footer>

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
    TaskList
  },
  beforeCreate: function () {
    document.body.classList.remove('auth')
  },
  mounted () {
    const jwtToken = this.$store.state.jwt
    axios.defaults.headers.common['Authorization'] = `Bearer ${jwtToken}`
    axios.defaults.headers.common['Content-Type'] = 'application/json'

    this.getProjects()
  },
  data () {
    return {
      projects: [],
      tasks: [],
      tasksTodayCount: 0,
      filter: {}, // declare filters
      user: {}, // current user
      currentPage: 1, // pagination option
      perPage: 12, // pagination option
      totalRows: 0 // pagination option
    }
  },
  methods: {
    /**
     * Fetch(GET) collection of Projects Models
     */
    getProjects: function () {
      axios.get('/api/v1/project/').then((response) => {
        this.projects = response.data.projects

        if (typeof this.tasks !== 'undefined') {
          this.tasks = response.data.tasks.results
          this.totalRows = response.data.tasks.count
          this.tasksTodayCount = this.tasks.length
        }

        // init or reset filters
        this.filter = {
          project_id: 0, // selected project
          state: '', // it means 'all'
          period: '',
          title: 'Recent tasks'
        }
      }).catch(error => {
        if (error.response.data.detail) {
          this.$router.push('login')
        }
      })
    },

    /**
     * Fetch(GET) collection of Tasks Models
     */
    getTasks: function (params, page = 1) {
      axios.get(`/api/v1/task/?page=${page}`, {'params': params}).then((response) => {

        this.tasks = response.data.results ? response.data.results : []
        this.totalRows = response.data.count
        this.filter.project_id = params.project_id
        this.filter.period = params.filter_period ? params.filter_period : ''

        if (this.filter.period === 'today') {
          this.tasksTodayCount = this.tasks.length
          this.filter.title = 'Recent tasks for today'
        } else if (this.filter.period === 'last_week') {
          this.filter.title = 'Recent tasks for next week'
        }

        if (params.project_id) {
          let project = this.projects.find(x => parseInt(x.id) === parseInt(params.project_id))
          this.filter.title = project.name + ' - ' + moment(project.created).format('MMMM Do')
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
