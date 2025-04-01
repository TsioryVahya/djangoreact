document.addEventListener('DOMContentLoaded', () => {
    console.log('Search.js loaded - Auto-filter version');
    
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const postsContainer = document.getElementById('posts-container');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
    if (!searchInput || !postsContainer) {
        console.error('Essential elements not found on search page');
        return;
    }
    
    // Pagination variables
    let currentPage = 1;
    let hasMorePosts = true;
    let isLoading = false;
    let currentQuery = '';
    
    // Simple function to get CSRF token
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
    
    // Function to fetch and display posts
    async function fetchPosts(query = '', page = 1, append = false) {
        if (isLoading || (!append && !hasMorePosts)) return;
        
        isLoading = true;
        loadingSpinner.style.display = 'block';
        
        if (!append) {
            postsContainer.innerHTML = '';
            hasMorePosts = true;
        }
        
        try {
            let url = `/api/problemes/?page=${page}`;
            if (query) {
                url += `&search=${encodeURIComponent(query)}`;
            }
            
            console.log(`Fetching posts: ${url}`);
            
            const response = await fetch(url, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            if (!response.ok) {
                throw new Error(`Network error: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.results && data.results.length > 0) {
                displayResults(data.results, append);
                hasMorePosts = data.next !== null;
            } else if (!append) {
                postsContainer.innerHTML = '<div class="no-results
