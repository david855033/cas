
<template>
  <div class="main">
    <h1>Clinical Alerting System Prototype</h1>
    <h4>{{ msg }}</h4>
    <input v-model="ward">
    <button @click="subscribe">subscribe</button>
    <div class="patients">
      <patient
        v-for="(item, index) in patient_list"
        :patient="item"
        :key="index"
      ></patient>
    </div>
  </div>
</template>

<script>
/*eslint no-console: ["error", { allow: ["warn", "error","log"] }] */
import Patient from "./Patient.vue";

let ws;
export default {
  name: "PatientCollection",
  components: {
    Patient
  },
  data() {
    return {
      msg: "",
      ward: "A091",
      patient_list: []
    };
  },
  methods: {
    subscribe: function() {
      let vm = this;
      ws.send(
        JSON.stringify({
          action: "subscribe",
          type: "ward",
          content: vm.ward
        })
      );
    },
    connect: function() {
      let vm = this;
      ws = new WebSocket("ws://192.168.2.109:5000");
      ws.onopen = function() {
        vm.subscribe();
      };
      ws.onmessage = function(event) {
        let data = JSON.parse(event.data);

        if (data.type == "patientcollection") {
          console.log("update patientcollection");
          let content = data.content;
          vm.patient_list = content;
        } else if (data.type == "patient") {
          var hisid = data.content.hisid;
          console.log("update patient: " + hisid);
          let matchPatientIndex = vm.patient_list.findIndex(function(e) {
            return e.hisid == hisid;
          });
          vm.patient_list.splice(matchPatientIndex, 1, data.content);
        } else if (data.type == "users") {
          vm.msg = "Connected. Active users:" + data.content;
        }
      };
      ws.onclose = function() {
        vm.msg = "Disconnected. Reconnect will be attempted in 1 second.";
        setTimeout(function() {
          vm.connect();
        }, 1000);
      };
      ws.onerror = function(err) {
        vm.msg = "Socket encountered error: " + err.message + "Closing socket";
        ws.close();
      };
    }
  },
  mounted: function() {
    this.connect();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.patients{
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex-wrap: wrap;
}

</style>
