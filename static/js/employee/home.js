$(document).ready(function () {

    setTimeout(function () {
        $('.alert').hide()
    }, 3000);

    showNextWeekSlotsList();

});

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
