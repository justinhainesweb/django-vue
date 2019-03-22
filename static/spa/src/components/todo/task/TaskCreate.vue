<template>

    <div class="col-md-12 col-sm-12 col-12">
      <form
        ref="form"
        v-if="show"
        v-on:submit.prevent="onSubmit"
        @keydown.enter="onSubmit"
        class="add-wrapper"
        >

        <div class="input-group mb-4">
          <textarea
            type="text"
            class="form-control"
            placeholder="Enter description"
            required
            v-model="defaultContent"
          ></textarea>
          <datepicker
            :value="defaultDate"
            :format="customFormatter"
            :wrapperClass="`input-group-append`"
            :bootstrap-styling="true"
            v-model="defaultDate"
          ></datepicker>
        </div>

        <div class="input-group">
          <div class="col-md-3 col-sm-6 col-6">
            <label for="defaultProjectId">Select project</label>
            <select class="form-control" v-model="filter.project_id" required id="defaultProjectId">
              <option v-for="project in projects" :value="project.id" :selected="project.id===filter.project_id">
                {{ project.name }}
              </option>
            </select>
          </div>
          <div class="col-md-3 col-sm-6 col-6">
            <label for="defaultPriority">Select priority</label>
            <select v-model="defaultPriority" class="form-control" id="defaultPriority" required>
              <option value=1>Low</option>
              <option value=2>Middle</option>
              <option value=3>High</option>
            </select>
          </div>
          <div class="col-md-3 col-sm-6 col-6 bttm">
            <button type="submit" class="btn btn-primary">
              Add task
            </button>
          </div>
          <div class="col-md-3 col-sm-6 col-6 bttm">
            <button class="btn btn-info" @click="show=!show">
              Cancel
            </button>
          </div>
        </div>

      </form>

      <b-button @click="show=!show" class="btn-success" v-else><i class="fas fa-plus-circle"></i>&nbsp; Add task</b-button>
    </div>

</template>

<script>
  import Datepicker from 'vuejs-datepicker'
  import moment from 'moment'

  export default {
    name: 'TaskCreate',
    components: {
      Datepicker
    },
	  props: [
	    'projects',
	    'filter'
	  ],
    data () {
      return {
        show: false,
        defaultContent: '',
        defaultPriority: 1,
        defaultDate: new Date()
      }
    },
    created() {
      this.$root.$on('_vent_hide_active', () => {
        this.show = false;
      })
    },
    methods: {

      customFormatter(date) {
        return moment(date).format('MMM Do');
      },

      onSubmit: function() {

        if ( moment(this.defaultDate).format('MM/DD/YYYY') < moment(new Date).format('MM/DD/YYYY') ) {
          alert('Are you sure? Do you want get back to the future?');
          return
        }

        let project = {
          'content': this.defaultContent,
          'priority': this.defaultPriority,
          'execute_date': moment(this.defaultDate).format('YYYY-MM-DD HH:MM'),
          'project_id': parseInt(this.filter.project_id)
        };

        this.$root.$emit('_vent_add_task', project);

        this.show = false;
        this.defaultContent = '';
        this.defaultPriority = 1;
        this.defaultDate = new Date();
      }
    }
  }

</script>
