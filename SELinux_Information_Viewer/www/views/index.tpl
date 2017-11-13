<!DOCTYPE html>
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
<html>
  <head>
    <title>SELinux Information Viewer</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <link rel="stylesheet" type="text/css" href="${ url('static', filepath='css/font-awesome.min.css') }">
    <link rel="stylesheet" type="text/css" href="${ url('static', filepath='css/tether.min.css') }">
    <link rel="stylesheet" type="text/css" href="${ url('static', filepath='css/bootstrap.min.css') }">
    <link rel="stylesheet" type="text/css" href="${ url('static', filepath='css/bootstrap-vue.css') }">
    <script src="${ url('static', filepath='js/jquery.min.js') }"></script>
    <script src="${ url('static', filepath='js/polyfill.min.js') }"></script>
    <script src="${ url('static', filepath='js/vue.min.js') }"></script>
    <script src="${ url('static', filepath='js/tether.min.js') }"></script>
    <script src="${ url('static', filepath='js/bootstrap-vue.js') }"></script>

    <style>
      .slide-fade-enter-active {
        transition: all .3s ease;
        position: absolute;
      }
      .slide-fade-leave-active {
        transition: all .3s ease;
        position: absolute;
      }
      .slide-fade-enter {
        transform: translateX(100%);
        opacity: 0;
      }
      .slide-fade-leave-to{
        transform: translateX(100%);
        opacity: 0;
      }

      .slide-fade-right-enter-active {
        transition: all .3s ease;
        position: absolute;
      }
      .slide-fade-right-leave-active {
        transition: all .3s ease;
        position: absolute;
      }
      .slide-fade-right-enter {
        transform: translateX(-100%);
        opacity: 0;
      }
      .slide-fade-right-leave-to{
        transform: translateX(-100%);
        opacity: 0;
      }

    </style>

    <script>
      function requestable(body){
        var timeout_id = null;
        return function(wait){
          var self = this;
          if(!$.isNumeric(wait)){
            wait = undefined
          }
          wait = wait || 500;
          if(timeout_id){
            clearTimeout(timeout_id);
            timeout_id = null;
          }
          timeout_id = setTimeout(body.bind(self), wait);
        }
      }

      function unique_id(prefix){
          return prefix+Math.random().toString(16);
      }

    </script>
  </head>
  <body>
    <%include file="vue/toggle-button.vue"/>
    <%include file="vue/auto-complete.vue"/>
    <%include file="vue/pagination.vue"/>
    <%include file="vue/file-information.vue"/>
    <%include file="vue/sepolicy-label.vue"/>
    <%include file="vue/sepolicy-files.vue"/>
    <%include file="vue/sepolicy-filecontext-files.vue"/>
    <%include file="vue/sepolicy-file-context.vue"/>
    <%include file="vue/sepolicy-information.vue"/>
    <%include file="vue/sepolicy-networks.vue"/>
    <%include file="vue/sepolicy-bools.vue"/>
    <%include file="vue/sepolicy-rules.vue"/>
    <%include file="vue/sepolicy-processes.vue"/>
    
    <div id="app">
      <div class="container">
        <h1>SELinux Information Viewer</h1>
        <hr/>
        <b-tabs>
          <b-tab title="File Contexts" >
            <div class="pt-4">
              <sepolicy-file-context></sepolicy-file-context>
            </div>
          </b-tab>
          <b-tab title="Files" >
            <div class="pt-4">
              <sepolicy-files></sepolicy-files>
            </div>
          </b-tab>

          <b-tab title="Process">
            <div class="pt-4">
              <sepolicy-processes></sepolicy-processes>
            </div>
          </b-tab>
          
          <b-tab title="TCP/IP">
            <div class="pt-4">
              <sepolicy-networks></sepolicy-networks>
            </div>
          </b-tab>
          <b-tab title="Bools" >
            <div class="pt-4">
              <sepolicy-bools></sepolicy-bools>
            </div>
          </b-tab>
          <b-tab title="Rules" >
            <div class="pt-4">
              <sepolicy-rules></sepolicy-rules>
            </div>
          </b-tab>
          <b-tab title="Information" >
            <div class="pt-4">
              <sepolicy-information></sepolicy-information>
            </div>
          </b-tab>
        </b-tabs>
        
      </div>
      
    </div>
    <script>
      $(function(){
        var app = new Vue( {
          el: "#app",
          data: {
          },

          computed: {

          },

          methods: {
          },
          created: function(){
          }
        });
      });
    </script>


  </body>
 
</html>