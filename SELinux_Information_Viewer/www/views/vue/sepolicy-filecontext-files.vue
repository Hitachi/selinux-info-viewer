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

<template id="sepolicy-filecontext-files-template">
  <div class="container">
    <div class="row align-items-end">
      <div class="col-5">
        <div class="form-group">
          <label>Path Filter</label>
          <input type="text" v-model="path" class="form-control" @input="requestSearch">
        </div>
      </div>
      <div class="col-3">
        <div class="form-group">
          <label>Filter</label>
          <input type="text" v-model="keyword" class="form-control" @input="requestSearch">
        </div>
      </div>
      <div class="col-2">
        <div class="form-group">
          <select  v-model="limit" class="form-control" @change="search(0)">
            <option v-for="val in [10, 25, 50, 100]" :value="val">{{ val }}</option>
          </select>
        </div>
      </div>
      <div class="col-2">
        <div class="form-group text-center">
          <label >HIT</label>
          <div>{{all_count}}</div>
        </div>
      </div>
    </div>
    <h4>Matched Files</h4>
    <table class="table">
      <thead>
        <tr>
          <th>File Path</th>
          <th>File Type</th>
          <th>SELinux Type</th>
          <th>Label</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items">
          <td>{{item["path"]}}</td>
          <td>{{item["file_type"]}}</td>
          <td><sepolicy-label :value="item['label']" :only-domain="true" ></sepolicy-label></td>
          <td><sepolicy-label :value="item['label']"></sepolicy-label></td>
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
    Vue.component("sepolicy-filecontext-files", {
      template: "#sepolicy-filecontext-files-template",
      data: function(){
        return  {
          items: [],
          path: "/",
          keyword: "",
          limit: 25,
          offset: 0,
          all_count: 0,
        };
      },
      
      props: {
        fcontext: {
          type: Number,
          default: -1,
        },
      },

      computed: {

      },
      
      methods: {
        search: function(offset){
          var self = this;
          if($.isNumeric(offset)){
            self.offset = offset;
          }
          var promise = $.getJSON('/ajax/filecontexts/files',{
            fcontext: self.fcontext,
            path: self.path,
            keyword: self.keyword,
            limit: self.limit,
            offset: self.offset,
          });

          promise.then(function(data){
            self.items = data.items;
            self.all_count = data.all;
            $(window).scrollTop(0);
          });
        },
        requestSearch: requestable(function(){
          this.search(0);
        }),

      },
      
      watch : {
        fcontext : function () {
          this.items = [];
          this.search(0);
        },
      },
      
      created: function(){
        this.search(0);
      }
    });
  });
</script>