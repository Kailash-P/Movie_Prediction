/* --- PREDICTION ANALYSIS --- */

function Predict() {

    function Generator() { };

    Generator.prototype.rand = Math.floor(Math.random() * 26) + Date.now();

    Generator.prototype.getId = function () {
        return this.rand++;
    };

    var idGen = new Generator();

    var uniqueId = "tt" + idGen.getId();

    var movieIMDBId = $('#txtMovieIMDBId').val();

    var movieTitle = $('#txtMovieTitle').val();

    var movieReleaseYear = $('#yrReleaseYear').val();

    var movieReleaseDate = $('#dtpReleaseDate').val();

    var movieGenre = $('#txtGenre').val();

    var movieWriters = $('#txtWriters').val();

    var movieActors = $('#txtActors').val();

    var movieDirectors = $('#txtDirectors').val();

    var movieSequel = $('#txtSequel').val();

    var jsonData = { data: [movieIMDBId, movieTitle, movieReleaseYear, movieReleaseDate, movieGenre, movieWriters, movieActors, movieDirectors, movieSequel] }

    var strJsonData = JSON.stringify(jsonData);

    if (!Validate(movieIMDBId, movieTitle, movieReleaseYear, movieReleaseDate, movieGenre, movieWriters, movieActors, movieDirectors, movieSequel)) {
        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://127.0.0.1:8080/predict",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Cache-Control": "no-cache"
            },
            "processData": false,
            "data": strJsonData
        }
        showNotification('Predicting ....', 'info', '', true);
        $.ajax(settings).done(function (response) {
            if (response) {
                hideNotification();
                var rating = response.Rating;
                var quotient = rating / 2;
                var reminder = rating % 2;
                var total = 5;
                var starCount = 0;
                var strHtml = "<div class=\"modal-dialog modal-sm\"><div class=\"modal-content\"><div class=\"modal-body\"><div  class=\"form-group\">";

                strHtml += "<h3><b> Rating. </h3></p><br/><h5>" + response.Prediction + "</h5>";

                if (quotient > 0) {
                    for (i = 1; i <= Math.floor(quotient); i++) {
                        strHtml += "<span class=\"fa fa-star checked\" style=\"font-size:36px;\"></span>";
                        starCount++;
                    }
                }

                if (reminder > 0) {
                    for (i = 1; i <= 1; i++) {
                        strHtml += "<span class=\"fa fa-star-half-o checked\" style=\"font-size:36px;\"></span>";
                        starCount++;
                    }
                }

                if (starCount < 5) {
                    for (i = 0; i <= (5 - starCount); i++) {
                        strHtml += "<span class=\"fa fa-star \" style=\"font-size:36px;\"></span>";
                        starCount++;
                    }
                }

                strHtml += "</div></div ></div ></div >"

                $('#divStarRatingPanel').html(strHtml);
            }
        });
    } else {
        showNotification('Please fill in all mandatory fields to proceed.', 'error', '');
    }
}

/* --- CLEAR ALL CONTROLS --- */

function ClearControls() {
    $('#txtMovieIMDBId').val('');
    $('#txtMovieTitle').val('');
    $('#yrReleaseYear').val('2019');
    $('#dtpReleaseDate').val('');
    $('#txtGenre').val('');
    $('#txtWriters').val('');
    $('#txtActors').val('');
    $('#txtDirectors').val('');
    $('#txtSequel').val('0');
    $('#divStarRatingPanel').html('');
}

/* --- VALIDATE PREDICTION --- */

function Validate(movieIMDBId, movieTitle, movieReleaseYear, movieReleaseDate, movieGenre, movieWriters, movieActors, movieDirectors, movieSequel) {
    var errorExists = false;
    if (!movieIMDBId || movieIMDBId == '') {
        $('#txtMovieIMDBId').addClass('btn-outline-danger');
        errorExists = true;
    }

    if (!movieTitle || movieTitle == '') {
        $('#txtMovieTitle').addClass('btn-outline-danger');
        errorExists = true;
    }

    if (!movieReleaseYear || movieReleaseYear == '') {
        $('#yrReleaseYear').addClass('btn-outline-danger');
        errorExists = true;
    }

    if (!movieReleaseDate || movieReleaseDate == '') {
        $('#dtpReleaseDate').addClass('btn-outline-danger');
        errorExists = true;
    }

    if (!movieGenre || movieGenre == '') {
        $('#txtGenre').addClass('btn-outline-danger');
        errorExists = true;
    }

    if (!movieWriters || movieWriters == '') {
        $('#txtWriters').addClass('btn-outline-danger');
        errorExists = true;
    }

    if (!movieActors || movieActors == '') {
        $('#txtActors').addClass('btn-outline-danger');
        errorExists = true;
    }

    if (!movieDirectors || movieDirectors == '') {
        $('#txtDirectors').addClass('btn-outline-danger');
        errorExists = true;
    }

    if (!movieSequel || movieSequel < 0) {
        $('#txtSequel').addClass('btn-outline-danger');
        errorExists = true;
    }

    return errorExists;
}

/* --- CHANGE EVENTS --- */

$('#txtMovieIMDBId').change(function () {
    var val = $('#txtMovieIMDBId').val();
    if (val && val != '') {
        $('#txtMovieIMDBId').removeClass('btn-outline-danger');
    }
});

$('#txtMovieTitle').change(function () {
    var val = $('#txtMovieTitle').val();
    if (val && val != '') {
        $('#txtMovieTitle').removeClass('btn-outline-danger');
    }
});

$('#yrReleaseYear').change(function () {
    var val = $('#yrReleaseYear').val();
    if (val && val != '') {
        $('#yrReleaseYear').removeClass('btn-outline-danger');
    }
});

$('#dtpReleaseDate').change(function () {
    var val = $('#dtpReleaseDate').val();
    if (val && val != '') {
        $('#dtpReleaseDate').removeClass('btn-outline-danger');
    }
});

$('#txtGenre').change(function () {
    var val = $('#txtGenre').val();
    if (val && val != '') {
        $('#txtGenre').removeClass('btn-outline-danger');
    }
});

$('#txtWriters').change(function () {
    var val = $('#txtWriters').val();
    if (val && val != '') {
        $('#txtWriters').removeClass('btn-outline-danger');
    }
});

$('#txtActors').change(function () {
    var val = $('#txtActors').val();
    if (val && val != '') {
        $('#txtActors').removeClass('btn-outline-danger');
    }
});

$('#txtDirectors').change(function () {
    var val = $('#txtDirectors').val();
    if (val && val != '') {
        $('#txtDirectors').removeClass('btn-outline-danger');
    }
});

$('#txtSequel').change(function () {
    var val = $('#txtSequel').val();
    if (val && val != '') {
        $('#txtSequel').removeClass('btn-outline-danger');
    }
});