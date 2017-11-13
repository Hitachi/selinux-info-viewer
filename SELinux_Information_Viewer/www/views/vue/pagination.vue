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

<template id="pagination-template">
  <ul :class="full_klass">
    <li :class="{'page-item': true, disabled: first_is_disabled}">
      <a class="page-link" href="javascript:void(0)" @click="change(0)" 
         :tabindex="(first_is_disabled) ? -1 : 1">First</a>
    </li>

    <li v-for="offset in offsets" :class="{'page-item': true, disabled: (current==offset)}">
      <a class="page-link" href="javascript:void(0)" @click="change(offset)"  
         :tabindex="(current==offset) ? -1 : 1">
        {{ (offset/limit) + 1}}
      </a>
    </li>

    <li :class="{'page-item': true, disabled: last_is_disabled}">
      <a class="page-link" href="javascript:void(0)" @click="change(all - all%limit)"  
         :tabindex="(last_is_disabled) ? -1 : 1">Last</a>
    </li>
  </ul>
</template>

<script>
  $(function(){
    Vue.component("pagination", {
      template: "#pagination-template",
      data: function(){
        return {
          
        };
      },
      model: {
        prop: 'current',
        event: 'change',
      },
      props: {
        current: {
          type: Number,
          default: 0,
        },
        limit: {
          type: Number,
          default: 25,
        },
        all: {
          type: Number,
          default: 100,
        },
        show: {
          type: Number,
          default: 10,
        },
        klass: {
          type: Object,
          default: {},
        },
      },
      computed: {
        first_is_disabled: function(){
          return this.current == 0;
        },
        last_is_disabled: function(){
          return this.current + this.limit >= this.all;
        },
        full_klass: function(){
          return $.extend({
            "pagination": true,
          }, this.klass);
        },
        offsets: function(){
          if(this.all==0){
            return [0];
          }
          var offsets = [];
          var offset = this.current;
          offset -= this.limit * 5;
          if(offset < 0) {
            offset = 0;
          }

          while(offset < this.all){
            offsets.push(offset);
            offset += this.limit;
            if(offsets.length >= this.show){
              break;
            }
          }
          return offsets;
        }
      },
      methods: {
        change: function(offset){
          if(offset==this.current){
            return
          }
          this.$emit('change', offset)
        }
      }
    });
  });
</script>
