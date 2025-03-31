// Post Data Structure
class Post {
    constructor(username, avatar, content, likes, comments, reposts, shares, time, isVerified = false) {
        this.username = username;
        this.avatar = avatar;
        this.content = content;
        this.likes = likes;
        this.comments = comments;
        this.reposts = reposts;
        this.shares = shares;
        this.time = time;
        this.isVerified = isVerified;
    }
}

// Post Manager sara
class PostsManager {
    constructor() {
        this.posts = [];
        this.container = document.getElementById('posts-container');
        this.loading = false;
        this.page = 1;
    }

    async loadPosts() {
        if (this.loading) return;
        this.loading = true;
        document.getElementById('loadingSpinner').style.display = 'block';

        try {
            // Simuler un appel API
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Ajouter des posts de démonstration
            const newPosts = this.generateDummyPosts();
            this.posts = [...this.posts, ...newPosts];
            this.renderPosts(newPosts);
            
            this.page++;
        } catch (error) {
            console.error('Erreur lors du chargement des posts:', error);
        } finally {
            this.loading = false;
            document.getElementById('loadingSpinner').style.display = 'none';
        }
    }

    generateDummyPosts() {
        const dummyContent = [
            {
                username: 'mess.jpg',
                content: 'Amazing sunset in Bali! 🌅 #travelphotography',
                likes: 445,
                comments: 23,
                reposts:12,
                shares:11,
                isVerified: true
            },
            {
                username: 'tech_mike',
                content: 'Just deployed my first React Native app! 🚀 #coding #developer',
                likes: 232,
                comments: 45,
                reposts:12,
                shares:11,
                isVerified: false
            },
            {
                username: 'mess.jpg',
                content: 'Amazing sunset in Bali! 🌅 #travelphotography',
                likes: 445,
                comments: 23,
                reposts:12,
                shares:11,
                isVerified: true
            },
            {
                username: 'tech_mike',
                content: 'Just deployed my first React Native app! 🚀 #coding #developer',
                likes: 232,
                comments: 45,
                reposts:12,
                shares:11,
                isVerified: false
            },

            // Add more dummy content as needed
        ];

        return dummyContent.map(post => new Post(
            post.username,
            `mess.jpg`,
            post.content,
            post.likes,
            post.comments,
            Math.floor(Math.random() * 50),
            Math.floor(Math.random() * 20),
            `${Math.floor(Math.random() * 23)}h`,
            post.isVerified
        ));
    }

    renderPosts(postsToRender) {
        postsToRender.forEach(post => {
            const postElement = this.createPostElement(post);
            this.container.appendChild(postElement);
        });
    }

    createPostElement(post) {
        const postEl = document.createElement('div');
        postEl.className = 'post';
        
        postEl.innerHTML = `
            <div class="post-header">
                <div class="user-info">
                    <div class="user-avatar">
                        <img src="${post.avatar}" alt="${post.username}" />
                    </div>
                    <div class="user-name">
                        ${post.username}
                        ${post.isVerified ? '<span class="verified-badge"><i class="fa-solid fa-circle-check"></i></span>' : ''}
                    </div>
                </div>
                <div class="post-time">${post.time}</div>
            </div>
            <div class="post-content">${post.content}</div>
            <div class="post-actions">
                <button class="action-btn like-btn">
                    <i class="fa-regular fa-heart"></i>
                    <span>${post.likes}</span>
                </button>
                <button class="action-btn"><i class="far fa-comment"></i> <span>${post.comments}</span></button>
                <button class="action-btn"><i class="fas fa-retweet"></i> <span>${post.reposts}</span></button>
                <button class="action-btn"><i class="far fa-share-square"></i> <span>${post.shares}</span></button>

        `;
        return postEl;
    }
}

// Add infinite scroll handler
document.addEventListener('DOMContentLoaded', () => {
    const postsManager = new PostsManager();
    postsManager.loadPosts(); // Initial load

    // Infinite scroll
    window.addEventListener('scroll', () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1000) {
            postsManager.loadPosts();
        }
    });

    // Handle post input
    const postInput = document.querySelector('.post-input');
    const publishBtn = document.querySelector('.publish-btn');

    postInput.addEventListener('input', (e) => {
        publishBtn.disabled = e.target.value.trim().length === 0;
    });

    publishBtn.addEventListener('click', () => {
        if (postInput.value.trim()) {
            const newPost = {
                username: 'current_user',
                content: postInput.value,
                likes: 0,
                comments: 0,
                isVerified: true
            };
            
            // Add new post to beginning of feed
            const postElement = postsManager.createPostElement(new Post(
                newPost.username,
                '/images/avatar1.jpg',
                newPost.content,
                newPost.likes,
                newPost.comments,
                0,
                0,
                'À l\'instant',
                newPost.isVerified
            ));
            
            postsManager.container.insertBefore(postElement, postsManager.container.firstChild);
            postInput.value = '';
            publishBtn.disabled = true;
        }
    });
});
