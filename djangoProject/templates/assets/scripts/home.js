// Post Data Structure
class Post {
    constructor(username, avatar, content, likes, comments, reposts, shares, time, isVerified = false, auteur_id = null, is_liked = false, id = null) {
        this.username = username;
        this.avatar = avatar;
        this.content = content;
        this.likes = likes;
        this.comments = comments;
        this.reposts = reposts;
        this.shares = shares;
        this.time = time;
        this.isVerified = isVerified;
        this.auteur_id = auteur_id;
        this.is_liked = is_liked;
        this.id = id;
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
            const username = probleme.est_anonyme ? 'Anonyme' : (probleme.id_utilisateur?.nom_utilisateur || 'Utilisateur inconnu');
            const postDate = new Date(probleme.date_creation);
            const now = new Date();
            const diffHours = Math.floor((now - postDate) / (1000 * 60 * 60));
            const timeText = diffHours < 24 ? `${diffHours}h` : postDate.toLocaleDateString();
            
            return new Post(
                username,
                probleme.id_utilisateur?.profil?.url_avatar || '/static/images/default-avatar.png',
                probleme.contenu,
                probleme.likes_count || 0,  // Utiliser le nombre réel de likes
                probleme.comments || 0,      // À implémenter plus tard
                0,                          // reposts - à implémenter plus tard
                0,                          // shares - à implémenter plus tard
                timeText,
                false,
                probleme.id_utilisateur?.id,
                probleme.has_liked,
                probleme.id
            );
        });
    }

    renderPosts(postsToRender) {
        postsToRender.forEach(post => {
            const postElement = this.createPostElement(post);
            this.container.appendChild(postElement);
        });
    }

    async toggleLike(problemeId, likeBtn) {
        try {
            const response = await fetch('/toggle-reaction/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({ probleme_id: problemeId })
            });

            if (response.ok) {
                const data = await response.json();
                const likeCountSpan = likeBtn.querySelector('span');
                let currentLikes = parseInt(likeCountSpan.textContent, 10);

                if (data.liked) {
                    likeCountSpan.textContent = currentLikes + 1;
                    likeBtn.classList.add('liked');
                } else {
                    likeCountSpan.textContent = currentLikes - 1;
                    likeBtn.classList.remove('liked');
                }
            } else {
                console.error('Erreur lors de la mise à jour de la réaction');
            }
        } catch (error) {
            console.error('Erreur réseau:', error);
        }
    }

    createPostElement(post) {
        const postEl = document.createElement('div');
        postEl.className = 'post';
        
        // Créer l'icône initiale au lieu d'utiliser une image
        const userInitial = post.username.charAt(0).toUpperCase();
        
        postEl.innerHTML = `
            <div class="post-header">
                <div class="user-info">
                    <div class="user-initial-icon">
                        ${userInitial}
                    </div>
                    <div class="user-name">
                        ${post.username}
                        ${post.isVerified ? '<span class="verified-badge"><i class="fa-solid fa-circle-check"></i></span>' : ''}
                    </div>
                </div>
                <div class="post-time">${post.time}</div>
            </div>
            <div class="post-content">
                <p class="post-text">${post.content}</p>
            </div>
            <div class="post-actions">
                <button class="action-btn like-btn ${post.is_liked ? 'liked' : ''}" data-post-id="${post.id}">
                    <i class="fa-${post.is_liked ? 'solid' : 'regular'} fa-heart"></i>
                    <span class="like-count">${post.likes}</span>
                </button>
                <button class="action-btn">
                    <i class="far fa-comment"></i>
                    <span>${post.comments}</span>
                </button>
                <button class="action-btn send-msg-btn" data-userid="${post.auteur_id}" data-username="${post.username}" data-anonymous="${post.is_anonymous}">
                    <i class="far fa-envelope"></i>
                    <span>Message</span>
                </button>
            </div>
        `;

        // Ajouter l'écouteur d'événements pour le bouton de message
        const messageBtn = postEl.querySelector('.send-msg-btn');
        messageBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const userId = this.dataset.userid;
            const username = this.dataset.username;
            const isAnonymous = this.dataset.anonymous === 'true';
            openChatDialog(userId, isAnonymous ? 'Anonyme' : username);
        });

        const likeBtn = postEl.querySelector('.like-btn');
        likeBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            const postId = likeBtn.dataset.postId;
            console.log('Toggling like for post:', postId);  // Debug log
            
            try {
                const response = await fetch('/utilisateurs/toggle-like/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                    body: JSON.stringify({ post_id: parseInt(postId) })  // Changé de probleme_id à post_id
                });

                const data = await response.json();
                console.log('Like response:', data);  // Debug log
                
                if (data.success) {
                    const likeCount = likeBtn.querySelector('.like-count');
                    const icon = likeBtn.querySelector('i');
                    
                    if (data.is_liked) {
                        likeBtn.classList.add('liked');
                        icon.className = 'fa-solid fa-heart';
                    } else {
                        likeBtn.classList.remove('liked');
                        icon.className = 'fa-regular fa-heart';
                    }
                    likeCount.textContent = data.likes_count;
                }
            } catch (error) {
                console.error('Error toggling like:', error);
            }
        });

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

    // Modal handling
    const modal = document.getElementById('publishModal');
    const closeModalBtn = modal.querySelector('.close-modal');
    const cancelBtn = modal.querySelector('.cancel-btn');
    const submitBtn = modal.querySelector('.submit-btn');
    const titleInput = document.getElementById('problemTitle');
    const contentTextarea = document.getElementById('problemContent');
    const anonymousCheck = document.getElementById('anonymousCheck');

    function openModal() {
        modal.classList.add('active');
        titleInput.focus();
    }

    function closeModal() {
        modal.classList.remove('active');
        titleInput.value = '';
        contentTextarea.value = '';
        anonymousCheck.checked = false;
        submitBtn.disabled = true;
    }

    function validateInputs() {
        submitBtn.disabled = !(titleInput.value.trim() && contentTextarea.value.trim());
    }

    postInput.addEventListener('click', openModal);
    closeModalBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    
    [titleInput, contentTextarea].forEach(input => {
        input.addEventListener('input', validateInputs);
    });

    submitBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/problemes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    titre: titleInput.value.trim(),
                    contenu: contentTextarea.value.trim(),
                    est_anonyme: anonymousCheck.checked
                })
            });

            if (response.ok) {
                const newPost = await response.json();
                
                // Créer un nouveau post avec les données de la réponse
                const postElement = postsManager.createPostElement(
                    new Post(
                        newPost.est_anonyme ? 'Anonyme' : newPost.id_utilisateur.nom_utilisateur,
                        '/static/images/default-avatar.png',
                        `${newPost.titre}\n\n${newPost.contenu}`,
                        0,
                        0,
                        0,
                        0,
                        'À l\'instant',
                        false
                    )
                );
                
                // Ajouter le post au début du feed
                postsManager.container.insertBefore(postElement, postsManager.container.firstChild);
                closeModal();
                
                // Optionnel : Afficher un message de succès
                alert('Problème publié avec succès !');
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erreur lors de la publication');
            }
        } catch (error) {
            console.error('Erreur lors de la publication:', error);
            alert('Erreur lors de la publication : ' + error.message);
        }
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

function openChatDialog(userId, username) {
    const chatDialog = document.getElementById('chat-dialog');
    if (!chatDialog) {
        console.error('Chat dialog not found');
        return;
    }

    const messageInput = document.getElementById('message-input');
    const messagesContainer = chatDialog.querySelector('.chat-messages');
    const headerInitial = chatDialog.querySelector('.header-initial');
    const chatTitle = chatDialog.querySelector('.chat-title');
    
    // Réinitialiser l'état
    messageInput.value = '';
    messagesContainer.innerHTML = '';
    currentConversationId = null;
    
    // Configurer l'apparence
    if (username === 'Anonyme') {
        headerInitial.textContent = 'A';
        headerInitial.style.backgroundColor = '#6c757d';
        chatTitle.textContent = 'Anonyme';
    } else {
        headerInitial.textContent = username.charAt(0).toUpperCase();
        headerInitial.style.backgroundColor = username.charAt(0).toUpperCase() === 'T' ? '#0084ff' : '#65676b';
        chatTitle.textContent = username;
    }

    // Afficher la boîte de dialogue
    chatDialog.style.display = 'block';
    
    // Charger la conversation
    loadConversation(userId);
}