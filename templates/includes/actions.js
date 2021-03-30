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


function AddMetricDiv(){

/*
clones the div for the exiting
metrics so that it appends more items with
the same properties
returns: Null
*/

    var container_holder = document.getElemetById('metrics_holder');
    var metrics = document.getElementsByClassName('metric_container');
    var last_metric = metrics[metrics.length-1];
    var metric_div = document.createElement('div');
    metric_div.setAttribute('class','metric_container');
    metric_div.setAttribute('id',`metric_${metrics.length+1}`);
    var description = document.createElement('input');
    var metric = document.createElement('input');
    var concecution = document.createElement('input');
    concecution.setAttribute('placeholder',"% de concecucion")

    var delete_btn = document.getElementsByClassName('metric_deleter');

}


function removeMetricDiv(div_id){
    /*
    removes the given metric div
    by finding it by the div_id

    if there's less than 3, it returns an error
    since we need atleast 2 metrics to work with

    */
}


function collectFormData(){
    /*
    collects all of the data
    and prepares it to be processed
    in a object
    */

}


function removeObjective(objective_id){
  /*
    removes the given objective
    this is done by sending a ajax request
  */


}


function loadObjectiveList(){
  /*
    loads the list of objectives after being updated
    this is performed via ajax
  */

}



function delete_record(option, unique_id){

    var sender = new XMLHttpRequest();
    var payload = JSON.stringify({'option':option,
    "unique_id":unique_id
    })

    sender.open('POST','/admintr/auth/delete_record/'+unique_id+'/'+option)
    var csrf = getCookie('csrftoken');
    sender.setRequestHeader('X-CSRFToken', csrf);
    sender.setRequestHeader("Content-Type", "application/JSON");
    sender.onload = function(){
        if(this.readyState == 4)
            {

                var response = JSON.parse(this.responseText);
                if(this.status == 200)
                {
//                    toastr.success("The record was successfully deleted",'Success')
                    console.log(response.redirect_url);
                    window.location.href = response.redirect_url
                }

                else
                {
                   toastr.error(response.error,'Error');

                }

             }
    }
    sender.send(payload);
}


function get_page(model_name, page_number, per_page, detail_id=null)
{
    var sender = new XMLHttpRequest();
    var payload = JSON.stringify({'model_name':model_name,
    'page_number':page_number,
    'per_page':per_page,
    'detail_id': detail_id
    })

    sender.open('POST','/paginate')
    list_name = 'paginate_list'+'_'+model_name;
    var csrf = getCookie('csrftoken');
    sender.setRequestHeader('X-CSRFToken', csrf);
    sender.setRequestHeader("Content-Type", "application/JSON");

    sender.onload = function(){
        if(this.readyState == 4)
            {

                var response = JSON.parse(this.responseText);
                if(this.status == 200)
                {
//                    console.log(list_name);
                    page = document.getElementById(list_name);
                    page.innerHTML=response.page;

                }

                else
                {
                   toastr.error(response.error,'Error');

                }

             }
    }
    sender.send(payload);

}
