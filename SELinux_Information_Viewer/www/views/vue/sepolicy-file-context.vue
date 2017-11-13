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

<template id="sepolicy-file-context-template">
  <div class="container" style="position: relative">
    <div class="d-flex">

      <transition name="slide-fade-right">
        <div v-show="mode_main" key="main">
          <nav class="container mb-4">
            <form @submit.prevent>
              <div class="row align-items-end">
                <div class="col-3">
                  <div class="form-group">
                    <label>Process Domain</label>
                    <auto-complete :klass="{'form-control': true}" :items="domains" v-model="source" @enter="search(0)" ></auto-complete>
                  </div>
                </div>
                <div class="col-3">
                  <div class="form-group">
                    <label>Filter</label>
                    <input v-model="filter" class="form-control" @input="requestSearch" />
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
                  <div class="form-group">
                    <button type="button" class="form-control btn btn-primary" @click="search(0)">SEARCH</button>
                  </div>
                </div>                
                <div class="col-2">
                  <div class="form-group text-center">
                    <label >HIT</label>
                    <div>{{all_count}}</div>
                  </div>
                </div>
              </div>
            </form>
          </nav>
          <h3>File Contexts</h3>
          <table class="table">
            <thead class="thead-inverse">
              <tr>
                <th style="width: 10rem">SELinux Type</th>
                <th style="width: 9rem">File Type</th>
                <th style="width: 20rem">Label</th>
                <th>File Pattern</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="$.isEmptyObject(items)" >
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
              </tr>
              <tr v-else v-for="item in items" :id="'CONTEXTS'+item['id']">
                <td :style="{ 'word-break': 'break-all'}">{{ display_domain(item["label"])  }}</td>
                <td :style="{ 'word-break': 'break-all'}">{{ item["type"] }}</td>
                <td :style="{ 'word-break': 'break-all'}">{{ display_label(item["label"])  }}</td>
                <td :style="{ 'word-break': 'break-all'}">
                  <button v-if="item['has_files']"  type="button" class="btn btn-link p-0" @click="search_files(item)">{{ item["pattern"] }}</button>
                  <template v-else>{{ item["pattern"] }}</template>
                </td>
              </tr>
            </tbody>
          </table>
          <nav>
            <pagination :klass="{'justify-content-center': true}" v-model="offset" :limit="limit" :all="all_count" @change="search"></pagination>
          </nav>
        </div>
      </transition>
      
      <transition name="slide-fade">
        <div v-if="mode_files" key="files">
          <button type="button" class="btn btn-default mb-2" @click="back_main(search_file_target)">Back</button>
          <hr>
          <h3>File Context</h3>
          <table class="table">
            <thead class="thead-inverse">
              <tr>
                <th style="width: 10rem">SELinux Type</th>
                <th style="width: 9rem">File Type</th>
                <th style="width: 20rem">Label</th>
                <th>File Pattern</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td :style="{ 'word-break': 'break-all'}">{{ display_domain(search_file_target["label"])  }}</td>
                <td :style="{ 'word-break': 'break-all'}">{{ search_file_target["type"] }}</td>
                <td :style="{ 'word-break': 'break-all'}">{{ display_label(search_file_target["label"])  }}</td>
                <td :style="{ 'word-break': 'break-all'}">{{ search_file_target["pattern"] }}</td>
              </tr>
            </tbody>
          </table>
          <sepolicy-filecontext-files  :fcontext="search_file_target['id']"></sepolicy-filecontext-files>
        </div>
      </transition>
    
    </div>
  </div>
</template>

<script>
  $(function(){
    Vue.component("sepolicy-file-context", {
      template: "#sepolicy-file-context-template",
      data: function(){
        return  {
          source: "",
          filter: "",
          items: [],
          all_count: 0,
          limit: 25,
          offset: 0,

          domains: [],

          search_file_target: null,
        };
      },
      computed: {
        
        mode_main: function(){
          return (this.search_file_target == null);
        },

        mode_files: function(){
          return (this.search_file_target != null);
        },
      },

      methods: {
        load_domains: function(){
          var self = this;
          var promise = $.getJSON('/ajax/domains');
          promise.then(function(data){
            self.domains = data.domains;
          });
        },

        search: function(offset){
          var self = this;
          if($.isNumeric(offset)){
            self.offset = offset;
          }
          var promise = $.getJSON('/ajax/filecontexts/accessable',{
            "source": self.source,
            "filter": self.filter,
            "limit": self.limit,
            "offset": self.offset,
          });
          promise.then(function(data){
            self.all_count = data.all;
            self.items = data.items;
            $(window).scrollTop(0);
          });
        },

        requestSearch: requestable(function(){
          this.search(0);
        }),

        display_label: function(label){
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

        display_domain: function(label){
          if(!label){
            return "-"
          }
          return label["domain"];
        },

        search_files: function(item){
          this.search_file_target = item;
        },

        back_main: function(target){
          this.search_file_target = null;
          Vue.nextTick(function () {
            window.location.hash='CONTEXTS'+target["id"];
          });
        },

      },

      created: function(){
        this.load_domains();
      }
    });
  });
</script>