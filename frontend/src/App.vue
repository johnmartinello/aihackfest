<template>
  <div class="app-container">
    <header>
      <h1>Book Recommendation System</h1>
      <div class="history-toggle" @click="toggleHistory">

        <span v-if="!showHistory">History</span>
        <span v-else>Hide</span>
      </div>
    </header>
    <main>
      <search-history 
        v-if="showHistory" 
        :searchHistory="searchHistory" 
        @select-search="loadFromHistory"
        @clear-history="clearHistory"
      ></search-history>
      
      <book-search @books-loaded="handleBooksLoaded"></book-search>
      <book-results 
        v-if="hasResults" 
        :books="books" 
        @load-more="loadMoreBooks"
        :isLoadingMore="isLoadingMore"
      ></book-results>
    </main>
    <footer>
      <p> Application made for AI Hackfest (2025) in one day, by João Lucas Martinello (and AIs)</p>
    </footer>
  </div>
</template>

<script>
import BookSearch from './components/BookSearch.vue';
import BookResults from './components/BookResults.vue';
import SearchHistory from './components/SearchHistory.vue';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    BookSearch,
    BookResults,
    SearchHistory
  },
  data() {
    return {
      books: [],
      hasResults: false,
      searchId: null,
      searchQuery: '',
      isLoadingMore: false,
      searchHistory: [],
      showHistory: false
    };
  },
  created() {
    // Load search history from localStorage when the app starts
    this.loadSearchHistory();
  },
  methods: {
    handleBooksLoaded(data) {
      this.books = data.books;
      this.searchId = data.id;
      this.searchQuery = data.query;
      this.hasResults = true;
      
      // Save this search to history
      this.saveToHistory({
        id: data.id,
        query: data.query,
        timestamp: new Date().toISOString(),
        books: data.books,
        previewBooks: data.books.slice(0, 3)  
      });
    },
    async loadMoreBooks() {
      if (!this.searchId || this.isLoadingMore) return;
      
      this.isLoadingMore = true;
      
      try {
        const response = await axios.post('http://localhost:8000/api/more-books', {
          search_id: this.searchId,
          count: 6 
        });
        
        // Update books with the full list (including new recommendations)
        this.books = response.data.books;
        
        // Update this search in history with new books
        this.updateHistoryItem({
          id: this.searchId,
          query: this.searchQuery,
          books: response.data.books,
          previewBooks: response.data.books.slice(0, 3)
        });
      } catch (error) {
        console.error('Error loading more books:', error);
      } finally {
        this.isLoadingMore = false;
      }
    },
    toggleHistory() {
      this.showHistory = !this.showHistory;
    },
    loadFromHistory(item) {
      // Load books from history item
      this.books = item.books;
      this.searchId = item.id;
      this.searchQuery = item.query;
      this.hasResults = true;
      
      // Hide history after selection
      this.showHistory = false;
    },
    saveToHistory(search) {
      // Check if this search already exists in history
      const existingIndex = this.searchHistory.findIndex(item => item.query === search.query);
      
      if (existingIndex > -1) {
        // Update existing search
        this.searchHistory.splice(existingIndex, 1);
      }
      
      // Add to the beginning of history array
      this.searchHistory.unshift(search);
      
      // Limit history to 10 items
      if (this.searchHistory.length > 10) {
        this.searchHistory = this.searchHistory.slice(0, 10);
      }
      
      // Save to localStorage
      this.saveSearchHistory();
    },
    updateHistoryItem(updatedSearch) {
      const index = this.searchHistory.findIndex(item => item.id === updatedSearch.id);
      
      if (index > -1) {
        // Update the search in history
        this.searchHistory[index].books = updatedSearch.books;
        this.searchHistory[index].previewBooks = updatedSearch.previewBooks;
        
        // Save to localStorage
        this.saveSearchHistory();
      }
    },
    clearHistory() {
      this.searchHistory = [];
      this.saveSearchHistory();
    },
    saveSearchHistory() {
      try {
        localStorage.setItem('bookSearchHistory', JSON.stringify(this.searchHistory));
      } catch (e) {
        console.error('Error saving search history to localStorage:', e);
      }
    },
    loadSearchHistory() {
      try {
        const savedHistory = localStorage.getItem('bookSearchHistory');
        if (savedHistory) {
          this.searchHistory = JSON.parse(savedHistory);
        }
      } catch (e) {
        console.error('Error loading search history from localStorage:', e);
      }
    }
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #e0e0e0; 
  background: #1e1e1e; 
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  margin-bottom: 30px;
  text-align: center;
  position: relative;
}

header h1 {
  font-weight: 300;
  color: #e0e0e0;
}

.history-toggle {
  position: absolute;
  right: 0;
  top: 5px;
  background-color: #333;
  color: #888;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background-color 0.2s;
  border: 1px solid #444;
}

.history-toggle:hover {
  background-color: #404040;
}



main {
  margin-bottom: 50px;
}

footer {
  text-align: center;
  margin-top: 50px;
  padding: 20px 0;
  color: #888; 
  font-size: 0.9rem;
}
</style>