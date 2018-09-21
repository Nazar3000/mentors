$(document).ready(function() {

  $('#next-tip').click(function (e) {
    e.preventDefault();

    const dataId = $(this).attr('data-id');

    $.get(`/mentor/next-tip?id=${dataId}`, (data) => {
      $(this).attr('data-id', data.id);

      $('#tip-content').html(
        `<h2 class="admin-walk-title">Що робити з вихованцем</h2>
        <div class="admin-walk-line"></div>
        <div class="admin-walk-wrapp">
          <div class="admin-walk-place"><img src="${data.image}" alt="">
            <div class="admin-walk-desc">
              <h4>${data.title}</h4>
              <p>${data.content}</p>
            </div>
          </div>
        </div>`
      );
    })
  });

});