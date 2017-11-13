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

<template id="sepolicy-networks-template">
  <div>
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
    <div v-for="item in items" class="mb-5">
      <div class="card">
        <div class="card-block">
          
          <h4 class="card-title">Network Process</h4>
          <table class="table mb-1" style="max-width: 30rem">
            <thead class="thead-inverse">
              <tr>
                <th>Program</th>
                <th>Protocol</th>
                <th>Domain</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{item.program || "-"}}</td>
                <td>{{item.protocol}}</td>
                <td>{{item.domain || "-"}}</td>
              </tr>
            </tbody>
          </table>

          <div class="card">
            <div class="card-block">
              <h4 class="card-title">Connection</h4>
              <div class="card">
                <div class="card-block">
                  
                  <div class="d-flex align-items-end">
                    
                    <div class="card border-0">
                      <div class="card-block pl-0 pb-0">
                        <h4 class="card-title">Local</h4>
                        <table class="table" style="max-width: 15rem" >
                          <thead class="thead-inverse">
                            <tr>
                              <th>IP</th>
                              <th>Port</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>{{item.local.ip}}</td>
                              <td>{{item.local.port}}</td>
                            </tr>
                          </tbody>
                        </table>  
                      </div>
                    </div>
                    
                    <div class="card border-0">
                      <div class="card-block pb-0">
                        <h4 class="card-title">Foreign</h4>
                        <table class="table" style="max-width: 15rem" >
                          <thead class="thead-inverse">
                            <tr>
                              <th>IP</th>
                              <th>Port</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>{{item.foreign.ip}}</td>
                              <td>{{item.foreign.port}}</td>
                            </tr>
                          </tbody>
                        </table>  
                      </div>
                    </div>

                    <div class="ml-3">
                      <table class="table" style="max-width: 15rem" >
                        <thead class="thead-inverse">
                          <tr>
                            <th>State</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>{{item.state}}</td>
                          </tr>
                        </tbody>
                      </table>  
                    </div>

                  </div>

                  <div class="card border-0">
                    <div class="card-block p-0">
                      <h4 class="card-title">Security Contexts</h4>
                      <table class="table">
                        <thead class="thead-inverse">
                          <tr>
                            <th>Type</th>
                            <th>Port Range</th>
                            <th>permission</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="port in item.ports">
                            <td>{{port.info.type}}</td>
                            <td>{{port.info.low}} - {{port.info.high}}</td>
                            <td>{{port.permlist}}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <nav>
      <pagination v-model="offset" :limit="limit" :all="all_count" @change="search"></pagination>
    </nav>
  </div>
</template>
<script>
  $(function(){
    Vue.component("sepolicy-networks", {
      template: "#sepolicy-networks-template",
      data: function(){
        return  {
          items: [],
          query: '',
          limit: 25,
          offset: 0,
          all_count: 0,
        };
      },
      methods: {
        search: function(){
          var self = this;
          var promise = $.getJSON('/ajax/network_processes',{
            limit: self.limit,
            offset: self.offset,
            query: self.query
          });

          promise.then(function(data){
            self.items = data.processes;
            self.all_count = data.all;
            $(window).scrollTop(0);
          });
        },
        requestSearch: requestable(function(){
          this.search(0);
        }),
      },
      computed: {

      },
      created: function(){
        this.search(0);
      }
    });
  });
</script>