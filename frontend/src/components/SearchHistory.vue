<template>
  <div class="history-container">
    <div class="history-header">
      <h3>Search History</h3>
      <div class="header-buttons">
        <button v-if="searchHistory.length >= 2" @click="generateProfile" class="profile-button" :disabled="isGeneratingProfile">
          Profile Me
        </button>
        <button v-if="searchHistory.length > 0" @click="clearHistory" class="clear-history-button">
          Clear History
        </button>
      </div>
    </div>
    
    <div v-if="userProfile" class="profile-container">
      <div class="profile-content">
        <h4>Your Reader Profile</h4>
        <div class="profile-text" v-html="formattedProfile"></div>
      </div>
      <button @click="clearProfile" class="close-profile">×</button>
    </div>
    
    <div v-if="searchHistory.length === 0" class="empty-history">
      <p>No search history yet</p>
    </div>
    
    <div v-else class="history-list">
      <div 
        v-for="(item, index) in searchHistory" 
        :key="index" 
        class="history-item"
        @click="selectSearch(item)"
      >
        <div class="history-query">
          <span class="query-text">{{ item.query }}</span>
          <span class="query-date">{{ formatDate(item.timestamp) }}</span>
        </div>
        <div class="history-preview">
          <div 
            v-for="book in item.previewBooks.slice(0, 3)" 
            :key="book.id" 
            class="book-preview"
          >
            <img 
              :src="book.cover_url || 'https://via.placeholder.com/40x60?text=No+Cover'" 
              :alt="book.title"
              class="preview-cover"
            />
          </div>
          <div v-if="item.books.length > 3" class="more-books">
            +{{ item.books.length - 3 }} more
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>


export default {
  name: 'SearchHistory',
  props: {
    searchHistory: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      userProfile: '',
      isGeneratingProfile: false
    };
  },
  methods: {
    selectSearch(item) {
      this.$emit('select-search', item);
    },
    clearHistory() {
      this.$emit('clear-history');
      this.clearProfile();
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString(undefined, {
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    async generateProfile() {
      if (this.searchHistory.length < 2 || this.isGeneratingProfile) return;
      
      this.isGeneratingProfile = true;
      this.userProfile = '';
      
      try {
        // Check if backend server is available
        try {
          const healthCheck = await fetch('http://localhost:8001/');
          if (!healthCheck.ok) {
            throw new Error('Backend server unreachable');
          }
        } catch (e) {
          throw new Error('Backend server appears to be offline. Please make sure the backend is running.');
        }
        
        // Extract queries from search history
        const queries = this.searchHistory.map(item => item.query);
        
        console.log('Sending profile request with queries:', queries);
        
        // Use fetch with streaming instead of axios
        const response = await fetch('http://localhost:8001/api/generate-profile', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ queries }),
        });
        
        if (!response.ok) {
          console.error('Profile generation failed with status:', response.status);
          throw new Error(`HTTP error! status: ${response.status}. Make sure the backend server is running.`);
        }
        
        // Create a reader for the stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        // Read stream chunks and append to profile
        let streamComplete = false;
        while (!streamComplete) {
          const { done, value } = await reader.read();
          if (done) {
            streamComplete = true;
          } else {
            const chunk = decoder.decode(value);
            this.userProfile += chunk;
          }
        }
      } catch (error) {
        console.error('Error generating profile:', error);
        this.userProfile = `Failed to generate your profile: ${error.message}`;
      } finally {
        this.isGeneratingProfile = false;
      }
    },
    clearProfile() {
      this.userProfile = '';
    }
  },
  computed: {
    // Format the profile text with line breaks
    formattedProfile() {
      if (!this.userProfile) return '';
      return this.userProfile.replace(/\n/g, '<br>');
    }
  }
};
</script>

<style scoped>
.history-container {
  background-color: #222;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #444;
  padding-bottom: 10px;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.history-header h3 {
  font-size: 1.4rem;
  font-weight: 300;
  color: #e0e0e0;
  margin: 0;
}

.clear-history-button, .profile-button {
  background-color: #555;
  color: #ddd;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.profile-button {
  background-color: #4a6fa5;
}

.profile-button:hover {
  background-color: #5a8ad3;
}

.profile-button:disabled {
  background-color: #3a5a80;
  cursor: not-allowed;
}

.clear-history-button:hover {
  background-color: #777;
}

.empty-history {
  text-align: center;
  padding: 20px 0;
  color: #777;
  font-style: italic;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  padding: 15px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.history-item:hover {
  background-color: #444;
}

.history-query {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.query-text {
  font-size: 1.1rem;
  color: #e0e0e0;
}

.query-date {
  font-size: 0.85rem;
  color: #999;
}

.history-preview {
  display: flex;
  align-items: center;
  gap: 10px;
}

.book-preview {
  width: 40px;
  height: 60px;
  overflow: hidden;
  border-radius: 3px;
}

.preview-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.more-books {
  font-size: 0.9rem;
  color: #999;
  white-space: nowrap;
}

.profile-container {
  background-color: #333;
  border-radius: 6px;
  margin-bottom: 20px;
  padding: 20px;
  position: relative;
  border-left: 4px solid #4a6fa5;
  animation: fadeIn 0.5s ease-in-out;
}

.profile-content h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #e0e0e0;
  font-weight: 400;
  font-size: 1.2rem;
}

.profile-text {
  color: #ccc;
  line-height: 1.6;
  font-size: 1rem;
}

.close-profile {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: #888;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s, color 0.2s;
}

.close-profile:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ccc;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>