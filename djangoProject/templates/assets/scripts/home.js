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

// Post Manager
class PostsManager {
    constructor() {
        this.posts = [];
        this.container = document.getElementById('posts-container');
        this.loading = false;
        this.page = 1;
        this.hasMore = true;
    }

    async loadPosts() {
        if (this.loading || !this.hasMore) return;
        this.loading = true;
        document.getElementById('loadingSpinner').style.display = 'block';

        try {
            const response = await fetch(`/api/problemes/?page=${this.page}`);
            if (!response.ok) {
                throw new Error('Erreur réseau');
            }
            const data = await response.json();
            
            if (data.results.length === 0) {
                this.hasMore = false;
                return;
            }
            
            const newPosts = this.transformApiDataToPosts(data.results);
            this.posts = [...this.posts, ...newPosts];
            this.renderPosts(newPosts);
            
            this.hasMore = data.has_next;
            this.page++;
        } catch (error) {
            console.error('Erreur lors du chargement des posts:', error);
        } finally {
            this.loading = false;
            document.getElementById('loadingSpinner').style.display = 'none';
        }
    }

    transformApiDataToPosts(apiData) {
        return apiData.map(probleme => {
            // Utilisez le nom d'utilisateur ou "Anonyme" si le post est anonyme
            const username = probleme.est_anonyme ? 'Anonyme' : (probleme.id_utilisateur?.nom_utilisateur || 'Utilisateur inconnu');
            
            // Formatage de la date (simplifié - vous pourriez utiliser une lib comme moment.js)
            const postDate = new Date(probleme.date_creation);
            const now = new Date();
            const diffHours = Math.floor((now - postDate) / (1000 * 60 * 60));
            const timeText = diffHours < 24 ? `${diffHours}h` : postDate.toLocaleDateString();
            
            return new Post(
                username,
                probleme.id_utilisateur?.profil?.url_avatar || '/static/images/default-avatar.png',
                probleme.contenu,
                Math.floor(Math.random() * 100), // likes aléatoires (à adapter si votre API les fournit)
                Math.floor(Math.random() * 30),   // comments aléatoires
                Math.floor(Math.random() * 20),   // reposts aléatoires
                Math.floor(Math.random() * 10),   // shares aléatoires
                timeText,
                false // isVerified - à adapter selon vos besoins
            );
        });
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
                        <img src="${post.avatar}" alt="${post.username}" onerror="this.src='/static/images/default-avatar.png'" />
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
            </div>
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

    // Handle post input (si vous voulez garder cette fonctionnalité)
    const postInput = document.querySelector('.post-input');
    const publishBtn = document.querySelector('.publish-btn');

    if (postInput && publishBtn) {
        postInput.addEventListener('input', (e) => {
            publishBtn.disabled = e.target.value.trim().length === 0;
        });

        publishBtn.addEventListener('click', () => {
            if (postInput.value.trim()) {
                // Ici, vous devriez faire un appel API pour créer un nouveau problème
                // Ceci est juste un exemple simplifié
                const newPost = {
                    username: 'current_user',
                    content: postInput.value,
                    likes: 0,
                    comments: 0,
                    isVerified: true
                };
                
                const postElement = postsManager.createPostElement(new Post(
                    newPost.username,
                    '/static/images/default-avatar.png',
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
    }
});