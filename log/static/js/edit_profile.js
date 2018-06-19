/**
 * Created by rsegev on 29/06/2017.
 */
$(document).ready(function () {
    $.ajax({
        url: edit_profile_form_url, //from template
        type: "get", //send it through get method,
        success: form_success_callback,
        error: function (xhr) {
            //Do Something to handle error
        }
    });

    $('#form_here').on('click', '.btn-warning', function () {
        show_text_and_send_btn($(this));
    });
    $('#form_here').on('click', '.btn-info', function () {
        var field_name = $(this).prev().prev().attr('name');
        var fix_text = $(this).siblings('input[class="new_text"]').val();

        var curr_val = "";
        var $prevprev = $(this).prev().prev();

        if ($prevprev.is('input')) {
            curr_val = $prevprev.attr('value');
        } else if ($prevprev.is('select')) {
            curr_val = $prevprev.find(":selected").text();
        }
        report_incorrect($(this), field_name, fix_text, curr_val);
    });

    $("#theForm").submit(function () {
        console.log("selected are: " + JSON.stringify(instance.pickList('getSelected')));
        $("#id_preferred_shift_time_frames").val(JSON.stringify(instance.pickList('getSelected')));
    })
});


function show_text_and_send_btn($elem) {
    $elem.before('<input type="text" class="new_text" style="margin-left: 30px" placeholder="submit your fix">');
    $elem.addClass('btn-info').removeClass('btn-warning').text('send');
    $elem.after('<i class="fa fa-spinner fa-spin" style="font-size:18px; margin-left: 10px; display: none"></i>')
}

function form_success_callback(response) {
    $('#form_here').html(response);
    showMultiSelectList();

    $('input:disabled').after(
        '<button type="button" class="btn btn-warning btn-xs report-btn">' +
        'Incorrect?</button>');
    $('select:disabled').after(
        '<button type="button" class="btn btn-warning btn-xs report-btn">' +
        'Incorrect?</button><hr>');
}

function report_incorrect($btn, field, fix, curr_val) {
    var $spinner = $btn.siblings('.fa-spinner');
    $spinner.show();
    $.ajax({
        url: report_incorrect_url, //from template
        type: "post",
        data: {
            incorrect_field: field,
            fix_suggestion: fix,
            curr_val: curr_val
        },
        headers: {
            'X-CSRFToken': csrf_token //from template
        },
        success: function (response) {
            $btn.siblings('input[class="new_text"]').remove();
            $btn.after('<p style="display: inline; margin-left: 10px"> <b> ' + response + '</b> </p>');
            $btn.remove();
            $spinner.hide();

        },
        error: function (response) {
            $btn.siblings('input[class="new_text"]').remove();
            $btn.after('<p style="display: inline; margin-left: 10px"> <b> ' + response.responseText + '</b> </p>');
            $btn.remove();
            $spinner.hide();
        }
    });
}

function showMultiSelectList() {
    instance = $('#preferredTimesList').pickList({
        data: makeData()
    });
}
function makeData() {
    var data = {
        available: [
            {id: 1, label: "Sunday - first leg (08:00 - 15:00)"},
            {id: 2, label: "Sunday - second leg (15:00 - 22:00)"},
            {id: 3, label: "Monday - first leg (08:00 - 15:00)"},
            {id: 4, label: "Monday - second leg (15:00 - 22:00)"},
            {id: 5, label: "Tuesday - first leg (08:00 - 15:00)"},
            {id: 6, label: "Tuesday- second leg (15:00 - 22:00)"},
            {id: 7, label: "Wednesday - first leg (08:00 - 15:00)"},
            {id: 8, label: "Wednesday - second leg (15:00 - 22:00)"},
            {id: 9, label: "Thursday - first leg (08:00 - 15:00)"},
            {id: 10, label: "Thursday - second leg (15:00 - 22:00)"},
            {id: 11, label: "Friday - first leg (08:00 - 15:00)"},
            {id: 12, label: "Friday - second leg (15:00 - 22:00)"},
            {id: 13, label: "Saturday - first leg (08:00 - 15:00)"},
            {id: 14, label: "Saturday - second leg (15:00 - 22:00)"}
        ],
        selected: []
    };
    var currentPreferred = $("#id_preferred_shift_time_frames").val()
    if (currentPreferred) {
        var preferred_times = $.parseJSON(currentPreferred);
        for (var i = 0; i < preferred_times.length; i++) {
            for (var j = 0; j < data.available.length; j++){
                if (data['available'][j]['id'] === preferred_times[i]['id']) {
                    data['selected'].push(preferred_times[i]);
                    data['available'].splice(j, 1);
                }
            }
        }
    }
    return data;
}
var instance = null;