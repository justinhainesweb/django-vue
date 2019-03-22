<template>
  <div class="col-md-3 col-sm-6 col-12 tp">
    <div class="task-item" :class="{ expired: isExpiredTask }" :style="'background-color: ' + task.project.color">
      <div class="row">
        <div class="col-md-10 col-sm-10 col-10">
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
        <div class="col-md-2 col-sm-2 col-2">
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
</template>

<script>
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
      content: ''
    }
  },
  computed: {
    isExpiredTask: function() {
      if (moment(this.task.final_date).format('MM/DD/YYYY') < moment(new Date).format('MM/DD/YYYY')) {
        return true
      } else {
        return false
      }
    },

    format_final_date: function () {
      return moment(this.task.final_date).format('MM/DD/YYYY');
    }
  },
  created () {
    this.$root.$on('_vent_hide_active', () => {
      this.isEdit = false
    })
  },
    methods: {
      fakeVContent: function(e){
        this.content = e.target.innerText;
      },

      saveTask: function () {
        if (moment(this.task.execute_date).format('MM/DD/YYYY') < moment(new Date()).format('MM/DD/YYYY')) {
          alert('Are you sure? Do you want get back to the future?');
          return;
        }

        /* format before will be send */
        this.task.final_date = moment(this.task.final_date).format('YYYY-MM-DD HH:MM');
        this.task.project_id = this.task.project.id;
        this.task.content = this.content;

        this.$root.$emit('_vent_edit_task', this.task);
        this.isEdit = false
      },

      deleteTask: function() {
        this.$root.$emit('_vent_delete_task', this.task);
      },

      markTask: function () {
        this.task.done = 1;
        this.task.project_id = this.task.project.id;
        this.$root.$emit('_vent_edit_task',this.task);
      },

      customFormatter (date) {
        return moment(date).format('MMMM Do');
      }
    }
  }
</script>
