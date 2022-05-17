function search_alert() {
            Swal.fire({
                  title: 'Search!',
                  html: "<form action='/search-results' method='POST' class='form-signup' autocomplete='off'>" +
                      "<input type='search' name='search_text' id='login' class='swal2-input' placeholder='Search anything...' onclick='showResults(this.value)' >" +
                      "<div id='result'></div>" +
                      "<button type='submit' class='btn m-2' style='background-color: #00D1B2; color: white;' value='submit'>Search</button>  " +
                      "" +
                      "</form>",
                  showConfirmButton: false,
                  showClass: {
                    popup: 'animate__animated animate__fadeInDown'
                  },
                  hideClass: {
                    popup: 'animate__animated animate__fadeOutUp'
                  }
            });
        }

        /**
         *
         *
         * PASSARE L'ARRAY TRACKS PER LE TRACCE CONSIGLIATE
         *
         *
         */



        function autocompleteMatch(input) {
          if (input == '') {
            return search_terms;
          }
          var reg = new RegExp(input)
          return search_terms.filter(function(term) {
              if (term.match(reg)) {
              return term;
              }
          });
        }

        function showResults(val) {
          res = document.getElementById("result");
          res.innerHTML = '';
          let list = '';
          let terms = autocompleteMatch(val);
          for (i=0; i<terms.length; i++) {
            list += '<li class="list-group-item">' + terms[i] + '</li>';
          }
          let stringa = '';
          if (terms.length > 0)
              stringa += '<span>We recommend:</span>'
          stringa += '<ul class="list-group">' + list + '</ul>';
          res.innerHTML = stringa;
        }


        function showElementDetails() {

            let details = $(".details");
            let reprs = $(".repr");

            for(let index = 0; index<details.length; index++) {
                details[index].addEventListener("click", function(){
                    //console.log(reprs[index])
                    let element = $(".repr").eq(index).data().name;
                    //console.log(element)
                    var img = convertStringToImageUrl(element['Title']);
                    var stringa = "";
                    for (const key in element) {
                        if( key=='Title')
                            continue;
                        if (key == "Copyright")
                            stringa += "<p class='card-text'><small class='text-muted'>" + element[key] + "</small></p>"
                        else
                            stringa += "<p class='card-text'>" + element[key] + "</p>";
                    }
                    Swal.fire({
                          title: 'Details',
                          html: "<div class='card mb-3' style='max-width: 500px;'>" +
                                  "<div class='row no-gutters'>" +
                                    "<div class='col-md-4'>" +
                                      "<img src='" + img + "' class='card-img' alt='...'>" +
                                    "</div>" +
                                    "<div class='col-md-8'>" +
                                      "<div class='card-body'>" +
                                        "<h5 class='card-title'>" + element['Title'] + "</h5>" +
                                        stringa +
                                        "<span style='cursor: pointer;'>Saved <i class='bi bi-heart-fill'></i></span>" +
                                      "</div>" +
                                    "</div>" +
                                  "</div>" +
                                "</div>",
                          showConfirmButton: false,
                          showClass: {
                            popup: 'animate__animated animate__fadeInDown'
                          },
                          hideClass: {
                            popup: 'animate__animated animate__fadeOutUp'
                          }
                        });
                })
            }

        }