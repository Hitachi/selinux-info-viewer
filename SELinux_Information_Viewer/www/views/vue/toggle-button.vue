<!--
# Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.
#
# Licensed under the MIT License.
# You may obtain a copy of the License at
#
#    https://opensource.org/licenses/MIT
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OF ANY KIND.
-->

<template id="toggle-button-template">
  <button  type="button" class="btn btn-secondary" :class="mode" @click="toggle" style="border: 1px solid #ccc" >
    <slot>Button</slot>
  </button>
</template>

<script>
  $(function(){
    Vue.component("toggle-button", {
      template: "#toggle-button-template",
      data: function(){
        return {
        };
      },
      model: {
        prop: 'value',
        event: 'change',
      },
      props: {
        value:{
          type: Boolean,
          default: false,
        }
      },
      computed: {
        mode: function(){
          var key = (this.value) ? "btn-info" : "btn-default";
          var klass = {}
          klass[key] = true;
          return klass;
        },
      },
      methods: {
        toggle: function(){
          this.value = !this.value;
          this.$emit('change', this.value);
        }
      }
    });
  });
</script>
