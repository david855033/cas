<template>
  <div class='patient-card'>
    <div class="col">
      <div class='basicinfo'>
        <div>{{patient.ward}}-{{patient.bedno}}</div>
        <div>{{patient.name}}</div>
        <div>{{patient.age}}歲 {{patient.gender}}</div>
        <div>{{patient.hisid}}</div>
        <div>{{patient.caseno}}</div>
        <div>{{patient.section}}</div>
      </div>
    </div>
    <div class="col">
      <div class="row">NEWS</div>
      <div class="row">Risk Group</div>
    </div>
    <div class="col">
      <div class="row">Delta</div>
      <div class="row">
        <div class="box-title">BT</div>
        <div class="box-content">{{last_bt[0]}}</div>
        <div class="box-subtitle">{{last_bt[1]}}</div>
      </div>
    </div>
    <div class="col">
      <div class="row">
        <div class="box-title">HR</div>
        <div class="box-content">{{last_hr[0]}}</div>
        <div class="box-subtitle">{{last_hr[1]}}</div>
      </div>
      <div class="row">
        <div class="box-title">SBP</div>
        <div class="box-content">{{last_sbp[0]}}</div>
        <div class="box-subtitle">{{last_sbp[1]}}</div>
      </div>
    </div>
    <div class="col">
      <div class="row">
        <div class="box-title">RR</div>
        <div class="box-content">{{last_rr[0]}}</div>
        <div class="box-subtitle">{{last_rr[1]}}</div>
      </div>
      <div class="row">
        <div class="box-title">SAT</div>
        <div class="box-content">{{last_sat[0]}}</div>
        <div class="box-subtitle">{{last_sat[1]}}</div>
      </div>
    </div>

    <div class="col">
      <div class="row">
        <div class="box-title">RespDevice</div>
        <div class="box-content device">{{last_device[0]}}</div>
        <div class="box-subtitle">{{last_device[1]}}</div>
      </div>
      <div class="row">
        <div class="box-title">GCS</div>
        <div class="box-content">{{last_gcs[0]}}</div>
        <div class="box-subtitle">{{last_gcs[1]}}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Patient",
  props: {
    patient: {
      hisid: String,
      caseno: String,
      name: String,
      age: String,
      ward: String,
      bedno: String,
      section: String,
      hr: [],
      rr: [],
      bt: [],
      sat: [],
      sbp: [],
      gcs: [],
      device: [],
      news: []
    }
  },
  computed: {
    last_bt: function() {
      let vm = this;
      return vm.get_last_element(vm.patient.bt);
    },
    last_hr: function() {
      let vm = this;
      return vm.get_last_element(vm.patient.hr);
    },
    last_sbp: function() {
      let vm = this;
      return vm.get_last_element(vm.patient.sbp);
    },
    last_rr: function() {
      let vm = this;
      return vm.get_last_element(vm.patient.rr);
    },
    last_sat: function() {
      let vm = this;
      return vm.get_last_element(vm.patient.sat);
    },
    last_device: function() {
      let vm = this;
      return vm.get_last_element(vm.patient.device);
    },
    last_gcs: function() {
      let vm = this;
      return vm.get_last_element(vm.patient.gcs);
    }
  },
  methods: {
    datetime_formatter: function(input) {
      let split = input.split(" ");
      let date =
        Number(split[0].slice(5, 7)) +
        "/" +
        split[0].slice(9, 10) +
        " " +
        String(split[1].slice(0, 5));
      return date;
    },
    get_last_element: function(input_array) {
      let vm = this;
      if (input_array.length == 0) {
        return ["-", ""];
      } else {
        let last_element = input_array[input_array.length - 1];
        return [
          last_element.value,
          vm.datetime_formatter(last_element.datetime)
        ];
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.patient-card {
  font-size: 0.8rem;
  background: #fff;
  height: 120px;
  width: 480px;
  margin: 10px;
  border-radius: 5px;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.2),
    4px 4px 10px 1px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: row;
  .basicinfo {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
  }
  .col {
    width: 80px;
    border-radius: 5px;
    // background-color: pink;
    .row {
      box-shadow: 0px 0px 1px 0 rgba(0, 0, 0, 0.5) inset;
      height: 60px;
      .box-title {
        padding: 2px;
        height: 11px;
        font-size: 0.8rem;
      }
      .box-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-top: 3px;
        height: 27px;
        font-size: 1rem;
        &.device {
          font-size: 0.8rem !important;
        }
        font-weight: 700;
      }
      .box-subtitle {
        font-size: 0.6rem;
        padding: 2px;
        height: 11px;
      }
    }
  }
}
</style>
