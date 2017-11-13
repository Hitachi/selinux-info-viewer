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

<template id="sepolicy-bools-template">
  <div>

    <b-modal :id="dialog_id" :hide-header="true" :hide-footer="true" :close-on-backdrop="true" size="lg">
      <div v-if="detail!=null">
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">{{detail.name}}</h4>
            <p class="card-text">{{detail.desc}}</p>
          </div>
          <div class="card-block pb-0">
            <table class="table" style="max-width: 10rem">
              <thead class="thead-inverse">
                <tr>
                  <th>Default</th>
                  <th>Current</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{{detail.default}}</td>
                  <td>{{detail.current}}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="card-block pt-0">
            <table class="table">
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
                <tr v-for="rule in detail.rules">
                  <td>{{rule.type}}</td>
                  <td>{{rule.source}}</td>
                  <td>{{rule.target}}</td>
                  <td>{{rule.class}}</td>
                  <td>{{rule.enabled}}</td>
                  <td>{{rule.permlist}}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </b-modal>

    <div class="row align-items-end">
      <div class="col">
        <div class="form-group">
          <label>Query</label>
          <input type="text" v-model="query" class="form-control" @input="requestSearch">
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
          <th>Name</th>
          <th>Default</th>
          <th>Current</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items">
          <td>
            <a href="javascript:void(0)" @click="requestDetail(item)">{{item.name}}</a>
          </td>
          <td>{{item.default}}</td>
          <td>{{item.current}}</td>
          <td>{{item.desc}}</td>
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
    Vue.component("sepolicy-bools", {
      template: "#sepolicy-bools-template",
      data: function(){
        return  {
          items: [],
          query: '',
          limit: 25,
          offset: 0,
          all_count: 0,
          detail: null,
        };
      },
      methods: {
        search: function(offset){
          var self = this;
          if($.isNumeric(offset)){
            self.offset = offset;
          }
          var promise = $.getJSON('/ajax/bools',{
            limit: self.limit,
            offset: self.offset,
            query: self.query
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

        requestDetail: function(item){
          var self = this;
          var promise = $.getJSON('/ajax/bools/rules',{
            name: item.name,
          });

          promise.then(function(data){
            item.rules = data.items;
            self.detail = item;
            self.$root.$emit('show::modal', self.dialog_id);
          });
        }
      },
      computed: {
        dialog_id: function(){
          return unique_id("BD");
        }
      },
      created: function(){
        this.search(0);
      }
    });
  });
</script>