$(document).ready(function () {

    setTimeout(function () {
        $('.alert').hide()
    }, 3000);

    showNextWeekSlotsList();


});
// $(document).on('click', '.addToRequest', function () {
//     $(this).hide();
//     addToRequest($(this).parent().prev().text());
//     $(this).parent().parent().addClass("slot-selected");
// });
// $(document).on('click', '.removeFromRequest', function () {
//     var slotId = getSlotIdFromListItem($(this).parent().attr("id"));
//     restoreSlotPanel($("#panel_" + slotId));
//     $(this).parent().remove();
// });

function showNextWeekSlotsList() {
    $.ajax({
        url: next_slots_url, //from template
        type: "get", //send it through get method,
        success: displaySlotList,
        error: function (xhr) {
            console.error("couldn't get slots data");
        }
    });
}

function displaySlotList(slotsData) {
    $(".slotRows").html(slotsData);
}
//
// function addToRequest(slotText) {
//     $("#requestList").append('<li id="' + slotText + '" class="list-group-item">' + slotText +
//         '<button type="button" class="btn btn-xs btn-danger removeFromRequest pull-right">' +
//         '<span class="glyphicon glyphicon-minus"></span></button>' + '</li>');
// }
//
// function getSlotIdFromListItem(listItemId) {
//     return listItemId.split("- ")[1];
// }
//
// function restoreSlotPanel(panelToRestore) {
//     panelToRestore.find(".addToRequest").show();
//     panelToRestore.find(".panel-heading").removeClass("slot-selected");
// }
