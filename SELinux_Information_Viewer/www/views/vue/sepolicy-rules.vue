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

<template id="sepolicy-rules-template">
  <div>

    <div class="row align-items-end">
      <div class="col-2">
        <div class="form-group">
          <label>Type</label>
          <auto-complete :klass="{'form-control': true}" :items="info.types" v-model="type" @enter="search(0)" ></auto-complete>
        </div>
      </div>
      <div class="col-2">
        <div class="form-group">
          <label>Source</label>
          <auto-complete :klass="{'form-control': true}" :items="info.sources" v-model="source" @enter="search(0)" ></auto-complete>
        </div>
      </div>
      <div class="col-2">
        <div class="form-group">
          <label>Target</label>
          <auto-complete :klass="{'form-control': true}" :items="info.targets" v-model="target" @enter="search(0)" ></auto-complete>
        </div>
      </div>
      <div class="col-2">
        <div class="form-group">
          <label>Class</label>
          <auto-complete :klass="{'form-control': true}" :items="info.classes" v-model="klass" @enter="search(0)" ></auto-complete>
        </div>
      </div>
      <div class="col-1">
        <div class="form-group">
          <button type='button' class="btn btn-primary" @click=search(0)>SEARCH</button>
        </div>
      </div>
      <div class="col-2">
        <div class="form-group ml-2">
          <select  v-model="limit" class="form-control" @change="search(0)">
            <option v-for="val in [10, 25, 50, 100]" :value="val">{{ val }}</option>
          </select>
        </div>
      </div>
      <div class="col-1">
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
          <th>Type</th>
          <th>Source</th>
          <th>Target</th>
          <th>Class</th>
          <th>Enabled</th>
          <th>Permission</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items">
          <td>{{item.type}}</td>
          <td>{{item.source}}</td>
          <td>{{item.target}}</td>
          <td>{{item.class}}</td>
          <td>{{item.enabled}}</td>
          <td>{{item.permlist}}</td>
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
    Vue.component("sepolicy-rules", {
      template: "#sepolicy-rules-template",
      data: function(){
        return  {
          items: [],
          type: 'allow',
          source: '',
          target: '',
          klass: '',
          limit: 25,
          offset: 0,
          all_count: 0,
          detail: null,
          info: {}
        };
      },
      methods: {
        search: function(offset){
          var self = this;
          if($.isNumeric(offset)){
            self.offset = offset;
          }
          var promise = $.getJSON('/ajax/rules',{
            limit: self.limit,
            offset: self.offset,
            type: self.type,
            source: self.source,
            target: self.target,
            "class": self.klass
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
          var promise = $.getJSON('/ajax/rules/info',{
          });

          promise.then(function(data){
            var info = data.info;
            self.info = info;
          });;
        },
      },
      computed: {
        dialog_id: function(){
          return unique_id("BD");
        }
      },
      created: function(){
        this.updateInfo();
        this.search(0);
      }
    });
  });
</script>
