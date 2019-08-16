<template>
  <li class="cursor" @mouseover="isEdit=true" @mouseleave="isEdit=false">
    <div class="project-wrapper">
      <span :style="'background-color: ' + project.color" class="color-item"></span>
      <span class="item-name" :class="{ current: isActive }" @click="showTasks">{{ project.name }}</span>
      <span :style="'color: #ccc'">({{ this.project.task_count }})</span>
      <i class="far fa-edit" v-if="isEdit && this.project.is_my" @click="showEditBtn=true"></i>
      <project-edit :propProject="project" v-if="showEditBtn && this.project.is_my" />
    </div>
  </li>
</template>

<script>
import ProjectEdit from './ProjectEdit.vue'

export default {
  components: {
    ProjectEdit
  },
  props: {
    project: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      showEditBtn: false,
      isEdit: false,
      isActive: false
    }
  },
  created () {
    this.$root.$on('_vent_hide_edit_project', (projectID) => {
      if (parseInt(projectID) === parseInt(this.project.id)) {
        this.showEditBtn = false
      }
    })

    this.$root.$on('_vent_get_tasks', (params) => {
      if (parseInt(params.project_id) !== parseInt(this.project.id)) {
        this.isActive = false
      }
    })

    this.$root.$on('_vent_hide_active', (params) => {
      this.isActive = false
    })
  },
  methods: {
    showTasks: function () {
      this.isActive = true
      this.$root.$emit('_vent_get_tasks', {project_id: this.project.id})
    }
  }
}
</script>
