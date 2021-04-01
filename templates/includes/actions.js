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

function removeMetricDiv(div_id){
    /*
    removes the given metric div
    by finding it by the div_id

    if there's less than 3, it returns an error
    since we need atleast 2 metrics to work with

    */

    goals = document.getElementsByClassName("metric_container");
    if(goals.length <= 2){

        toastr.error("No se puede remover mas metas, por defecto deben de existir 2")
    }
    else
    {
        goner = document.getElementById(div_id);
        goner.remove()

    }
}
// still needs some work
function generate_deleter(delete_id){

    var deleter = document.createElement('button')
    deleter.className="ion-trash-a metric_deleter btn btn-danger"
    deleter.setAttribute('id',delete_id)
    deleter.style.width='8px';
    deleter.style.marginTop="4px";
    deleter.style.marginLeft="-7px";
    deleter.style.fontSize="23px";
    deleter.addEventListener('onclick',function(){
    /*
    removes the given metric div
    by finding it by the div_id

    if there's less than 3, it returns an error
    since we need atleast 2 metrics to work with

    */

    goals = document.getElementsByClassName("metric_container");
    if(goals.length <= 2){

        toastr.error("No se puede remover mas metas, por defecto deben de existir 2")
    }
    else
    {
        alert(this);
//        goner = document.getElementById(div_id);
        this.parentNode.remove()

    }
});
    return deleter;
}

function AddMetricDiv(){

    /*
    clones the div for the exiting
    metrics so that it appends more items with
    the same properties
    returns: Null
    */

    var container_holder = document.getElementById('metrics_holder');
    var metrics = document.getElementsByClassName('metric_container');
    var last_metric = metrics[metrics.length-1];
    var new_metric = last_metric.cloneNode(true);
    var deleter = new_metric.getElementsByClassName('metric_deleter')[0]
    deleter.remove();
    var mtr_id = last_metric.getAttribute('id')
    var new_id = parseInt(mtr_id) + 1
    new_metric.setAttribute('id',`${new_id}`)
    var new_deleter = generate_deleter(`deleter_${new_id}`)
    console.log(`${this},${new_deleter},${new_deleter==this}`)
    new_metric.appendChild(new_deleter);
    container_holder.appendChild(new_metric.cloneNode(true));

}

function parse_values(array, dtype){
/*
    parses the values of the array or
    return null if there's an empty string or if
    the vale don't match the given datatype
*/
    final_values = []
    for(var i=0;i<array.length;i++){
            var value = (dtype=='str')?array[i].value: (parseFloat(array[i].value).toString()=='NaN')? null: parseFloat(array[i].value);

            if(value == '' || value== null)
            {
                return "No se puede procesar un valor vacio, por favor de llenar los campos."
            }
            final_values.push(value);
    }
    return final_values;

}

function collectFormData(update=false){
    /*
    collects all of the data
    and prepares it to be processed
    in a object
    */
    var class_suffix = (!update) ? '':'update_'
    var form_data = {};
    var error = ``;
    var descriptions = document.getElementsByClassName(`meta_description`);
    var goals  = document.getElementsByClassName(`meta_value`);
    var percentage_concecution = document.getElementsByClassName(`meta_consecution`);
    goals_values = [descriptions, goals, percentage_concecution]
    for(i=0;i<goals_values.length;i++)
    {
        gathered_data = parse_values(goals_values[i],'str')

        if (ist)


    }

}




function loadObjectiveList(){
  /*
    loads the list of objectives after being updated
    this is performed via ajax
  */
  var requester = new XMLHttpRequest();

}

function close_modal(modal_id){
$(`#${modal_id}`).modal('hide');

}

function createObjective()
{




}

function delete_record(unique_id){

    var sender = new XMLHttpRequest();
    var token = getCookie('authtoken');
    var payload = JSON.stringify({
    "authtoken":token
    })

    sender.open('POST','/delete_objective/'+unique_id+'/')
    var csrf = getCookie('csrftoken');
    sender.setRequestHeader('X-CSRFToken', csrf);
    sender.setRequestHeader("Content-Type", "application/JSON");
    sender.onload = function(){
        if(this.readyState == 4)
            {

                var response = JSON.parse(this.responseText);
                if(this.status == 200)
                {
                    toastr.success("El record ha sido borrado existosamente!!",'Success')
                    loadObjectiveList();
                    close_modal();


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
