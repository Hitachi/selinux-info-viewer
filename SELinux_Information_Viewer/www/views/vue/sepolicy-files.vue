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

<template id="sepolicy-files-template">
  <div>
    <b-modal :id="dialog_id" :hide-header="true" :hide-footer="true" :close-on-backdrop="true" size="lg">
      <file-information :file-id="detail_id"></file-information>
    </b-modal>
    <div class="row align-items-end">
      <div class="col">
        <div class="form-group">
          <label>Path</label>
          <input type="text" v-model="path" class="form-control" @input="requestSearch">
        </div>
      </div>
      <div class="col-2">
        <div class="form-group">
          <select  v-model="limit" class="form-control" @change="search(0)">
            <option v-for="val in [10, 25, 50, 100]" :value="val">{{ val }}</option>
          </select>
        </div>
      </div>
    </div>
    <h3>Files</h3>
    <table class="table">
      <thead>
        <tr>
          <th>File Path</th>
          <th>SELinux Type</th>
          <th>fContext Type</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :class="{'table-warning': item.warning }" >
          <td>
            <button type="button" class="btn btn-link" @click="detail(item.id)">{{item.path}}</button>
          </td>
          <td>{{item.domain}}</td>
          <td >{{item.context}}</td>
        </tr>
      </tbody>
    </table>
    <nav>
      <pagination v-model="offset" :limit="limit" :all="all_count" @change="search"></pagination>
    </nav>
  </div>
</template>
<script>
  $(function(){
    Vue.component("sepolicy-files", {
      template: "#sepolicy-files-template",
      data: function(){
        return  {
          files: [],
          path: "",
          limit: 25,
          offset: 0,
          all_count: 0,
          detail_id: null,
        };
      },
      
      computed: {
        dialog_id: function(){
          return "ID"+Math.random().toString(16);
        },
        items: function(){
          return $.map(this.files, function(file){
            var domain = file.label.domain;
            var item = {
              id: file.id,
              path: file.path,
              domain: domain,
            }
            var warning = false;
            var c_domain = "-";
            if(file.context){
              c_domain = file.context.label.domain;
              if(c_domain!=domain){
                warning = true;
              }
              if(!c_domain){
                c_domain = "None"
              }
            }
            item.context = c_domain;
            item.warning = warning;
            return item;
          });
        }
      },
      methods: {
        search: function(offset){
          var self = this;
          if($.isNumeric(offset)){
            self.offset = offset;
          }
          var promise = $.getJSON('/ajax/files',{
            path: self.path,
            limit: self.limit,
            offset: self.offset,
          });

          promise.then(function(data){
            self.files = data.files;
            self.all_count = data.all;
            $(window).scrollTop(0);
          });
        },
        requestSearch: requestable(function(){
          this.search(0);
        }),

        detail: function(id){
          this.detail_id = id;
          this.$root.$emit('show::modal', this.dialog_id);
        },
      },
      created: function(){
        this.search(0);
      }
    });
  });
</script>