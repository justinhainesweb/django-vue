<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <button type="button" id="sidebarCollapse" @click="toogleSidebar" class="navbar-btn">
          <span></span>
          <span></span>
          <span></span>
        </button>
        <button class="btn btn-success d-inline-block d-lg-none ml-auto" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <i class="fas fa-align-justify"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="nav navbar-nav ml-auto">
            <li class="nav-item">
              <a
                @click.prevent="filterState('all')" :class="{ 'active': filter_states.is_all }" class="nav-link">All
              </a>
            </li>
            <li class="nav-item">
              <a
                @click.prevent="filterState('active')" :class="{ 'active': filter_states.is_active }" class="nav-link">Active
              </a>
            </li>
            <li class="nav-item">
              <a @click.prevent="filterState('completed')" :class="{ 'active': filter_states.is_completed }" class="nav-link">Completed
              </a>
            </li>
            <li class="nav-item">
              <router-link to="/login" @click.native="logout()" class="nav-link" replace>Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="row">
      <div class="col-md-12 col-sm-12 col-12 title"><h4>{{ filter.title }}</h4></div>
    </div>
    <div class="row">
      <div v-if="tasks.length" class="col-md-12 col-sm-12 col-12">
        <div class="row">
          <task-item v-for="task in tasks" :key="task.id" :task="task" :projects="projects" />
        </div>
      </div>
    </div>
    <div class="row bttm">
      <task-create :projects="projects" :filter="filter" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import TaskCreate from './TaskCreate.vue'
import TaskItem from './TaskItem.vue'
import moment from 'moment'

export default {
  name: 'TaskList',
  components: {
    TaskCreate,
    TaskItem
  },
  props: [
    'projects',
    'tasks',
    'filter',
    'getTasks'
  ],
  data () {
    return {
      filter_states: {
        is_active: false,
        is_completed: false,
        is_all: true
      }
    }
  },
  /**
   * Listen events
   */
  created () {
    this.$root.$on('_vent_get_tasks', (params) => {
      this.getTasks(params)
    })

    this.$root.$on('_vent_add_task', (taskObj) => {
      this.addTask(taskObj)
    })

    this.$root.$on('_vent_edit_task', (taskObj) => {
      this.updateTask(taskObj)
    })

    this.$root.$on('_vent_delete_task', (taskId) => {
      this.deleteTask(taskId)
    })
  },
  methods: {
    /**
     * Create new Task model
     */
    addTask: function (object) {
      axios.post('/api/v1/task/', object, {params: {project_id: object.project_id}}).then((response) => {
        if (parseInt(this.filter.project_id) === parseInt(object.project_id) || !this.filter.project_id) {
          this.tasks.push(response.data)
        }

        // increase project tasks counter
        let index = this.projects.findIndex(p => parseInt(p.id) === parseInt(object.project_id))
        ++this.projects[index].task_count
      }).catch((err) => {
        console.log(err)
      })
    },

    /**
     * Update exists Task model by ID
     */
    updateTask: function (object) {
      axios.put(`/api/v1/task/${object.id}/`, object).then((response) => {
        let index = this.tasks.findIndex(p => parseInt(p.id) === parseInt(object.id))
        this.tasks[index] = response.data
      }).catch((err) => {
        console.log(err)
      })
    },

    /**
     * Delete exists Task model by ID
     */
    deleteTask: function (object) {
      axios.delete(`/api/v1/task/${object.id}/`, {params: {project_id: object.project.id}}).then((response) => {
        let index = this.tasks.findIndex(p => parseInt(p.id) === parseInt(object.id))
        this.tasks.splice(index, 1)

        // decrease project tasks counter
        index = this.projects.findIndex(p => parseInt(p.id) === parseInt(object.project.id))
        --this.projects[index].task_count
      }).catch((err) => {
        console.log(err)
      })
    },

    filterState: function (state) {
      switch (state) {
        case 'active':
          this.filter_states.is_active = !this.filter_states.is_active
          this.filter_states.is_all = false
          this.filter_states.is_completed = false
          break
        case 'completed':
          this.filter_states.is_completed = !this.filter_states.is_completed
          this.filter_states.is_all = false
          this.filter_states.is_active = false
          break
        default:
          this.filter_states.is_all = !this.filter_states.is_all
          this.filter_states.is_active = false
          this.filter_states.is_completed = false
      }

      this.getTasks({
        filter_state: state,
        filter_period: this.filter.period,
        project_id: this.filter.project_id
      })
    },

    logout () {
      // remove token from localStorage and redirect to Login page
      this.$store.commit('removeToken')
    },

    toogleSidebar: function () {
      $('#sidebar').toggleClass('active')
      $('#sidebarCollapse').toggleClass('active')
    },

    dismiss: function () {
      $('#sidebar').removeClass('active') // hide sidebar
      $('.overlay').removeClass('active') // hide overlay
    }
  }
}
</script>
