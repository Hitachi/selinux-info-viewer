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

<template id="sepolicy-information-template">
  <div>
    <div class="card mb-4">
      <div class="card-block">
        <h4 class="card-title">Created Date</h4>
        <p class="card-text">{{info.date}}</p>
      </div>
    </div>

    <div class="card mb-4" v-if="info.status">
      <div class="card-block">
        <h4 class="card-title">SELinux</h4>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">SELinux status</h4>
            <p class="card-text">{{info.status["SELinux status"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Current mode</h4>
            <p class="card-text">{{info.status["Current mode"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Mode from config file</h4>
            <p class="card-text">{{info.status["Mode from config file"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Policy Path</h4>
            <p class="card-text">{{info.policy}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">SELinux root directory</h4>
            <p class="card-text">{{info.status["SELinux root directory"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Loaded policy name</h4>
            <p class="card-text">{{info.status["Loaded policy name"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Max kernel policy version</h4>
            <p class="card-text">{{info.status["Max kernel policy version"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Policy MLS status</h4>
            <p class="card-text">{{info.status["Policy MLS status"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Policy deny_unknown status</h4>
            <p class="card-text">{{info.status["Policy deny_unknown status"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">SELinuxfs mount</h4>
            <p class="card-text">{{info.status["SELinuxfs mount"]}}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="card mb-4" v-if="info.platform">
      <div class="card-block">
        <h4 class="card-title">Host</h4>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Hostname</h4>
            <p class="card-text">{{info.platform["hostname"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">System</h4>
            <p class="card-text">{{info.platform["system"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Machine</h4>
            <p class="card-text">{{info.platform["machine"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Platform</h4>
            <p class="card-text">{{info.platform["platform"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Version</h4>
            <p class="card-text">{{info.platform["version"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Release</h4>
            <p class="card-text">{{info.platform["release"]}}</p>
          </div>
        </div>
      </div>
    </div>


    <div class="card mb-4"  v-if="info.python">
      <div class="card-block">
        <h4 class="card-title">Python</h4>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Python version</h4>
            <p class="card-text">{{info.python["version"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Python build date</h4>
            <p class="card-text">{{info.python["build_date"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Python build number</h4>
            <p class="card-text">{{info.python["build_number"]}}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-block">
            <h4 class="card-title">Python compiler</h4>
            <p class="card-text">{{info.python["compiler"]}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  $(function(){
    Vue.component("sepolicy-information", {
      template: "#sepolicy-information-template",
      data: function(){
        return  {
          info: {},
        };
      },
      created: function(){
        var self = this;
        var promise = $.getJSON('/ajax/info');
        promise.then(function(data){
          self.info = data.info;
        });
      }
    });
  });
</script>