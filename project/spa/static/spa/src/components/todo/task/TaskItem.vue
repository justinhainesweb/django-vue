<template>
  <div class="col-md-3 col-sm-6 col-12 tp" v-if="is_my">
    <div class="task-item" :style="'background-color: ' + task.project.color">
      <div class="row">
        <div class="col-md-9 col-sm-9 col-9">
          <span v-if="!isEdit" @click="isEdit=true">{{ format_final_date }}</span>
          <datepicker
            :value="task.final_date"
            :format="customFormatter"
            :wrapperClass="`input-group-append`"
            :bootstrap-styling="true"
            v-model="task.final_date"
            v-if="isEdit"
          ></datepicker>
        </div>
        <div class="col-md-3 col-sm-3 col-3">
          <i class="fas fa-trash-alt right" @click="deleteTask"></i>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12 col-sm-12 col-12"
             @click="isEdit=true"
             contenteditable
             spellcheck="false"
             @input="fakeVContent"
        >
          {{ task.content }}
        </div>
      </div>
      <div class="row" v-if="isEdit">
        <div class="col-md-12 col-sm-12 col-12">
          <input type="checkbox" id="checkbox" v-model="task.done">
          <label for="checkbox">Has been completed?</label>
        </div>
        <div class="col-md-12 col-sm-12 col-12">
          <button @click="saveTask" class="btn btn-primary">Save</button>
          <button @click="isEdit=false" class="btn btn-default">Cancel</button>
        </div>
      </div>
    </div>
  </div>
  <div class="col-md-3 col-sm-6 col-12" v-else>
    <div class="task-item" :style="'background-color: ' + task.project.color">
      <div class="row">
        <div class="col-md-9 col-sm-9 col-9">
            <span>{{ format_final_date }}</span>
        </div>
        <div class="col-md-12 col-sm-12 col-12" spellcheck="false">
          {{ task.content }}
        </div>
        <div class="col-md-12 col-sm-12 col-12">
          <i class="far fa-thumbs-up cursor right" v-if="!task.liked" @click="likeTask">{{ task.like_count }}</i>
          <i class="fas fa-thumbs-up cursor right" v-else @click="unlikeTask">{{ task.like_count }}</i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
import Datepicker from 'vuejs-datepicker'

export default {
  components: {
    Datepicker
  },
  props: [
    'task',
    'projects'
  ],
  data () {
    return {
      isEdit: false,
      content: this.task.content
    }
  },
  computed: {
    format_final_date: function () {
      return moment(this.task.final_date).format('MM/DD/YYYY')
    },
    is_my: function () {
      let projectId = this.task.project.id
      let matchingValues = this.projects.filter(function (project) { return project.id === projectId })

      if (matchingValues.length) {
        return matchingValues[0].is_my
      } else {
        return false
      }
    }
  },
  created () {
    this.$root.$on('_vent_hide_active', () => {
      this.isEdit = false
    })
  },
  methods: {
    fakeVContent: function (e) {
      this.content = e.target.innerText
    },

    saveTask: function () {
      if (moment(this.task.execute_date).format('MM/DD/YYYY') < moment(new Date()).format('MM/DD/YYYY')) {
        alert('Are you sure? Do you want get back to the future?')
        return
      } else if (!this.content.trim() || 0 === this.content.trim().length) {
        return false
      }

      /* format before will be send */
      this.task.final_date = moment(this.task.final_date).format('YYYY-MM-DD HH:MM')
      this.task.project_id = this.task.project.id
      this.task.content = this.content

      this.$root.$emit('_vent_edit_task', this.task)
      this.isEdit = false
    },

    deleteTask: function () {
      this.$root.$emit('_vent_delete_task', this.task)
    },

    markTask: function () {
      this.task.done = 1
      this.task.project_id = this.task.project.id
      this.$root.$emit('_vent_edit_task', this.task)
    },

    likeTask: function () {
      axios.post(`/api/v1/like/`, {'task_id': this.task.id}).then((response) => {
        this.task.liked = response.data.like_id
        ++this.task.like_count
      }).catch((error) => {
        alert(error)
      })
    },

    unlikeTask: function () {
      axios.delete(`/api/v1/like/${this.task.liked}/`).then((response) => {
        this.task.liked = 0
        --this.task.like_count
      }).catch((error) => {
        alert(error)
      })
    },

    customFormatter (date) {
      return moment(date).format('MMMM Do')
    }
  }
}
</script>
