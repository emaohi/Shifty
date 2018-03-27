$(document).ready(function () {

    setTimeout(function () {
        $('.alert').hide()
    }, 3000);

    getSlotsStatus(); // this will whether populate or not the next week div
    populateTimerDiv();

    if (location.hash) {
        $("a[href='" + location.hash + "']").tab("show");
    }
    $.ajax({
        url: next_slots_url, //from template
        type: "get", //send it through get method,
        success: display_cal,
        error: function (xhr) {
            //Do Something to handle error
        }
    });

    populate_current_calendar();


    $('.edit-slot').click(function () {
        var shiftId = $('#putShiftId').text();
        window.location.href = getUpdateShiftUrl(shiftId);
    });

    $('.remove-slot').click(function () {
        var shiftId = $('#putShiftId').text();
        deleteSlot(shiftId);
    });

    $('.generateBtn').click(function () {
        generate_shifts();
    });

    $(document.body).on("click", "a[data-toggle]", function (event) {
        location.hash = this.getAttribute("href");
    });

    $('.approve').click(function () {
        var request_id = $(this).parents('div').siblings("span:first").text();
        spin_instead_of_btn($(this));
        handle_request("A", request_id);
    });
    $('.reject').click(function () {
        var request_id = $(this).parents('div').siblings("span:first").text();
        spin_instead_of_btn($(this));
        handle_request("R", request_id);
    });

    $('#finishSlots').click(function () {
        updateFinishedSlots(true);
    });

    $('#resetSlots').click(function () {
        updateFinishedSlots(false);
    });
});
$(window).on("popstate", function () {
    var anchor = location.hash || $("a[data-toggle='tab']").first().attr("href");
    $("a[href='" + anchor + "']").tab("show");
});

function populate_current_calendar() {
    $.ajax({
        url: current_shifts_url,
        type: "get",
        success: display_current_cal,
        error: function (xhr) {
            //Do Something to handle error
        }
    });
}

function updateFinishedSlots(isFinished) {
    $.ajax({
        url: finish_slots_url, //from template
        type: "post", //send it through get method,
        data: {
            isFinished: isFinished
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: getSlotsStatus,
        error: function (xhr) {
            alert("something fishy: " + xhr);
        }
    });
}

function updateShiftSummaryForm(slotId) {
    $.ajax({
        url: summary_url.slice(0, -1) + slotId,
        type: "get",
        success: setSummaryForm,
        error: function (xhr) {
            console.warn(xhr.responseText);
            var summaryTab =  $('a[href="#shiftSummaryTab"]');
            if (!summaryTab.hasClass("disabledbutton")) {
                summaryTab.addClass("disabledbutton");
            }
        }
    });
}

function setSummaryForm(formResponse) {
    $('a[href="#shiftSummaryTab"]').removeClass("disabledbutton");
    $("#shiftSummaryTab").html(formResponse);
}

function getSlotsStatus() {
    $.ajax({
        url: finish_slots_url, //from template
        type: "get",
        success: finishSlots,
        error: function (xhr) {
            alert("something fishy: " + xhr);
        }
    });
}

function generate_shifts() {
    $.ajax({
        url: generate_shifts_url, //from template
        type: "post",
        data: {},
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function () {
            location.reload();
        },
        error: function () {
            location.reload();
        }
    });
}

function finishSlots(isFinished) {
    if (shifts_generated === '0') {
        if (isFinished === 'True') {
            $('#calDiv').addClass("disabledbutton");
            $('#finishSlots').hide();
            $('#slotMsg').show();
        } else {
            $('#calDiv').removeClass("disabledbutton");
            $('#finishSlots').show();
            $('#slotMsg').hide();
        }
    }
    else {
        $('#slotMsg').hide();
        $('#notFinished').hide();
        $('#afterGeneration').show();
    }
}

function spin_instead_of_btn($btn) {
    $btn.hide();
    $btn.siblings("button").hide();
    $btn.siblings('.fa-spin').show();
}

function handle_request(new_status, request_id) {
    $.ajax({
        url: handle_emp_request_url,
        type: "post", //send it through get method
        data: {
            emp_request_id: request_id,
            new_status: new_status
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            window.location.reload();
        }
    });
}

function deleteSlot(shiftId) {
    $.ajax({
        url: delete_slot_url,
        type: "post", //send it through get method
        data: {
            slot_id: shiftId
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            window.location.reload();
        }
    });
}

function display_cal(event_list) {
    var id_to_constraint_json = JSON.parse(event_list.pop());

    var r_list = [];
    for (var i = 0; i < event_list.length; i++) {
        r_list.push(JSON.parse(event_list[i]));
    }

    $('#calDiv').easycal({

        minTime: '06:00:00',
        maxTime: '23:59:00',
        timeGranularity: 30,
        slotDuration: 60,
        startDate: start_date,
        dayClick: function (el, startTime) {
            var dateStr = el.parent().attr('data-date');
            var d = toDate(dateStr);
            window.location.href = getNewShiftUrl(d.getDay(), startTime);
        },
        eventClick: function (shiftId) {
            showSlotDetails(shiftId, JSON.parse(id_to_constraint_json[shiftId]));
        },
        events: r_list
    });
}

function showSlotDetails(slotId, constraints_json) {

    var slotModal = $('#slotModal');

    $('#constraintTab').html(listifyConstraintJson(constraints_json));
    slotModal.find('.modal-title').html('Slot #' + slotId + ' constraints');

    setSlotEmpList(slotId);
    setShiftEmpList(slotId);

    $('#putShiftId').text(slotId);
    slotModal.modal('show');
}
function setSlotEmpList(slotId) {
    $.ajax({
        url: slot_request_employees.slice(0, -1) + slotId, //from template
        type: "get", //send it through get method,
        success: function (res) {
            $("#empsTab").html(res);
        },
        error: function (err) {
            $("#empsTab").html(err.responseText);
        }
    });
}

function setShiftEmpList(slotId) {
    $.ajax({
        url: slot_employees.slice(0, -1) + slotId, //from template
        type: "get", //send it through get method,
        success: function (res) {
            $("#nextShiftEmpsTab").html(res);
        },
        error: function (err) {
            $("#empsTab").html(err);
        }
    });
}

function listifyConstraintJson(constraints_json) {

    console.log(constraints_json);

    var $div = '<div class="container">';
    $div += '<div class="row">';
    $div += '<div class=col-md-8>';
    $.each(constraints_json, function (role, constraints) {
        var $roleDiv = '<div>';
        $roleDiv += '<h3>' + role + ' - ' + constraints.num + ' employee/s' + '</h3>';
        var $conList = '<ul class="list-group">';
        $.each(constraints, function (field, field_json) {
            if (field != 'num') {
                $conList += '<li class="list-group-item">' + make_sentence(field, field_json) + '</li>';
            }
        });
        $conList += '</ul>';

        $roleDiv += $conList + '<hr>' + '</div>';

        $div += $roleDiv;
    });
    $div += '</div></div></div>';
    return $div;
}

function make_sentence(field, field_json) {
    var sentence_dict = {'lte': 'less than ', 'gte': 'more than ', 'eq': 'equals to '};
    var gender_dict = {'M': 'Male', 'F': 'Female'};
    var val = '';
    if (field != 'gender') {
        val = field_json['val'];
    } else {
        val = gender_dict[field_json['val']];
    }
    return 'The ' + field + ' of at least ' + field_json['apply_on'] + ' employees needs to be ' +
        sentence_dict[field_json['op']] + val;
}

function getNewShiftUrl(day, startTime) {
    var params = {"day": day + 1, "startTime": startTime.replace(/:/g, "-")};
    return new_slot_url + "?" + $.param(params);
}

function getUpdateShiftUrl(id) {
    return update_slot_url.replace(/\/[^\/]*$/, '/' + id);
}

function toDate(dateStr) {
    var parts = dateStr.split("-");
    return new Date(parts[2], parts[1] - 1, parts[0]);
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

function display_current_cal(shifts_json) {
    shifts_json = JSON.parse(shifts_json);
    var r_list = [];
    for (var i = 0; i < shifts_json.length; i++) {
        r_list.push(JSON.parse(shifts_json[i]));
    }
    $('#currentCalDiv').easycal({

        minTime: '06:00:00',
        maxTime: '23:59:00',
        timeGranularity: 30,
        slotDuration: 60,
        startDate: current_start_date,
        eventClick: function (shiftId) {
            showShiftDetails(shiftId);
            updateShiftSummaryForm(shiftId);
        },
        events: r_list
    });
}

function showShiftDetails(shiftId) {
    $.ajax({
        url: slot_employees.slice(0, -1) + shiftId,
        type: "get",
        success: insertEmployeesToModal,
        error: function () {
            console.error('couldnt get employees of shift id ' + shiftId);
        }
    });
    $("#shiftModal").modal('show');
}

function insertEmployeesToModal(emp_list) {
    $("#shiftEmpsTab").html(emp_list);
}