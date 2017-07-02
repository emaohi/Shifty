/**
 * Created by rsegev on 29/06/2017.
 */
$(document).ready(function () {
  $.ajax({
      url: "{% url 'edit_profile_form' %}",
      type: "get", //send it through get method,
      success: form_success_callback,
      error: function(xhr) {
        //Do Something to handle error
      }
  });

  $('#form_here').on('click', '.btn-warning', function() {
      show_text_and_send_btn($(this));
  });
  $('#form_here').on('click', '.btn-info', function() {
      var field_name = $(this).prev().prev().attr('name');
      var fix_text = $(this).siblings('input[class="new_text"]').val();

      var curr_val = "";
      var $prevprev = $(this).prev().prev();

      if ($prevprev.is('input')){
          curr_val = $prevprev.attr('value');
      }else if ($prevprev.is('select')){
          curr_val = $prevprev.find(":selected").text();;
      }
      report_incorrect($(this), field_name, fix_text, curr_val);
  });
});

function show_text_and_send_btn($elem) {
    $elem.before('<input type="text" class="new_text" style="margin-left: 30px" placeholder="submit your fix">');
    $elem.addClass('btn-info').removeClass('btn-warning').text('send');
    $elem.after('<i class="fa fa-spinner fa-spin" style="font-size:18px; margin-left: 10px; display: none"></i>')
}

function form_success_callback(response) {
                $('#form_here').html(response);

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
      url: "{% url 'report_incorrect' %}",
      type: "post", //send it through get method
      data: {
        incorrect_field: field,
        fix_suggestion: fix,
        curr_val: curr_val
      },
      headers: {
          'X-CSRFToken': '{{ csrf_token }}'
      },
      success: function(response){
                $btn.siblings('input[class="new_text"]').remove();
                $btn.after('<p style="display: inline; margin-left: 10px"> <b> '+ response + '</b> </p>');
                $btn.remove();
                $spinner.hide();

            }
    });
}
