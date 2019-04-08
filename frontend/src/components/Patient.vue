<template>
  <div class='patient-card'>
    <div class="col">
      <div class='basicinfo'>
        <div>{{patient.ward}}-{{patient.bedno}}</div>
        <div class="name">{{patient.name}}</div>
        <div>{{patient.age}}歲 {{patient.gender}}</div>
        <div>{{patient.hisid}}</div>
        <!-- <div>{{patient.caseno}}</div> -->
        <div>{{patient.section}}</div>
      </div>
    </div>
    <div class="col">
      <div class="row">
        <div class="box-title">NEWS</div>
        <div class="box-content news">{{last_news}}</div>
      </div>
      <div class="row">
        <div class="box-title">Delta</div>
        <div class="box-content delta">{{delta}}</div>
      </div>
    </div>
    <div class="col">
      <div class="row">
        <div class="box-title">Risk Group</div>
        <div class="box-content risk">{{risk}}</div>
      </div>
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
        <div
          class="box-content"
          :class="last_device[0]!='-'?'device':''"
        >{{last_device[0]}}</div>
        <div class="box-subtitle">{{last_device[1]}}</div>
      </div>
      <div class="row">
        <div class="box-title">GCS</div>
        <div
          class="box-content"
          :class="last_gcs[0]!='-'?'gcs':''"
        >{{last_gcs[0]}}</div>
        <div class="box-subtitle">{{last_gcs[1]}}</div>
      </div>
    </div>
  </div>
</template>

<script>
/*eslint no-console: ["error", { allow: ["warn", "error","log"] }] */
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
    },
    last_news: function() {
      let vm = this;
      return vm.get_news(
        vm.last_bt[0],
        vm.last_hr[0],
        vm.last_sbp[0],
        vm.last_rr[0],
        vm.last_sat[0],
        vm.last_device[0],
        vm.last_gcs[0]
      );
    },
    delta: function() {
      let vm = this;
      let event_array = [];
      vm.patient.rr.forEach(function(e) {
        event_array.push({ field: "rr", ...e });
      });
      vm.patient.hr.forEach(function(e) {
        event_array.push({ field: "hr", ...e });
      });
      vm.patient.bt.forEach(function(e) {
        event_array.push({ field: "bt", ...e });
      });
      vm.patient.sbp.forEach(function(e) {
        event_array.push({ field: "sbp", ...e });
      });
      vm.patient.sat.forEach(function(e) {
        event_array.push({ field: "sat", ...e });
      });
      vm.patient.gcs.forEach(function(e) {
        event_array.push({ field: "gcs", ...e });
      });
      vm.patient.device.forEach(function(e) {
        event_array.push({ field: "device", ...e });
      });
      event_array.sort(function(a, b) {
        return a.datetime.localeCompare(b.datetime);
      });
      let min_news = -1;
      for (var i = 0; i < event_array.length; i++) {
        let vm = this;
        var current_time = event_array[i].datetime;
        var last_rr = vm.get_last_time_field(event_array, current_time, "rr");
        var last_hr = vm.get_last_time_field(event_array, current_time, "hr");
        var last_bt = vm.get_last_time_field(event_array, current_time, "bt");
        var last_sbp = vm.get_last_time_field(event_array, current_time, "sbp");
        var last_sat = vm.get_last_time_field(event_array, current_time, "sat");
        var last_device = vm.get_last_time_field(
          event_array,
          current_time,
          "device"
        );
        var last_gcs = vm.get_last_time_field(event_array, current_time, "gcs");
        var news = vm.get_news(
          last_bt,
          last_hr,
          last_sbp,
          last_rr,
          last_sat,
          last_device,
          last_gcs
        );
        // console.log(
        //   last_bt,
        //   last_hr,
        //   last_sbp,
        //   last_rr,
        //   last_sat,
        //   last_device,
        //   last_gcs,
        //   ">>",
        //   news
        // );
        if (
          min_news == -1 &&
          last_bt != "-" &&
          last_hr != "-" &&
          last_sbp != "-" &&
          last_rr != "-"
        ) {
          min_news = news;
        }
        if (
          news < min_news &&
          current_time != event_array[event_array.length - 1].datetime
        ) {
          min_news = news;
        }
      }
      let delta = vm.last_news - min_news;
      // console.log(event_array);
      // console.log(vm.last_news);
      // console.log("NEWS" + vm.last_news + "/" + min_news);
      if (delta > 0) {
        return "+" + delta;
      }
      return 0;
    },
    risk: function() {
      let vm = this;
      if (vm.last_news <= 5) {
        return "Low";
      } else if (vm.last_news <= 9) {
        return "Medium";
      } else if (vm.last_news <= 13) {
        return "High";
      }
      return "Critical";
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
        input_array.sort(function(a, b) {
          return a.datetime.localeCompare(b.datetime);
        });
        let last_element = input_array[input_array.length - 1];
        return [
          last_element.value,
          vm.datetime_formatter(last_element.datetime)
        ];
      }
    },
    get_last_time_field: function(event_array, current_time, field) {
      let filtered = event_array.filter(function(e) {
        return e.datetime.localeCompare(current_time) <= 0 && e.field == field;
      });
      if (filtered.length > 0) {
        return filtered[filtered.length - 1].value;
      }
      return "-";
    },
    get_score_bt: function(bt) {
      if (bt == "-") {
        return 0;
      }
      if (bt <= 35) {
        return 3;
      } else if (bt <= 36) {
        return 1;
      } else if (bt <= 38) {
        return 0;
      } else if (bt <= 39) {
        return 1;
      }
      return 2;
    },
    get_score_hr: function(hr) {
      if (hr == "-") {
        return 0;
      }
      if (hr <= 40) {
        return 3;
      } else if (hr <= 50) {
        return 1;
      } else if (hr <= 90) {
        return 0;
      } else if (hr <= 110) {
        return 1;
      } else if (hr < 130) {
        return 2;
      }
      return 3;
    },
    get_score_sbp: function(sbp) {
      if (sbp == "-") {
        return 0;
      }
      if (sbp <= 90) {
        return 3;
      } else if (sbp <= 100) {
        return 2;
      } else if (sbp <= 110) {
        return 1;
      } else if (sbp <= 219) {
        return 0;
      }
      return 3;
    },
    get_score_rr: function(rr) {
      if (rr == "-") {
        return 0;
      }
      if (rr <= 8) {
        return 3;
      } else if (rr <= 11) {
        return 1;
      } else if (rr <= 20) {
        return 0;
      } else if (rr <= 24) {
        return 2;
      }
      return 3;
    },
    get_score_sat: function(sat) {
      if (sat == "-") {
        return 0;
      }
      if (sat <= 91) {
        return 3;
      } else if (sat <= 93) {
        return 2;
      } else if (sat <= 95) {
        return 1;
      }
      return 0;
    },
    get_score_device: function(device) {
      if (device != "-") {
        return 2;
      }
      return 0;
    },
    get_score_gcs: function(gcs) {
      if (gcs == "-") {
        return 0;
      }
      if (gcs == "E4V5M6" || gcs == "E4VaM6") {
        return 0;
      }
      return 3;
    },
    get_news: function(bt, hr, sbp, rr, sat, device, gcs) {
      let vm = this;
      let result =
        vm.get_score_bt(bt) +
        vm.get_score_hr(hr) +
        vm.get_score_sbp(sbp) +
        vm.get_score_rr(rr) +
        vm.get_score_sat(sat) +
        vm.get_score_device(device) +
        vm.get_score_gcs(gcs);
      return result;
    }
  }
};
</script>

<style lang="scss" scoped>
.patient-card {
  font-size: 0.6rem;
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
    color: #777;
    .name {
      font-size: 1.2rem;
      font-weight: 900;
      margin-top: 3px;
      margin-bottom: 3px;
      color: #000;
    }
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
        font-size: 0.6rem;
        color: #555;
      }
      .box-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-top: 3px;
        height: 27px;
        font-size: 1rem;
        font-weight: 400;
        &.device {
          font-size: 0.6rem !important;
        }
        &.gcs {
          font-size: 0.6rem !important;
        }
        &.news {
          height: 33px;
          font-size: 1.4rem;
          font-weight: 900;
        }
        &.delta {
          height: 33px;
          font-size: 1rem;
          font-weight: 900;
        }
        &.risk {
          height: 33px;
          font-size: 1rem;
          font-weight: 900;
        }
      }
      .box-subtitle {
        font-size: 0.5rem;
        padding: 2px;
        color: #aaa;
        height: 11px;
      }
    }
  }
}
</style>
