$.when( $.ready ).then(function() {
    $('#song-list-ordering')
        .on('show.bs.dropdown', function () {
            console.log('Hey~')
        });
});
