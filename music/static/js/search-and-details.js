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

            for(let index = 0; index<details.length; index++) {
                details[index].addEventListener("click", function(){
                    //console.log(reprs[index])
                    let element = $(".repr").eq(index).data().name;
                    //console.log(element)
                    let first_key = Object.keys(element)[0]
                    var img = convertStringToImageUrl(element[first_key]);
                    var stringa = "";
                    for (const key in element) {
                        if( key ===first_key)
                            continue;
                        if (key === "Copyright")
                            stringa += "<p class='card-text'><small class='text-muted'>" + element[key] + "</small></p>"
                        else
                            stringa += "<p class='card-text'>" + element[key] + "</p>";
                    }

                    let art = $('.art').eq(0).data().name;
                    let id_elem = $(".id_elem").eq(index).data().name;
                    let table_elem = $(".table_elem").eq(index).data().name;
                    let route_user = 'location.href="/delete/' + id_elem +'"';
                    let route_artist = 'location.href="/delete/' + table_elem + '/' + id_elem + '"';
                    if (art === "user")
                        stringa += "<span style='cursor: pointer;'>Saved <i class='bi bi-heart-fill' onclick="+ route_user +"></i></span>"
                    else if (art === "artist")
                        stringa += "<span style='cursor: pointer;'>Delete <i class='bi bi-trash' onclick="+ route_artist +"></i></span>"
                    Swal.fire({
                          title: 'Details',
                          html: "<div class='card mb-3' style='max-width: 500px;'>" +
                                  "<div class='row no-gutters'>" +
                                    "<div class='col-md-4'>" +
                                      "<img src='" + img + "' class='card-img' alt='...'>" +
                                    "</div>" +
                                    "<div class='col-md-8'>" +
                                      "<div class='card-body'>" +
                                        "<h5 class='card-title'>" + element[first_key] + "</h5>" +
                                        stringa +
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