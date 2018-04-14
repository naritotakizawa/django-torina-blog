/* 目次を自動で生成します。

<h2 id="1">犬とは</h2>
<h3 id="2">ビーグル</h3>
<h3 id="3">柴犬</h3>

<h2 id="4">猫とは</h2>

<h2 id="5">熊とは</h2>

という見出しだった場合は

<div class="card mb-1">
  <div class="card-body" id="toc">
    <p class="text-center font-weight-bold h4">目次</p>
    <ul>
      <li>
        <a href="#1">犬とは</a>
        <ul>
          <li><a href="#2">ビーグル</a></li>
          <li><a href="#3">柴犬</a></li>
        </ul>
      </li>
      <li>
        <a href="#4">猫とは</a>
      </li>
      <li>
        <a href="#5">熊とは</a>
      </li>
    </ul>
  </div>
</div>

となります。

*/

// 最終的なhtml
let toc_html = ''

// h3があったら、これをtrueにし、その後にこの値によって</ul>等を入れる
let h3_flag = false

$(".blog-h2, .blog-h3").each(function(){
  // h2
  if ($(this)[0].tagName == 'H2'){
    let li_html = ''
    li_html += '<li><a href="#' + $(this).prop("id") + '">' + $(this).text() + '</a>'

    // 前がh3だったら、</li></ul>を入れてフラグをfalse。前の<li>h2<ul>h3を閉じるため
    if (h3_flag){
      toc_html += '</ul></li>'
      h3_flag = false

    // 前がh2なら、</li>を入れて1つの<li>として簡潔させておく
    }else{
      toc_html += '</li>'
    }
    toc_html += li_html
  // h3
  }else{
    // 前がh3だったら、そのまま<li>として入れる。既に中の<ul>があるため
    if (h3_flag){
      toc_html += '<li><a href="#' + $(this).prop("id") + '">' + $(this).text() + '</a></li>'
    
    //前がh2だったら、今後のために<ul>を作る。この中に<li>が入っていく
    }else{
      h3_flag = true
      toc_html += '<ul><li><a href="#' + $(this).prop("id") + '">' + $(this).text() + '</a></li>'
    }
  }
});

// toc_htmlが空じゃなければ、目次として挿入
if (toc_html){
  toc_html = '<div class="card"><div class="card-body"><p class="text-center font-weight-bold h4">目次</p><ul>' + toc_html + '</ul></div></div>'
  $('#toc').html(toc_html);
}