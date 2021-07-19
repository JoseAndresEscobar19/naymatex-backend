function init_datatable(id) {
  $("#" + id).DataTable({
    // columnDefs: [{ orderable: false }],
    ordering: false,
    fixedHeader: true,
    width: "100%",
    language: {
      lengthMenu: "Mostrando _MENU_ registros por página",
      zeroRecords: "No se obtuvieron resultados",
      info: "Mostrando página _PAGE_ de _PAGES_",
      infoEmpty: "No hay información disponible",
      infoFiltered: "(filtrado de _MAX_ registros en total)",
      search: "Buscar",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior",
      },
    },
  });
}
function init_pagination(num_pages, current_page) {
  $(".pagination").twbsPagination({
    totalPages: num_pages,
    visiblePages: 10,
    startPage: current_page,
    href: true,
    pageVariable: "page",
    first: null,
    last: null,
    prev: "Anterior",
    next: "Siguiente",
  });
}
