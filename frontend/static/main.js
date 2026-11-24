window.onload = function () {
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
};

function renderPosts(data) {
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = '';
    data.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.innerHTML = `<h2>${post.title}</h2>
            <p>${post.content}</p>
            <p><small>By ${post.author || 'Unknown'} on ${post.date || ''}</small></p>
            <button onclick="deletePost(${post.id})">Delete</button>`;
        postContainer.appendChild(postDiv);
    });
}

function loadPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    var sort = document.getElementById('sort-field').value;
    var direction = document.getElementById('sort-direction').value;
    var url = baseUrl + '/posts';
    if (sort) {
        url += `?sort=${sort}&direction=${direction}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => renderPosts(data))
        .catch(error => console.error('Error:', error));
}

function searchPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    var term = encodeURIComponent(document.getElementById('search-term').value);
    var url = `${baseUrl}/posts/search?title=${term}&content=${term}&author=${term}`;

    fetch(url)
        .then(response => response.json())
        .then(data => renderPosts(data))
        .catch(error => console.error('Error:', error));
}

function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;
    var postDate = document.getElementById('post-date').value;

    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: postTitle,
            content: postContent,
            author: postAuthor,
            date: postDate
        })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post added:', post);
        loadPosts();
    })
    .catch(error => console.error('Error:', error));
}

function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;
    fetch(baseUrl + '/posts/' + postId, { method: 'DELETE' })
        .then(() => {
            console.log('Post deleted:', postId);
            loadPosts();
        })
        .catch(error => console.error('Error:', error));
}