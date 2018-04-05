$(document).ready(function () {

    $('.attach-con').after(
        '<button type="button" class="btn btn-warning btn-sm report-btn">' +
        'Add constraints</button>');

    $('.btn-warning').click(function () {
        var $btnClicked = $(this);
        var curr_modal_role = getRoleBtn($btnClicked);
        hideNotRoleFields(curr_modal_role);

        var maxNumEmp = getMaxEmpNum($btnClicked);
        limit_apply_on(curr_modal_role, maxNumEmp);

        var $constraintModal = $('#constraintModal');
        $constraintModal.find('#Heading').html(curr_modal_role + ' constraints');
        $constraintModal.modal('show');
    });

    $('#removeModalFields').click(function () {
        var all_form_fields = $('[form="theForm"]');
        all_form_fields.each(function () {
            if($(this).attr('name').includes('__')){
                $(this).val("");
            }
        })
    });

    $("#savedBtn").click(function () {
        $("#savedShiftDiv").show();
        $("#customShiftDiv").hide();

        $("#submitSlot").show();
    });
    $("#customBtn").click(function () {
        $("#customShiftDiv").show();
        $("#savedShiftDiv").hide();

        $("#submitSlot").show();
    });

    $('#id_save_as').keyup(function(e) {
        clearTimeout($.data(this, 'timer'));
        $('#saveSlotExistWarning').hide();
        $(this).data('timer', setTimeout(search, 500));
    });
});

function getRoleBtn($btnClicked) {
    var btn_sibling_input_name = $btnClicked.siblings("label").text();
    var text_parts = btn_sibling_input_name.split(" ");
    var role_plural = text_parts[2];
    return role_plural.substring(0, role_plural.length - 1);
}

function getMaxEmpNum($btnClicked) {
    return $btnClicked.siblings("input").val();
}

function hideNotRoleFields(roleNotToHide) {
    var all_form_fields = $('[form="theForm"]');
    all_form_fields.each(function () {
        if(!$(this).attr('name').includes(roleNotToHide) && $(this).attr('name').includes('__')){
            $(this).hide();
        }else{
            $(this).show();
        }
    })
}
function limit_apply_on(curr_modal_role, maxNumEmp) {
    var all_modal_fields = $('[form="theForm"]');
    all_modal_fields.each(function () {
        if($(this).attr('name').includes(curr_modal_role) && $(this).attr('name').includes('apply')){
            $(this).attr({
                "max" : maxNumEmp
            });
        }
    })
}


function search() {
    var existingString = $("#id_save_as").val();
    if (existingString.length < 3) {
        console.log("less than 3 chars...");
        return;
    }
    console.log('trying to find savedSlot with name ' + existingString);
    $.ajax({
        url: existingSavedSlotsUrl.slice(0, -2) + existingString,
        type: "get",
        success: function(res) {
            var $savedSlotExist = $('#saveSlotExistWarning');
            $savedSlotExist.html("Slot with name " + existingString + " already exists, saving will override...");
            $savedSlotExist.show();
        },
        error: function (xhr) {
            console.log('no existing saved slot with this name, can continue...');
        }
    });
}
