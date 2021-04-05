toastr.options = {
  "closeButton": true,
  "debug": false,
  "newestOnTop": false,
  "progressBar": true,
  "positionClass": "toast-top-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "2000",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}
holder = {objective:null,}

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

    var deleter = document.createElement('i')
    deleter.className="ion-trash-a metric_deleter"
    deleter.setAttribute('id',delete_id)
    deleter.style.width='8px';
    deleter.style.marginTop="4px";
    deleter.style.marginLeft="-7px";
    deleter.style.fontSize="23px";
    return deleter;
}

function AddMetricDiv(num=1){

    /*
    clones the div for the exiting
    metrics so that it appends more items with
    the same properties
    returns: Null
    */
    if (num >= 1 ){
        for (i=0; i<num; i++){
            var container_holder = document.getElementById('metrics_holder');
            var metrics = document.getElementsByClassName('metric_container');
            var last_metric = metrics[metrics.length-1];
            var new_metric = last_metric.cloneNode(true);
            var deleter = new_metric.getElementsByClassName('metric_deleter')[0]
            deleter.remove();
            var mtr_id = last_metric.getAttribute('id')
            var new_id = parseInt(mtr_id) + 1
            new_metric.setAttribute('id',`${new_id}`)
            inputs = new_metric.getElementsByTagName('input')
            for (i=0;i<inputs.length;i++){

            inputs[i].value="";
            }
            var new_deleter = generate_deleter(`deleter_${new_id}`)
        //    console.log(`${this},${new_deleter},${new_deleter==this}`)
            new_metric.appendChild(new_deleter);
            container_holder.appendChild(new_metric.cloneNode(true));
            new_deleter.addEventListener('onclick',function(){
            /*
            removes the given metric div
            by finding it by the div_id

            if there's less than 3, it returns an error
            since we need atleast 2 metrics to work with

            */
            alert('executing before calling it....')
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



    }

    }

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

            if(value == '' || value == null)
            {
                return "No se puede procesar un valor vacio, por favor de llenar los campos."
            }
            final_values.push(value);
    }
    return final_values;

}

function cleanForm(){
    var containers = document.getElementsByClassName('metric_container');
    var descriptions = document.getElementsByClassName(`meta_description`);
    var goals  = document.getElementsByClassName(`meta_value`);
    var percentage_concecution = document.getElementsByClassName(`meta_consecution`);
    goals_values = [descriptions, goals, percentage_concecution]
    for(i=0;i<containers.length;i++)
    {
        if(containers.length > 2)
        {
            containers[i].remove();
        }

    }


    for(i=0;i<goals_values.length;i++)
    {
        for(j=0;j<goals_values[i].length;j++){
            goals_values[i][j].value="";

        }

    }

    document.getElementById('id_metrica').value="";
    document.getElementById('id_descripcion').value="";
//    document.getElementById('id_valor_de_acceptacion').value="";
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
    var passed = true;
    var descriptions = document.getElementsByClassName(`meta_description`);
    var goalx  = document.getElementsByClassName(`meta_value`);
    var percentage_concecution = document.getElementsByClassName(`meta_consecution`);
    goals_values = [parse_values(descriptions, 'str'), parse_values(goalx, 'str'),
                    parse_values(percentage_concecution, 'str')]
    form_data.objectivegoal_set = []
    d = parse_values(descriptions, 'str')
    g = parse_values(goalx, 'str')
    pc = parse_values(percentage_concecution, 'str')
    for(i=0;i<goalx.length;i++)
    {
         if (typeof(d)==typeof('')||typeof(g)==typeof('')||typeof(pc)==typeof(''))
        {
            toastr.error(`${(typeof(d)==typeof(''))?d:(typeof(g)==typeof(''))?g:(typeof(pc)==typeof(''))?pc:"Hbo un error con su procesamiento, debe pasar valores en cada campo"}`,'Error');
            passed=false;
            break;
        }

        else{
            form_data.objectivegoal_set.push({description:d[i],
                                              goal: g[i],
                                              consecution_percentage:pc[i]})

        }

    }
    if(passed)
    {
        form_data.metric=document.getElementById('id_metrica').value
        form_data.description=document.getElementById('id_descripcion').value
//        form_data.new_x=document.getElementById('id_valor_de_acceptacion').value

        if(form_data.metric!=''&&form_data.description!='')
        {
            return form_data;
        }
        else{
            toastr.error("No se puede procesar un valor vacio, por favor de llenar los campos.")
        }
    }

}




function loadObjectiveList(){
  /*
    loads the list of objectives after being updated
    this is performed via ajax
  */
   var sender = new XMLHttpRequest();
    sender.open('GET','/api/handle_objectives/');
    var token = getCookie('authtoken');
    var csrf = getCookie('csrftoken');
    sender.setRequestHeader('X-CSRFToken', csrf);
    sender.setRequestHeader("Authorization",`Token ${token}`);
    sender.setRequestHeader("Content-Type", "application/JSON");
    sender.onload = function(){
        if(this.readyState == 4)
            {

                var response = JSON.parse(this.responseText);
                if(this.status == 200)
                {
                   document.getElementById('rest_list_container').innerHTML=response.objective_list;
                }

                else
                {
                   toastr.error(response.error, 'Error');

                }

             }
    }
    sender.send();

}


function close_my_modal(modal_id){
    if(modal_id=='action_form'){cleanForm();}
    $(`#${modal_id}`).modal('hide');
}


function handleObjective()
{
 var sender = new XMLHttpRequest();
    var token = getCookie('authtoken');
    var objective_data = collectFormData();
    if (holder.objective != null){
        objective_data.objective_id=holder.objective.id;
    }
    console.log(objective_data)
    var payload = JSON.stringify(objective_data)
    method = (holder.objective==null)?'POST':'PUT';
    destination = (holder.objective!=null)?`/api/handle_objectives/${holder.objective.id}/`:`/api/handle_objectives/`
    sender.open(method, destination)
    var csrf = getCookie('csrftoken');
    sender.setRequestHeader('X-CSRFToken', csrf);
    sender.setRequestHeader("Content-Type", "application/JSON");
    sender.setRequestHeader('Authorization', `Token ${token}`)
    sender.onload = function(){
        if(this.readyState == 4)
            {

                var response = JSON.parse(this.responseText);
                if(this.status >=200 && this.status < 300)
                {
                    toastr.success(`El record ha sido ${(holder.objective==null)?'Agregado':'Actualizado'} exitosamente!!`,'Success')
                    loadObjectiveList();
                    cleanForm();
                    holder.objective = null;
                    document.getElementById('closer').click();

                }

                else
                {
                   toastr.error(response.error,'Error');

                }

             }
    }
    sender.send(payload);
}


function handleConsecution(objective_id)
{
 var sender = new XMLHttpRequest();
    var token = getCookie('authtoken');
    var consecution_create = (document.getElementById('interpolation_op_status').value=='create')?true:false;
    var new_x = document.getElementById('new_x').value;
    if( parseFloat(new_x).toString() == 'NaN' || parseFloat(new_x) <= 0)
    {
        toastr.error('Para poder actualizar el valor, debe de tener un valor numerico aceptable. el valor debe ser mayor que cero y no debe tener caracteres alfanumericos')
    }
    else
    {

        method = (consecution_create == true)?'POST':'PUT';
        payload = JSON.stringify({'interpolation':new_x, 'objective': objective_id})
        inter_id = (consecution_create == false )? document.getElementById('obj_id').value : null;
        console.log(payload, consecution_create)
        destination = (consecution_create == true)?`/api/interpolation_operation/`:`/api/interpolation_operation/${inter_id}/`
        sender.open(method, destination)
        var csrf = getCookie('csrftoken');
        sender.setRequestHeader('X-CSRFToken', csrf);
        sender.setRequestHeader("Content-Type", "application/JSON");
        sender.setRequestHeader('Authorization', `Token ${token}`)
        sender.onload = function(){
        if(this.readyState == 4)
            {

                var response = JSON.parse(this.responseText);
                if(this.status >=200 && this.status < 300)
                {
                    toastr.success(`El record ha sido ${(consecution_create == true)?'Agregado':'Actualizado'} exitosamente!!`,'Success')
                    console.log(response,response.interpolation, response.cosecution_consecution_percentage);
                    document.getElementById('new_x').value='';
                    document.getElementById('new_x_value').value=`${response.interpolation}`
                    document.getElementById('consecution_value').value=`${response.consecution_percentage} %`;
                    close_my_modal('calculate_objective');
                }

                else
                {
                   console.log(response);
                   toastr.error(response.detail,'Error');

                }

             }
        }
        sender.send(payload);

    }

}


function modify_consecution(){
    var interpolation_value = document.getElementById('new_x_value').value;
    var new_x = document.getElementById('new_x');
    if( parseFloat(interpolation_value).toString() == 'NaN')
    {
        toastr.error('Para poder actualizar el valor, debe de tener un valor numerico aceptable.')
    }
    else
    {
        new_x.value=interpolation_value;
        $('#calculate_objective').modal('show');

    }
}
function modify_objective(objective_id){

 var sender = new XMLHttpRequest();
    var token = getCookie('authtoken');
    sender.open('GET',`/api/handle_objectives/${objective_id}/`)
    var csrf = getCookie('csrftoken');
    sender.setRequestHeader('X-CSRFToken', csrf);
    sender.setRequestHeader("Authorization",`Token ${token}`);
    sender.setRequestHeader("Content-Type", "application/JSON");
    sender.onload = function(){
        if(this.readyState == 4)
            {
                var response = JSON.parse(this.responseText);
                if(this.status == 200)
                {
                      console.log(response);
                      holder.objective=response;
                      load_form(holder.objective);

                }

                else
                {
                   toastr.error(response.error,'Error');

                }
                return null;

             }
    }
    sender.send();

}

function load_form(objective)
{
    holder.objective_id = objective.objective_id;
    console.log(objective.objectivegoal_set.length,"OBJECTIVE");
    AddMetricDiv(num=(objective.objectivegoal_set.length >= 2) ? objective.objectivegoal_set.length-2 : (objective.objectivegoal_set.length-2 ==1 )?1:0);
    var containers = document.getElementsByClassName('metric_container');
    var descriptions = document.getElementsByClassName(`meta_description`);
    var goals  = document.getElementsByClassName(`meta_value`);
    var percentage_concecution = document.getElementsByClassName(`meta_consecution`);
    goals_values = [descriptions, goals, percentage_concecution]
    console.log(goals_values, objective.objectivegoal_set.length)

    for(i=0; i<containers.length; i++)
    {   console.log(i,objective.objectivegoal_set.length)
        cov = containers[i].getElementsByTagName('input')
        cov[0].value=objective.objectivegoal_set[i].description;
        cov[1].value=objective.objectivegoal_set[i].goal;
        cov[2].value=objective.objectivegoal_set[i].consecution_percentage;

    }

    document.getElementById('id_metrica').value=objective.metric;
    document.getElementById('id_descripcion').value=objective.description;
//    document.getElementById('id_valor_de_acceptacion').value=objective.interpolation.x_new;

    $('#action_form').modal('show');

}

function delete_record(unique_id){

    var sender = new XMLHttpRequest();
    var token = getCookie('authtoken');
    var payload = JSON.stringify({
    "authtoken":token
    })
    sender.open('DELETE',`/api/handle_objectives/${unique_id}/`)
    var csrf = getCookie('csrftoken');
    sender.setRequestHeader('X-CSRFToken', csrf);
    sender.setRequestHeader("Content-Type", "application/JSON");
    sender.setRequestHeader('Authorization', `Token ${token}`)
    sender.onload = function(){
        if(this.readyState == 4)
            {

                if(this.status == 204)
                {
                    toastr.success("El record ha sido borrado existosamente!!",'Success')
                    loadObjectiveList();
                    close_my_modal(`delete-objective-${unique_id}`);


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
////                    console.log(list_name);
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
