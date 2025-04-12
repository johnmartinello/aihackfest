<template>
  <div class="search-container">
    <div class="search-box">
      <input 
        type="text" 
        v-model="query" 
        @keyup.enter="searchBooks" 
        placeholder="What kind of books are you looking for?"
        :disabled="isLoading"
        class="search-input"
      />
      <button 
        @click="searchBooks" 
        class="search-button"
        :disabled="isLoading || !query.trim()"
      >
        <span v-if="isLoading">Searching...</span>
        <span v-else>Search</span>
      </button>
    </div>
    
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">
        <span v-if="processingStage === 'ai'">Searching for book recommendations...</span>
        <span v-else-if="processingStage === 'structuring'">Structuring recommendations...</span>
      </p>
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BookSearch',
  data() {
    return {
      query: '',
      isLoading: false,
      error: null,
      processingStage: 'ai' 
    };
  },
  methods: {
    async searchBooks() {
      if (!this.query.trim() || this.isLoading) return;
      
      this.isLoading = true;
      this.error = null;
      this.processingStage = 'ai';
      
      try {
        // Add a delay before changing to the structuring stage to simulate the process
        // This ensures users see the initial "Searching..." message
        setTimeout(() => {
          if (this.isLoading) {
            this.processingStage = 'structuring';
          }
        }, 2000);
        
        const response = await axios.post('http://localhost:8000/api/search', {
          query: this.query
        });
        
        // Emit the result to parent component
        this.$emit('books-loaded', response.data);
      } catch (error) {
        console.error('Error searching for books:', error);
        this.error = 'Failed to get book recommendations. Please try again.';
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.search-container {
  margin-bottom: 30px;
}

.search-box {
  display: flex;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  border-radius: 30px;
  overflow: hidden;
}

.search-input {
  flex: 1;
  padding: 15px 25px;
  font-size: 1.1rem;
  border: none;
  outline: none;
  background-color: #333; 
  color: #e0e0e0; 
}

.search-input::placeholder {
  color: #888;
}

.search-button {
  padding: 15px 30px;
  background-color: #3498db;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #2980b9;
}

.search-button:disabled {
  background-color: #444; 
  color: #888; 
  cursor: not-allowed;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 40px;
}

.loading-spinner {
  border: 4px solid #333; 
  border-top: 4px solid #3498db; 
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 2s linear infinite;
  margin-bottom: 15px;
}

.loading-text {
  color: #bbb; 
}

.error-message {
  color: #ff6b6b; 
  text-align: center;
  margin-top: 20px;
  padding: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>