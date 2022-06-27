$(document).ready(function(){
    var ctx = $("#gender");

    //get values from jinja
    let vector = $('.gender_listeners').eq(0).data().name;
    //console.log(vector);
    let numbers = vector.split(',');
    var values = [numbers[0],numbers[1],numbers[2]];
    if( numbers[0]==0 && numbers[1]==0 && numbers[2]==0) {
        alert("all values are zero [0]");
        return;
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
                /*font: {
                    family: 'Comic Sans MS',
                    size: 50,
                    weight: 'bold',
                    lineHeight: 1.2,
                  },*/
            }
        }
    });

});


