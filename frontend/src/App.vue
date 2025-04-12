<template>
  <div class="app-container">
    <header>
      <h1>Book Recommendation System</h1>
    </header>
    <main>
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
import axios from 'axios';

export default {
  name: 'App',
  components: {
    BookSearch,
    BookResults
  },
  data() {
    return {
      books: [],
      hasResults: false,
      searchId: null,
      searchQuery: '',
      isLoadingMore: false
    };
  },
  methods: {
    handleBooksLoaded(data) {
      this.books = data.books;
      this.searchId = data.id;
      this.searchQuery = data.query;
      this.hasResults = true;
    },
    async loadMoreBooks() {
      if (!this.searchId || this.isLoadingMore) return;
      
      this.isLoadingMore = true;
      
      try {
        const response = await axios.post('http://localhost:8000/api/more-books', {
          search_id: this.searchId,
          count: 8
        });
        
        // Update books with the full list (including new recommendations)
        this.books = response.data.books;
      } catch (error) {
        console.error('Error loading more books:', error);
      } finally {
        this.isLoadingMore = false;
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
}

header h1 {
  font-weight: 300;
  color: #e0e0e0;
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