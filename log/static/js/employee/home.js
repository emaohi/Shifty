$(document).ready(function () {

    setTimeout(function () {
        $('.alert').hide()
    }, 3000);

    showNextWeekSlotsList();

    populateTimerDiv();

    populate_calendar();

    showSuggestions();

    getPreviousShifts();

});

$(document).on("click", "#toggleOld", function () {
    $(this).hide();
    ManagerMessagesAjax('false');
});

$(document).on("click", "#toggleClosed", function () {
    $(this).hide();
    swapRequestsAjax('closed');
});

$(document).on("click", ".swapBtn", function () {
    requestSwap($(this));
});

$(document).on("click", ".approve", function () {
    var request_id = $(this).parents('div').siblings("span:first").text();
    spin_instead_of_btn($(this));
    handle_request(true, request_id);
});

$(document).on("click", ".reject", function () {
    var request_id = $(this).parents('div').siblings("span:first").text();
    spin_instead_of_btn($(this));
    handle_request(false, request_id);
});

$(document).on('shown.bs.tab', 'a[href="#messages"]', function () {
    ManagerMessagesAjax('true');
});

$(document).on('shown.bs.tab', 'a[href="#swaps"]', function () {
    swapRequestsAjax('open');
});

function ManagerMessagesAjax(queryParam) {
    $.ajax({
        url: getManagerMessagesUrl,
        type: "get",
        data: {
            new: queryParam
        },
        success: function(res) {
            if (queryParam === 'true') {
                $("#newMessages").html(res);
                $("#msgsBadge").hide();
            } else {
                $("#oldMessages").html(res);
            }
        },
        error: function (xhr) {
            console.error("couldn't get manager messages");
        }
    });
}

function swapRequestsAjax(queryParam) {
    $.ajax({
        url: swapRequestsUrl,
        type: "get",
        data: {
            state: queryParam
        },
        success: function(res) {
            if (queryParam === 'open') {
                $("#openSwaps").html(res);
            } else {
                $("#closedSwaps").html(res);
            }
        },
        error: function (xhr) {
            console.error("couldn't get swap requests");
        }
    });
}

function showSuggestions() {
    console.log('first login: ' + first_login);
    if (first_login === 'True') {
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
        slotDuration: 60,
        startDate: start_date,
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
        type: "get",
        success: function (emp_list) {
            insertEmployeesToModal(emp_list, shiftId);
        },
        error: function () {
            console.error('couldnt get employees of shift id ' + shiftId);
        }
    });
    $("#shiftModal").modal('show');
}

function displaySwapRequests(swap_requests) {
    $("#openSwaps").html(swap_requests);
}

function insertEmployeesToModal(emp_list, shift_id) {
    $("input[name='shiftId']").val(shift_id);
    $("#shiftModalBody").html(emp_list);
}

function getPreviousShifts() {
    $.ajax({
        url: prev_shifts_url,
        type: "get",
        success: function (res) {
            $("#previous").html(res);
        },
        error: function (xhr) {
            if (xhr.status === 400) {
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

function sendSwapRequest(username, requestedShift, requesterShift) {
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
        error: notifySwapRequestFailed
    });
}

function notifySwapRequestDelivered() {
    var resultSpan = $("#swapRequestResult");
    resultSpan.addClass("success");
    resultSpan.text("success");
}
function notifySwapRequestFailed(xhr) {
    var resultSpan = $("#swapRequestResult");
    resultSpan.addClass("fail");
    if (xhr.status === 400) {
        resultSpan.text("Illegal request - request exists");
    } else {
        resultSpan.text("server error: " + xhr.responseText);
    }
}

function spin_instead_of_btn($btn) {
    $btn.hide();
    $btn.siblings("button").hide();
    $btn.siblings('.fa-spin').show();
}

function handle_request(is_accept, request_id) {
    $.ajax({
        url: handle_swap_request_url,
        type: "post", //send it through get method
        data: {
            emp_request_id: request_id,
            is_accept: is_accept
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            swapRequestsAjax('open');
        },
        error: function (xhr) {
            console.error(xhr.responseText)
        }
    });
}