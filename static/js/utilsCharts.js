var chart_ventas = create_chart("ventas-semana");
var chart_dinero = create_chart("dinero-semana");

var config = {
  autoUpdateInput: false,
  locale: {
    format: "DD/MM/YYYY",
    separator: " - ",
    applyLabel: "Aceptar",
    cancelLabel: "Cancelar",
    fromLabel: "Desde",
    toLabel: "Hasta",
    weekLabel: "Sem",
    daysOfWeek: ["DO", "LU", "MA", "MI", "JU", "VI", "SA"],
    monthNames: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    firstDay: 1,
  },
  maxSpan: {
    days: 6,
  },
};

function create_chart(id_canvas) {
  var ctx = document.getElementById(id_canvas).getContext("2d");
  var chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [],
      datasets: [
        {
          label: "-------",
          data: [],
          backgroundColor: ["rgba(255, 99, 132, 0.2)"],
          borderColor: ["rgba(255, 99, 132, 1)"],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
  return chart;
}

function _init_daterange() {
  $("#id_fecha_ventas").daterangepicker(config, function (start, end, label) {
    console.log(start, end);
    filtro_ventas(start.format("YYYY-MM-DD"), end.format("YYYY-MM-DD"));
  });

  $("#id_fecha_dinero").daterangepicker(config, function (start, end, label) {
    filtro_dinero(start.format("YYYY-MM-DD"), end.format("YYYY-MM-DD"));
  });

  $(".daterange").on("apply.daterangepicker", function (ev, picker) {
    if (picker) {
      $(this).val(picker.startDate.format("DD/MM/YYY") + " - " + picker.endDate.format("DD/MM/YYYY"));
    }
  });

  $(".daterange").on("cancel.daterangepicker", function (ev, picker) {
    $(this).val("").trigger("apply.daterangepicker");
  });
}

function filtro_ventas(start, end) {
  $.ajax({
    url: $("#id_fecha_ventas").data("url"),
    data: {
      fecha_inicio: start,
      fecha_fin: end,
    },
  }).always(function (res) {
    if (res.status == 200) {
      $("#cantidad_ventas").text(res.data.ventas_rango);
      chart_ventas.data = res.data.data_chart;
      chart_ventas.update();
    } else {
      console.error(res.data);
    }
  });
}

function filtro_dinero(start, end) {
  $.ajax({
    url: $("#id_fecha_dinero").data("url"),
    data: {
      fecha_inicio: start,
      fecha_fin: end,
    },
  }).always(function (res) {
    if (res.status == 200) {
      $("#cantidad_dinero").text(res.data.dinero_rango);
      chart_dinero.data = res.data.data_chart;
      chart_dinero.update();
    } else {
      console.error(res.data);
    }
  });
}

function _init_() {
  _init_daterange();
  filtro_ventas("", "");
  filtro_dinero("", "");
}

$(document).ready(_init_);
