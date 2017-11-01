$.when( $.ready ).then(function() {
    $('#searchForm input, #searchForm .btn')
        .focus(function () {
            $('#searchForm').addClass('focus');
            $('#searchText').attr('placeholder', '可輸入中文或漢羅');
        })
        .blur(function () {
            $('#searchForm').removeClass('focus');
            $('#searchText').attr('placeholder', '搜尋歌曲');
        });

    $('#searchForm')
        .find('.dropdown-item')
        .click(function (e) {
            var target = $(e.target);
            var value = target.data('value');
            $('#searchType').val(value);
            var text = target.text();
            $('#searchTypeSelect').text(text);
        });
});
