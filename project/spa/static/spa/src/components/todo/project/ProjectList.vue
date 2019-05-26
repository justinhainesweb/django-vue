<template>
  <nav id="sidebar">

    <div class="sidebar-header text-center">
      <router-link to="home">
        <h3><i class="fab fa-python"></i>&nbsp;DjangoVue&nbsp;<i class="fab fa-vuejs"></i></h3>
      </router-link>
      <br>
      <h6 class="cursor">Hello {{ userComputed.email }}</h6>
      <h5 class="cursor" @click="getProjects">Go to Home page</h5>
    </div>

    <ul class="list-unstyled components">
      <li>
        <a href="#menu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">Filter</a>
        <ul class="collapse list-unstyled" id="menu">
          <li>
            <a @click.prevent="filterTasks('today')">Today ({{ tasksTodayCount }})</a>
          </li>
          <li>
            <a @click.prevent="filterTasks('last_week')">Next 7 days</a>
          </li>
        </ul>
      </li>
      <li class="active">
        <a href="#projectsMenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
          Projects ({{ projects.length }})
        </a>
        <ul class="collapse list-unstyled" id="projectsMenu">
          <project-item v-for="project in projects" :key="project.id" :project="project" />
        </ul>
      </li>
    </ul>

    <b-button @click="showModal" class="btn-success add-btn"><i class="fas fa-plus-circle"></i>&nbsp; Add project</b-button>
    <b-modal ref="myModalRef" hide-footer title="Create project">
      <project-create :state="modalShow" />
    </b-modal>

  </nav>
</template>

<script>
import axios from 'axios'
import ProjectCreate from './ProjectCreate.vue'
import ProjectItem from './ProjectItem.vue'

export default {
  name: 'ProjectList',
  components: {
    ProjectCreate,
    ProjectItem
  },
  props: [
    'projects',
    'tasks',
    'getProjects',
    'getTasks',
    'tasksTodayCount'
  ],
  data () {
    return {
      modalShow: false
    }
  },
  computed: {
    userComputed() {
      return this.$store.state.authUser
    }
  },
  /**
   * Listen events
   */
  created () {
    this.$root.$on('_vent_create_project', (object) => {
      this.createProject(object)
    })

    this.$root.$on('_vent_edit_project', (object) => {
      this.updateProject(object)
    })

    this.$root.$on('_vent_delete_project', (projectID) => {
      this.deleteProject(projectID)
    })

    this.$root.$on('_vent_close_modal', () => {
      this.hideModal()
    })
  },
  methods: {
    /**
     * Create new Project Model
     */
    createProject: function (object) {
      axios.post('/api/v1/project/', object).then((response) => {
        this.projects.push(response.data)
      }).catch((err) => {
        console.log(err)
      })
    },

    /**
     * Update exists Project model by ID
     */
    updateProject: function (object) {
      axios.put(`/api/v1/project/${object.id}/`, object).then((response) => {
        let index = this.projects.findIndex(p => parseInt(p.id) === parseInt(response.data.id))

        this.projects[index].name = response.data.name
        this.projects[index].color = response.data.color
        this.projects[index].task_count = response.data.task_count

        // update colors in tasks
        for (let i = 0; i < this.tasks.length; i++) {
          if (parseInt(this.tasks[i].project.id) === parseInt(object.id)) {
            this.tasks[i].project.color = object.color
          }
        }
      }).catch((error) => {
        alert(error)
      })
    },

    /**
     * Delete exists Project model by ID
     */
    deleteProject: function (projectID) {
      axios.delete(`/api/v1/project/${projectID}/`).then((response) => {
        alert(response.data.message)

        if (!response.incomplete_tasks_count) {
          let index = this.projects.findIndex(p => parseInt(p.id) === parseInt(projectID))
          this.projects.splice(index, 1)

          // remove related tasks
          for (let i = 0; i < this.tasks.length; i++) {
            if (parseInt(this.tasks[i].project.id) === parseInt(projectID)) {
              this.tasks.splice(i, 1)
            }
          }
        }
      }).catch((err) => {
        console.log(err)
      })
    },

    /**
     * Filter tasks by date period
     */
    filterTasks: function (period) {
      this.getTasks({filter_period: period})
    },

    showModal () {
      this.$refs.myModalRef.show()
      this.modalShow = !this.modalShow
    },

    hideModal () {
      this.$refs.myModalRef.hide()
    }
  }
}
</script>
