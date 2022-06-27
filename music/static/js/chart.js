$(document).ready(function(){

    //-----------------Gender chart
    var ctx = $("#gender");

    //get values from jinja
    let vector = $('.gender_listeners').eq(0).data().name;
    //console.log(vector);
    let numbers = vector.split(',');
    var values = [numbers[0],numbers[1],numbers[2]];
    if( numbers[0]==0 && numbers[1]==0 && numbers[2]==0) {
        alert("all values are zero [0]");
    }


    const data = {
      labels: [
        'Male',
        'Female',
        'Null'
      ],
      datasets: [{
        label: 'Dataset',
        data: [values[0], values[1], values[2]],
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)'
        ],
        hoverOffset: 4
      }]
    }

    //create pie chart
    const pie = new Chart(ctx,
    {
        type:"pie",
        data: data,
        options : {
            title: {
                display: true,
                text: 'Listener Gender'
            }
        }
    });


    //-----------------country chart

    var ctxc = $("#country");
    let v = $('.country_listeners').eq(0).data().name;
    let vals = v.split(',');

    countries = [];
    country_perc = [];
    for ( let i=0; i<vals.length; i=i+2 ){
        countries.push((vals[i]).toString());
        country_perc.push(vals[i+1]);
    }

     const datac = {
      labels: countries,
      datasets: [{
        label: 'Dataset',
        data: country_perc,
        backgroundColor: [
          'rgb(99,133,255)',
          'rgb(54,235,96)',
          'rgb(255,86,196)'
        ],
        hoverOffset: 4
      }]
    }

    //create pie chart
    const piec = new Chart(ctxc,
    {
        type:"pie",
        data: datac,
        options : {
            title: {
                display: true,
                text: 'Listener Country'
            }
        }
    });


});


