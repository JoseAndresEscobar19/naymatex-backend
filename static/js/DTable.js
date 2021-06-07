function init_datatable(id) {
    $("#"+id).DataTable({
        "columnDefs": [
            { "orderable": false, "targets": -1 }
            ],
        orderCellsTop: true,
        fixedHeader: true,
        width: "100%",
        "language": {
            "lengthMenu": "Mostrando _MENU_ registros por página",
            "zeroRecords": "No se obtuvieron resultados",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "No hay información disponible",
            "infoFiltered": "(filtrado de _MAX_ registros en total)",
            "search": "Buscar",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            },
        }
    })
};
