$.when( $.ready ).then(function() {
    $('#search-form input, #search-form .btn')
        .focus(function () {
            $('#search-form').addClass('focus');
            $('#search-text').attr('placeholder', '可輸入中文或漢羅');
        })
        .blur(function () {
            $('#search-form').removeClass('focus');
            $('#search-text').attr('placeholder', '搜尋歌曲');
        });

    $('#search-form')
        .find('.dropdown-item')
        .click(function (e) {
            var target = $(e.target);
            var value = target.data('value');
            $('#search-type').val(value);
            var text = target.text();
            $('#search-type-select').text(text);
        });
});
