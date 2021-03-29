function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function check_del(modal_name_id){
    alert(modal_name_id);
$('#'+modal_name_id).modal({
				show: true
			});
}


function forfeit_block (block_iter_id){
var sender = new XMLHttpRequest();
console.log(typeof(block))
var payload = JSON.stringify({"iter_id": block_iter_id})
sender.open('POST','forfeit_block')
var csrf = getCookie('csrftoken');
sender.setRequestHeader('X-CSRFToken', csrf);
sender.setRequestHeader("Content-Type", "application/JSON");
sender.onload = function(){
    if(this.readyState == 4)
        {
            var response = JSON.parse(this.responseText);
            if(this.status == 200)
            {
                toastr.success(response.msg,'success')
                block_refresh();
            }
            else
            {
               toastr.error(response.msg,'error')
            }

         }
}
sender.send(payload);

}


function change_bot_status(prov_url)
    {
        $.ajax
        (
            {
              url: prov_url,
              data: {'redirect_url': window.location.href},
              type: "POST",
              headers:{'X-CSRFToken':getCookie('csrftoken')},
              dataType: 'json',
              success: function(data)
              {
               window.location = data.redirect_url;

              },
              error:function(data)
                 {
                  toastr.error(data);
                }

            }
        );
    };

window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-23581568-13');



function generate_pdf(invoice_name)
{
/* this function takes a div and generates a pdf with it
since the pdf is going to be generated from the listing page
we need to load the pdf with AJAX.
*/

var doc = new jsPDF();
var elementHTML = $('#contnet').html();
var specialElementHandlers = {
    '#elementH': function (element, renderer) {
        return true;
    }
};
doc.fromHTML(elementHTML, 15, 15, {
    'width': 170,
    'elementHandlers': specialElementHandlers
});

// Save the PDF
doc.save(invoice_name+'.pdf');


}

function load_form()
    {
        $.ajax
        (
            {
              url: 'refresh_accepted_blocks',
              data: {},
              type: "GET",
              dataType: 'json',
              success: function(data){$('#block-list').html(data.block_list);
//              console.log(data.block_list);
                                     }
            }
        );
    };
    function selected_loaded(sel)
    {
        var load_value = document.getElementById("invoice_price");
        $.ajax(
            {
                  url: 'load_invoice_amount',
                  data: {'id':sel.options[sel.selectedIndex].value},
                  type: "GET",
                  dataType: 'json',
                  success: function(data){

                                        load_value.value=data.invoice_amount;
                                         }
             }

        )


    }