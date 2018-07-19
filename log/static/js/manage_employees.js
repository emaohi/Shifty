/**
 * Created by rsegev on 02/07/2017.
 */

$(document).ready(function () {

    // $('.table-striped').paging({limit:5});

    var curr_modal_username = "";

    handle_manager_row();

    $('.btn-danger').click(function () {
        curr_modal_username = $(this).parents('td').siblings(":first").text();
        show_delete_modal(curr_modal_username);
    });
    $('.btn-primary').click(function () {
        curr_modal_username = $(this).parents('td').siblings(":first").text();
        show_edit_modal(curr_modal_username);
    });

    $('#del_btn').click(function () {
        del_user(curr_modal_username);
    });

    $('#broadcast_button').click(function () {
        show_broadcast_modal();
    });

    $('.btn-submit').on('click', function() {
        $('.btn-submit').hide();
        $('.progress').show();
        setTimeout(doProgress, 200);
    });
});

function handle_manager_row() {
    var $manager_row  = $('.manager-cell').parents('tr');
    $manager_row.css('background-color', 'lightgreen');
    $manager_row.find('.btn-xs').hide();
}

function show_edit_modal(username) {
    $.ajax({
      url: edit_profile_form_url,
      type: "get", //send it through get method
      data: {
        username: username
      },
      success: function(response) {
                    $('#edit').find('.modal-body').html(response);
                    $('#edit').find('#Heading').html('Edit ' + username + ' details');
                    $('#edit').modal('show');
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

function show_delete_modal(username){
    $('#delete').find('h4').text("Delete " + username + " from your business");
    $('#delete').modal('show');
}

function show_broadcast_modal(username) {
    $.ajax({
      url: broadcast_msg_url,
      type: "get", //send it through get method
      data: {
      },
      success: function(response) {
                    $('#broadcast').find('.modal-body').html(response);
                    $('#broadcast').find('#Heading').html('Broadcast message to all your employees');
                    $('#broadcast').modal('show');
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

function del_user(username) {
    $.ajax({
      url: delete_user_url,
      type: "post", //send it through get method
      data: {
        username: username
      },
      headers: {
          'X-CSRFToken': csrf_token
      },
      success: function(response){
                window.location.reload();
            }
    });
}
function doProgress() {
    var employeeIndex = employees_length;
    var i = 0;
    var counterBack = setInterval(function(){
      i++;
      if (i <= 100){
        $('.progress-bar').css('width', i+'%');
      } else {
        clearInterval(counterBack);
      }
      var is_plural_mail;
      if (employeeIndex > 0){
          is_plural_mail = "messages";
      }else{
          is_plural_mail = "message";
      }
      $("#percent").text((employeeIndex) + " " + is_plural_mail);

    }, (employeeIndex+1) * 10);

}