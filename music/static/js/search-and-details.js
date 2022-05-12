function search_alert() {
            Swal.fire({
                  title: 'Search!',
                  html: "<form method='POST' class='form-signup' autocomplete='off'>" +
                      "<input type='search' id='login' class='swal2-input' placeholder='Search anything...' onclick='showResults(this.value)' >" +
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


        function showElementDetails(element) {
            element = JSON.parse(element);
            console.log(element);
            var img = convertStringToImageUrl(element['title']);
            var keys = ['duration', 'copyright', 'genre', 'release_date', 'stage_name', 'bio', 'creator'];
            var stringa = "";
            for (const key of keys) {
                if (element.hasOwnProperty(key)) {
                    if (key == "copyright")
                        stringa += "<p class='card-text'><small class='text-muted'>" + element[key] + "</small></p>"
                    else stringa += "<p class='card-text'>" + element[key] + "</p>";
                }
            }
            Swal.fire({
                  title: 'Track details',
                  html: "<div class='card mb-3' style='max-width: 500px;'>" +
                          "<div class='row no-gutters'>" +
                            "<div class='col-md-4'>" +
                              "<img src='" + img + "' class='card-img' alt='...'>" +
                            "</div>" +
                            "<div class='col-md-8'>" +
                              "<div class='card-body'>" +
                                "<h5 class='card-title'>" + element['title'] + "</h5>" +
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
        }