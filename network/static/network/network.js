'use strict';

document.addEventListener('DOMContentLoaded', function() {
  load_index()
});

function load_index() {

  let sections = document.querySelector("#sections");

  if (sections.dataset.sections == "Profile") {
      // Show the mailbox and hide other views
      document.querySelector('#newpost-view').style.display = 'none';
      document.querySelector('#profile-view').style.display = 'block';
      document.querySelector('#followings-view').style.display = 'none';
      document.querySelector('#postings-view').style.display = 'block';

  } else if (sections.dataset.sections == "Followings") {
      // Show the mailbox and hide other views
      document.querySelector('#newpost-view').style.display = 'none';
      document.querySelector('#profile-view').style.display = 'none';
      document.querySelector('#followings-view').style.display = 'block';
      document.querySelector('#postings-view').style.display = 'block';

  } else {
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
          alert("No Post made: Your posting text is empty!")
          return false;
        }
      };
    }

  document.querySelectorAll('.bi-hand-thumbs-up').forEach(t => {
    if (t.dataset.svg == "True") {
      t.style.color = 'red';
      t.dataset.likes = 'on';
    } else {
      t.style.color = 'black';
      t.dataset.likes = 'off';
    }
  });

  document.querySelectorAll('.bi-hand-thumbs-down').forEach(t => {
    if (t.dataset.svg == "False") {
      t.style.color = 'red'
      t.dataset.likes = 'on';
    } else {
      t.style.color = 'black'
      t.dataset.likes = 'off';
    }
  });

}

function make_posting(url, text, post_id = null) {

  const postMsg = {
    method: "POST",
    body: JSON.stringify({
      text: text,
      post_id: post_id
    }),
    headers: {
      "X-CSRFToken": getCookie('csrftoken')
    },
  }

  let fetchStatus = fetch(url, postMsg)
    .then(response => {
      if (response.status === 201) {
        response.json()
          .then(result => {
            console.log(`Response Message: ${result.message} ID: ${result.posting_pk}`)
            alert(`Response Message: ${result.message} ID: ${result.posting_pk}`);
            //load_index();
            let select_page = document.querySelector('#select_page');
            if ( select_page == null ){
              window.location.reload()
            } else {
              let select_page_button = document.querySelector('#select_page_button');

              select_page.addEventListener("change", (e) => {
              select_page_button.click();
              });

              select_page.value = 1;
              select_page.dispatchEvent(new Event('change'));
          }


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

  const user = JSON.parse(document.getElementById('request_username').textContent);
  document.querySelectorAll('textarea').forEach(textarea => {
    let foreach_id = textarea.dataset.textarea
    if (foreach_id != 0) {
      if (textarea.disabled == false) {
        if (textarea.defaultValue !== textarea.value) {
          textarea.value = textarea.defaultValue;
        }
      }
      textarea.disabled = true;
      const posting_user = (document.getElementById('post-user-' + foreach_id).textContent);
      if (posting_user === user) {
        document.querySelector('#edit-' + foreach_id).style.display = 'block';
      } else {
        document.querySelector('#edit-' + foreach_id).style.display = 'none';
      }
      document.querySelector('#post-' + foreach_id).style.display = 'none';
    }
  });
  document.querySelector('#postings-body-' + post_id).disabled = false;
  document.querySelector('#edit-' + post_id).style.display = 'none';
  document.querySelector('#post-' + post_id).style.display = 'block';
}

function update_post(post_id) {

  let textarea = document.querySelector('#postings-body-' + post_id)

  if (textarea.value !== "") {
    if (textarea.defaultValue !== textarea.value) {
      make_posting('/make_posting', textarea.value, post_id);
    }
  } else {
    alert("No Post made: You posting text is empty!")
  }

  document.querySelector('#postings-body-' + post_id).disabled = true;
  document.querySelector('#post-' + post_id).style.display = 'none';

}

function thumbs_up(post_id) {

  const user = JSON.parse(document.getElementById('request_username').textContent);
  const posting_user = (document.getElementById('post-user-' + post_id).textContent);

  if (user === posting_user) {
    // alert("You cannot like your own post!");
    return false;
  }
  let thumbs_up_button = document.getElementById('thumbs-up-' + post_id);
  let thumbs_down_button = document.getElementById('thumbs-down-' + post_id);
  if (thumbs_up_button.dataset.likes == 'off') {

    post_thumbs_click(post_id, true)
    thumbs_up_button.style.color = 'red';
    thumbs_up_button.dataset.likes = 'on';

    thumbs_down_button.style.color = 'black';
    thumbs_down_button.dataset.likes = 'off';

  } else {

    post_thumbs_click(post_id, null)
    thumbs_up_button.style.color = 'black';
    thumbs_up_button.dataset.likes = 'off';
  }
  return true;
}

function thumbs_down(post_id) {

  const user = JSON.parse(document.getElementById('request_username').textContent);
  const posting_user = (document.getElementById('post-user-' + post_id).textContent);

  if (user === posting_user) {
    // alert("You cannot unlike your own post!");
    return false;
  }

  let thumbs_up_button = document.getElementById('thumbs-up-' + post_id);
  let thumbs_down_button = document.getElementById('thumbs-down-' + post_id);
  if (thumbs_down_button.dataset.likes == 'off') {

    post_thumbs_click(post_id, false)
    thumbs_down_button.style.color = 'red';
    thumbs_down_button.dataset.likes = 'on';

    thumbs_up_button.style.color = 'black';
    thumbs_up_button.dataset.likes = 'off';

  } else {

    post_thumbs_click(post_id, null)
    thumbs_down_button.style.color = 'black';
    thumbs_down_button.dataset.likes = 'off';
  }
  return true;
}

function post_thumbs_click(post_id, likes) {

  const postMsg = {
    method: "POST",
    body: JSON.stringify({
      thumbs: likes,
      post_id: post_id
    }),
    headers: {
      "X-CSRFToken": getCookie('csrftoken')
    },
  }

  let fetchStatus = fetch('/thumbs_click', postMsg)
    .then(response => {
      if (response.status === 201) {
        response.json()
          .then(result => {
            console.log(`Response Message: ${result.message}`)
            // alert(`Response Message Likes Count: ${result.likes_count}`);
            // alert(`Response Message DisLikes Count: ${result.dislikes_count}`);
            document.getElementById('likes-count-' + post_id).textContent = result.likes_count;
            document.getElementById('dislikes-count-' + post_id).textContent = result.dislikes_count;

            return Promise.resolve(true);
          });
      } else {
        response.json()
          .then(result => {
            console.log(`Error Message: ${result.error}`)
            // alert(`Error Message: ${result.error}`);
            return Promise.reject(new Error(response.statusText));
          });
      }
    }).catch(error => alert(`Thumbs Up Catch Error: ${error}`));

  return fetchStatus
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

function follow(follow) {

  const profile_id = (document.getElementById('profile-id').textContent);

  const postMsg = {
    method: "POST",
    body: JSON.stringify({
      profile_id: profile_id,
      follow: (follow === "follow" ? true : false)
    }),
    headers: {
      "X-CSRFToken": getCookie('csrftoken')
    },
  }

  let fetchStatus = fetch('/follows', postMsg)
    .then(response => {
      if (response.status === 201) {
        response.json()
          .then(result => {
            console.log(`Response Message: ${result.message}`)
            //alert(`Response Message follower Count: ${result.followings_count}, ${result.followers_count}`);

            document.getElementById("followings-count").textContent = result.followings_count;
            document.getElementById("followers-count").textContent = result.followers_count;

			if (result.user_follows == 0 ){
				document.getElementById("follow-button").style.display = "block";
				document.getElementById("unfollow-button").style.display = "none";

			} else {
				document.getElementById("follow-button").style.display = "none";
				document.getElementById("unfollow-button").style.display = "block";
			}

            return Promise.resolve(true);
          });
      } else {
        response.json()
          .then(result => {
            console.log(`Error Message: ${result.error}`)
            // alert(`Error Message: ${result.error}`);
            return Promise.reject(new Error(response.statusText));
          });
      }
    }).catch(error => alert(`Thumbs Up Catch Error: ${error}`));

  return fetchStatus
}
