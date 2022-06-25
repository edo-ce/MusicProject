$(document).ready(function(){
    var ctx = $("#myChart");
    

    //get values from jinja
    let vector = $('.values').eq(0).data().name;
    let numbers = vector.split(',');
    var values = [numbers[0],numbers[1],numbers[2]];


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


