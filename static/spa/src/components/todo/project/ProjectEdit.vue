<template>
  <div class="col-md-12 col-sm-12 col-12">
    <br>
    <form class="add-wrapper" @submit.prevent="onSubmit">
      <div class="row">
        <div class="col-md-2 col-sm-2 col-2">
          <colorpicker :color="projectClone.color" v-model="projectClone.color" />
        </div>
        <div class="col-md-10 col-sm-10 col-10">
          <input
            type="text"
            class="form-control"
            placeholder="Enter new name"
            required
            v-model="projectClone.name"
          >
        </div>
      </div>
      <br>
      <div class="row">
        <div class="col-md-4 col-sm-4 col-4">
          <button type="submit" class="btn btn-primary" title="Save"><i class="fas fa-save"></i></button>
        </div>
        <div class="col-md-4 col-sm-4 col-4">
          <button class="btn btn-danger" @click.prevent="deleteProject" title="Save"><i class="far fa-trash-alt"></i></button>
        </div>
        <div class="col-md-4 col-sm-4 col-4">
          <button class="btn btn-info" @click.prevent="hideBtn" title="Close"><i class="fas fa-times"></i></button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
  import ColorPicker from './ColorPicker.vue'

  export default {
    name: 'ProjectEdit',
    components: {
      'colorpicker': ColorPicker
    },
    props: {
      propProject: {
        type: Object,
        required: true
      }
    },
    data: function () {
      return {
        projectClone: {...this.propProject} // deep copying
      }
    },
    methods: {
      hideBtn: function() {
        this.$root.$emit('_vent_hide_edit_project', this.projectClone.id);
      },

      onSubmit: function() {
        this.$root.$emit('_vent_edit_project', this.projectClone);
        this.hideBtn()
      },

      deleteProject: function() {
        this.$root.$emit('_vent_delete_project', this.projectClone.id);
        this.hideBtn()
      }
    }
  }
</script>
