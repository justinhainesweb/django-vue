<template>
  <form ref="form" @submit.prevent="onSubmit">
    <div class="row">
      <div class="col-md-1 col-sm-1 col-1">
        <colorpicker :color="defaultColor" v-model="defaultColor" />
      </div>
      <div class="col-md-11 col-sm-11 col-11">
        <input
          type="text"
          class="form-control"
          placeholder="Enter project name"
          required
          v-model="defaultName"
        >
      </div>
      <div class="col-md-12 col-sm-12 col-12" id="shared">
        <input type="checkbox" id="checkbox" v-model="defaultShared">
        <label for="checkbox">It will be used between members?</label>
      </div>
    </div>
    <br>
    <div class="row">
      <div class="col-md-6 col-sm-6 col-6">
        <button class="btn btn-danger" @click.prevent="clearFields"><i class="far fa-times-circle"></i>&nbsp; Close</button>
      </div>
      <div class="col-md-6 col-sm-6 col-6">
        <button type="submit" class="btn btn-primary"><i class="fas fa-plus-circle"></i>&nbsp; Create</button>
      </div>
    </div>
  </form>
</template>

<script>
import ColorPicker from './ColorPicker.vue'

export default {
  name: 'ProjectCreate',
  components: {
    'colorpicker': ColorPicker
  },
  props: ['state'],
  data () {
    return {
      defaultColor: '#F933FF',
      defaultName: '',
      defaultShared: 0
    }
  },
  methods: {
    clearFields: function () {
      this.defaultColor = '#F933FF'
      this.defaultName = ''
      this.$root.$emit('_vent_close_modal')
    },
    onSubmit: function () {
      this.$root.$emit('_vent_create_project', {
        'color': this.defaultColor, 'name': this.defaultName, 'shared': this.defaultShared})
      this.clearFields()
    }
  },
  watch: {
    /**
     * Listen open/close modal state
     */
    state (val) {
      this.defaultColor = '#F933FF'
      this.defaultName = ''
      this.defaultShared = 0
    }
  }
}
</script>
