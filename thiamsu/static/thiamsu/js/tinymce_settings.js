tinymce.init({
  selector: 'textarea',
  language: 'zh_TW',
  height: 500,
  menubar: false,
  plugins: [
    'lists link image media paste wordcount'
  ],
  toolbar: 'formatselect bold italic | numlist bullist | alignleft aligncenter | link image media',

  // formatselect
  block_formats: '內文=p;大標題=h3;小標題=h4',
  // link
  link_title: false,
  // media
  media_alt_source: false,
  media_poster: false,
  media_dimensions: false,
  // paste
  paste_as_text: true,

  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//www.tinymce.com/css/codepen.min.css']
});
