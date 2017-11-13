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

<template id="auto-complete-template">
  <div>
    <input v-model="value" :class="klass" @input="input" @keyup.enter="enter" autocomplete="on" type="text" :list="list_id"/>
    <datalist :id="list_id" v-if="items">
      <option v-for="item in items" :value="item"></option>
    </datalist>
  </div>
</template>

<script>
  $(function(){
    Vue.component("auto-complete", {
      template: "#auto-complete-template",
      data: function(){
        return {
        };
      },
      model: {
        prop: 'value',
        event: 'input'
      },
      props: {
        value:{
          type: String,
          default: "",
        },
        items: {
          type: Array,
          default: [],
        },
        klass: {
          type: Object,
          default: {},
        },
      },
      computed: {
        list_id: function(){
          return "LIST"+ Math.random().toString(16);
        },
      },
      methods: {
        input: function(){
          this.$emit('input', this.value)
        },
        enter: function(){
          this.$emit('enter', this.value)
        }
      },
      created: function(){
      }
    });
  });
</script>
