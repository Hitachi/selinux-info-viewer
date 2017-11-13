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

<template id="sepolicy-label-template">
  <span>
    <template v-if="onlyDomain">
      {{ domain }}
    </template>
    <template v-else>
      {{ label }}
    </template>
  </span>
</template>

<script>
  $(function(){
    Vue.component("sepolicy-label", {
      template: "#sepolicy-label-template",
      data: function(){
        return {
        };
      },
      model: {
      },
      props: {
        value:{
          type: String,
          default: null,
        },
        onlyDomain: {
          type: Boolean,
          default: false,
        }
      },
      computed: {
        label: function(){
          var label = this.value;
          if(!label){
            return "-"
          }
          return [
            label["user"],
            label["role"],
            label["domain"],
            label["level"]
          ].join(":");
        },

        domain: function(){
          var label = this.value;
          if(!label){
            return "-"
          }
          return label["domain"];
        },
      },
      methods: {
      },
      created: function(){
      }
    });
  });
</script>
