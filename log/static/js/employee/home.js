$(document).ready(function () {

    setTimeout(function () {
        $('.alert').hide()
    }, 3000);

    showNextWeekSlotsList();

    populateTimerDiv();

    populate_calendar();

    showSuggestions();

    getPreviousShifts();

    $("#toggleOld").click(function () {
        var oldMsgs = $("#oldMsgs");
        if (oldMsgs.is(":visible")) {
            oldMsgs.hide();
            $(this).text('Show Old');
        } else {
            oldMsgs.show();
            $(this).text('Hide Old');
        }
    });

    if (sessionStorage.getItem("alreadyReset") !== null && new_messages > 0) {
        console.log("got new message, removing storage flag");
        sessionStorage.removeItem("alreadyReset");
    }
});

$(document).on("click", ".swapBtn", function () {
    requestSwap($(this));
});

$(document).on( 'shown.bs.tab', 'a[href="#messages"]', function (e) {
    if (sessionStorage.getItem("alreadyReset") === null) {
        console.log("going to reset new messages tab...");
        $.ajax({
            url: resetNewMessagesUrl,
            type: "post",
            data: {},
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: resetSuccess,
            error: function (xhr) {
                console.error("couldn't reset new messages");
            }
        });
    }
});

function showSuggestions() {
    console.log('first login: ' + first_login);
    if (first_login == 'True') {
        $("#suggestionsModal").modal('show');
    }
}

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

function resetSuccess() {
    sessionStorage.setItem("alreadyReset", "True");
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
        success: function(emp_list) {
            insertEmployeesToModal(emp_list, shiftId);
        },
        error: function () {
            console.error('couldnt get employees of shift id ' + shiftId);
        }
    });
    $("#shiftModal").modal('show');
}

function insertEmployeesToModal(emp_list, shift_id) {
    $("input[name='shiftId']").val(shift_id);
    $("#shiftModalBody").html(emp_list);
}

function getPreviousShifts() {
    $.ajax({
        url: prev_shifts_url,
        type:"get",
        success: function (res) {
            $("#previous").html(res);
        },
        error: function (xhr) {
            if (xhr.status === 400){
                $("#previous").html("<h3>No previous shifts...</h3>");
            } else {
                $("#previous").html("<h3>Server error trying to get previous shifts...</h3>");
                console.error('No previous shifts...');
            }
        }
    });
}

function requestSwap(btn) {
    var s = btn.siblings('select');
    var requesterShiftId = s.children('option').filter(':selected').val();
    var requestedShiftId = $("input[name='shiftId']").val();
    var requestedSwapUsername = btn.parent().siblings('span.username').text();
    sendSwapRequest(requestedSwapUsername, requestedShiftId, requesterShiftId);
}

function sendSwapRequest(username, requestedShift, requesterShift){
   $.ajax({
        url: swapRequstUrl, //from template
        type: "post", //send it through get method,
        data: {
            requested_employee: username,
            requester_shift: requesterShift,
            requested_shift: requestedShift
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: notifySwapRequestDelivered,
        error: function (xhr) {
            alert("something fishy: " + xhr);
        }
    });
}

function notifySwapRequestDelivered() {
    alert("success!");
}