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

<template id="file-information-template">
  <div>
    <h3>File</h3>
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <div class="card mb-4">
        <div class="card-block">
          <h4 class="card-title">File Path</h4>
          <p class="card-text">{{file.path}}</p>
        </div>
      </div>
      
      <div class="card mb-4">
        <div class="card-block">
          <h4 class="card-title">File Permission</h4>
          <p class="card-text">{{file.permission}}  {{file.owner}}  {{file.group}}</p>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-block">
          <h4 class="card-title">SELinux Label</h4>
          <p class="card-text">{{file.label.user}}:{{file.label.role}}:{{file.label.domain}}:{{file.label.level}}</p>
        </div>
      </div>

       <div class="card mb-4" v-if="file.contexts.length>0" >
        <div class="card-block">
          <h4 class="card-title">Matched File Contexts</h4>
          <div class="card" v-for="context in file.contexts">
            <div class="card-block">
              <h4 class="card-title">{{context.pattern}}</h4>
              <p class="card-text">{{context.label.user}}:{{context.label.role}}:{{context.label.domain}}:{{context.label.level}}</p>
            </div>
          </div>
        </div>
       </div>

       <div class="card mb-4" v-if="file.rules.length>0" >
        <div class="card-block">
          <b-btn class="btn-link p-0" v-b-toggle="permission_collapse_id">
            <h4 class="card-title">Permission with SELinux Domains</h4>
          </b-btn>
          <b-collapse :id="permission_collapse_id">
            <div class="form-group">
              <label>Filter</label>
              <input class="form-control" v-model="permission_filter"/>
            </div>
            <div class="card" v-for="rule in file.rules" v-if="filter([rule.source, rule.permlist], permission_filter)">
              <div class="card-block">
                <h4 class="card-title">{{rule.source}}</h4>
                <p class="card-text">{{rule.permlist}}</p>
              </div>
            </div>
          </b-collapse>
        </div>
       </div>
    </div>
  </div>
</template>

<script>
  $(function(){
    Vue.component("file-information", {
      template: "#file-information-template",
      data: function(){
        return  {
          file: null,
          permission_filter: "",
        };
      },
      props: {
        fileId: {
          type: Number,
          default: null,
        }
      },
      computed: {
        loading: function(){
          return (this.file==null); 
        },
        permission_collapse_id: function(){
          return "PCID"+Math.random().toString(16); 
        },
      },

      watch : {
        fileId : function () {
          var self = this;
          if(!self.fileId===null){
            return;
          }
          self.file = null;
          var promise = $.getJSON('/ajax/file', {
            id: self.fileId,
          });
          promise.then(function(data){
            self.file = data.file;
          });
        },
      },
      methods :{
        filter: function(items, query){
          var querys = query.toLowerCase().split(" ");
          var target = $.map(items, function(item){
            return item.toString();
          }).join(" ").toLowerCase();

          var flag = true;
          $.each(querys, function(index, query){
            if(target.indexOf(query) < 0){
              flag = false;
              return false;
            }
          });
          return flag;
        }
      },
    });
  });
</script>