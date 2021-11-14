'use strict';

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#allpost-nav').addEventListener('click', () => load_index());
  document.querySelector('#followings-nav').addEventListener('click', () => load_followings());

  load_index();

});

function load_index() {

  // Show the mailbox and hide other views
  document.querySelector('#newpost-view').style.display = 'block';
  document.querySelector('#profile-view').style.display = 'none';
  document.querySelector('#followings-view').style.display = 'none';
  document.querySelector('#postings-view').style.display = 'block';

  let posting_body = document.querySelector('#postings-body')
  posting_body.value = "";

  document.querySelector('#postings-form').onsubmit = () => {
    if (posting_body.value !== "") {
      make_posting('/make_posting', posting_body.value);
      return false;
    } else {
      alert("No Post made: You posting text is empty!")
      return false;
    }
  };
}

function make_posting(url, text, post_id=null) {

  const postMsg = {
    method: "POST",
    body: JSON.stringify({ text: text, post_id: post_id}),
    headers: { "X-CSRFToken": getCookie('csrftoken') },
  }

  let fetchStatus = fetch(url, postMsg)
  .then(response => {
    if (response.status === 201) {
      response.json()
        .then(result => {
          console.log(`Response Message: ${result.message}`)
          alert(`Response Message: ${result.message}`);
          load_index();
          let select_page = document.querySelector('#select_page');
          let select_page_button = document.querySelector('#select_page_button');

          select_page.addEventListener("change", (e) => {
            select_page_button.click();
          });

          select_page.value  = 1;
          select_page.dispatchEvent(new Event('change'));

          return Promise.resolve(true);
        });
    } else {
      response.json()
        .then(result => {
          console.log(`Error Message: ${result.error}`)
          alert(`Error Message: ${result.error}`);
          return Promise.reject(new Error(response.statusText));
        });
    }
  }).catch(error => alert(`Send Mail Catch Error: ${error}`));

  return fetchStatus;
}

function edit_post(post_id) {

  document.querySelectorAll('textarea').forEach(textarea => {
    let foreach_id = textarea.dataset.textarea
    if(foreach_id != 0) {
      textarea.disabled=true;
      document.querySelector('#edit-' + foreach_id).disabled = false;
      document.querySelector('#post-' + foreach_id).disabled = true;
    }
  });
  document.querySelector('#postings-body-' + post_id).disabled=false;
  document.querySelector('#post-' + post_id).disabled=false;
}

function update_post(post_id) {

  let textarea = document.querySelector('#postings-body-' + post_id)

    if (textarea.value !== "") {
      make_posting('/make_posting', textarea.value, post_id);
    } else {
      alert("No Post made: You posting text is empty!")
    }

    document.querySelector('#postings-body-' + post_id).disabled=true;
    document.querySelector('#post-' + post_id).disabled=true;

}

// The following function are copying from
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function load_followings(){

  // Show the mailbox and hide other views
  document.querySelector('#newpost-view').style.display = 'none';
  document.querySelector('#profile-view').style.display = 'none';
  document.querySelector('#followings-view').style.display = 'block';
  document.querySelector('#postings-view').style.display = 'block';

  return true;
}

function load_profiles(){

  // Show the mailbox and hide other views
  document.querySelector('#newpost-view').style.display = 'none';
  document.querySelector('#profile-view').style.display = 'block';
  document.querySelector('#followings-view').style.display = 'none';
  document.querySelector('#postings-view').style.display = 'block';

  return true;
}
