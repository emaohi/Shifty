$(document).ready(function () {

    setTimeout(function () {
        $('.alert').hide()
    }, 3000);

    showNextWeekSlotsList();

    populateTimerDiv();

    populate_calendar();
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
    $('.selectpicker').selectpicker();
}

function populateTimerDiv() {
    if (deadline_date != "None") {
        $('#timerH').countdown(deadline_date, function (event) {
            $(this).html(event.strftime('Deadline in: '
                + '<span>%d</span> days, '
                + '<span>%H</span> hours, '
                + '<span>%M</span> minutes, '
                + '<span>%S</span> seconds ')
            );
        });
    } else {
        $('#timerH').text('Time for shift requests is over !');
    }
}

function populate_calendar() {
    $.ajax({
        url: current_shifts_url,
        type: "get",
        success: display_cal,
        error: function (xhr) {
            //Do Something to handle error
        }
    });
}

function display_cal(shifts_json) {
    shifts_json = JSON.parse(shifts_json);
    var r_list = [];
    for (var i = 0; i < shifts_json.length; i++) {
        r_list.push(JSON.parse(shifts_json[i]));
    }
    $('#calDiv').easycal({

        minTime: '06:00:00',
        maxTime: '23:59:00',
        timeGranularity: 30,
        slotDuration : 60,
        startDate : start_date,
        eventClick: function (shiftId) {
            console.log('cooooooool');
            showShiftDetails(shiftId);
        },
        events: r_list
    });
}

function showShiftDetails(shiftId) {
    $.ajax({
       url: shift_employees_url.slice(0, -1) + shiftId,
        type:"get",
        success: insertEmployeesToModal,
        error: function () {
            console.error('couldnt get employees of shift id ' + shiftId);
        }
    });
    $("#shiftModal").modal('show');
}

function insertEmployeesToModal(emp_list) {
    $("#shiftModalBody").html(emp_list);
}
