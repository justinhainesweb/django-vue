<template>
  <div class="input-group color-picker" ref="colorpicker">
	  <span class="input-group-addon color-picker-container">
		  <i class="color-item" :style="'background-color: ' + colorValue" @click="togglePicker()"></i>
		  <compact-picker :value="colors" @input="updateFromPicker" v-if="displayPicker" />
	  </span>
  </div>
</template>

<script>
  import { Compact } from 'vue-color'

  export default {
    name: 'ColorPicker',
    components: {
      'compact-picker': Compact
    },
    props: ['color'],
	  data () {
		  return {
			  colors: {
				  hex: '#F933FF',
			  },
			  colorValue: '',
			  displayPicker: false,
		  }
	  },
    mounted () {
		  this.setColor(this.color || '#F933FF');
	  },
    methods: {
		  setColor (color) {
			  this.updateColors(color);
			  this.colorValue = color;
		  },

		  updateColors (color) {
			  if (color.slice(0, 1) === '#') {
				  this.colors = {
				    hex: color
				  }
			  } else if (color.slice(0, 4) === 'rgba') {
				  let rgba = color.replace(/^rgba?\(|\s+|\)$/g,'').split(','),
					  hex = '#' + ((1 << 24) + (parseInt(rgba[0]) << 16) + (parseInt(rgba[1]) << 8) + parseInt(rgba[2])).toString(16).slice(1);
				  this.colors = {
					  hex: hex,
					  a: rgba[3]
				  }
			  }
		  },

		  showPicker () {
			  document.addEventListener('click', this.documentClick);
			  this.displayPicker = true;
		  },

		  hidePicker () {
			  document.removeEventListener('click', this.documentClick);
			  this.displayPicker = false;
		  },

		  togglePicker () {
			  this.displayPicker ? this.hidePicker() : this.showPicker();
		  },

		  updateFromInput () {
			  this.updateColors (this.colorValue);
		  },

		  updateFromPicker (color) {
			  this.colors = color;

			  if (parseInt(color.rgba.a) === 1) {
				  this.colorValue = color.hex;
			  } else {
				  this.colorValue = 'rgba(' + color.rgba.r + ', ' + color.rgba.g + ', ' + color.rgba.b + ', ' + color.rgba.a + ')'
			  }
		  },

		  documentClick (e) {
			  let el = this.$refs.colorpicker, target = e.target
        if (el !== target && !el.contains(target)) {
          this.hidePicker()
        }
		  }
	  },

	  watch: {
		  colorValue (val) {
			  if (val) {
				  this.updateColors(val);
				  this.$emit('input', val);
			  }
		  },

		  color (val) {
			  this.setColor(val || '#F933FF');
		  }
	  }
	}

</script>
