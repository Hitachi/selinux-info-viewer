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

<template id="sepolicy-processes-template">
  <div>
    <div class="row align-items-end">
      <div class="col-3">
        <div class="form-group">
          <label>Name</label>
          <auto-complete :klass="{'form-control': true}" :items="info.names" v-model="name" @enter="search(0)" ></auto-complete>
        </div>
      </div>
      <div class="col-3">
        <div class="form-group">
          <label>Domain</label>
          <auto-complete :klass="{'form-control': true}" :items="info.domains" v-model="domain" @enter="search(0)" ></auto-complete>
        </div>
      </div>
      <div class="col-2">
        <div class="form-group">
          <button type='button' class="btn btn-primary" @click=search(0)>SEARCH</button>
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
        <div class="card border-0">
          <div class="card-block">
            <h4 class="card-title">Hit</h4>
            <div class="card-text">{{all_count}}</div>
          </div>
        </div>
      </div>     
    </div>
 

    <table class="table mb-1">
      <thead class="thead-inverse">
        <tr>
          <th>PID</th>
          <th>Name</th>
          <th>Domain</th>
          <th>Label</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items">
          <td>{{item.pid}}</td>
          <td>{{item.name}}</td>
          <td>{{item.label.domain}}</td>
          <td>{{item.label.user}}:{{item.label.role}}:{{item.label.domain}}:{{item.label.level}}</td>
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
    Vue.component("sepolicy-processes", {
      template: "#sepolicy-processes-template",
      data: function(){
        return  {
          items: [],
          name: '',
          domain: '',
          info: {},
          limit: 25,
          offset: 0,
          all_count: 0,
        };
      },
      methods: {
        search: function(offset){
          var self = this;
          if($.isNumeric(offset)){
            self.offset = offset;
          }
          var promise = $.getJSON('/ajax/processes',{
            limit: self.limit,
            offset: self.offset,
            name: self.name,
            domain: self.domain,
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
        
        updateInfo: function(){
          var self = this;
          var promise = $.getJSON('/ajax/processes/info',{
          });

          promise.then(function(data){
            var info = data.info;
            self.info = info;
          });;
        },
      },

      computed: {
      
      },
      
      created: function(){
        this.updateInfo();
        this.search(0);
      }
    });
  });
</script>