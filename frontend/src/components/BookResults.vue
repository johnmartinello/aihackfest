<template>
  <div class="results-container">
    <h2 class="results-title">Recommended Books</h2>
    <div class="book-cards">
      <div 
        v-for="book in books" 
        :key="book.id" 
        class="book-card"
        @click="redirectToGoogleSearch(book)"
      >
        <div class="book-cover">
          <img 
            :src="book.cover_url || 'https://via.placeholder.com/200x300?text=No+Cover'" 
            :alt="book.title"
            class="cover-image"
          />
        </div>
        <div class="book-details">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author" v-if="book.author">by {{ book.author }}</p>
          <p class="book-genre" v-if="book.genre">Genre: {{ book.genre }}</p>
          <p class="book-reason">{{ book.reason }}</p>
        </div>
      </div>
    </div>
    <div v-if="books.length === 0" class="no-results">
      <p>No books were found matching your query.</p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'BookResults',
  props: {
    books: {
      type: Array,
      required: true
    },
    isLoadingMore: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    redirectToGoogleSearch(book) {
      const query = `${book.title} (${book.author || 'Unknown Author'})`;
      const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
      window.open(url, '_blank');
    },
    loadMoreBooks() {
      this.$emit('load-more');
    }
  }
};
</script>

<style scoped>
.results-container {
  padding: 20px 0;
}

.results-title {
  font-size: 1.8rem;
  font-weight: 300;
  color: #e0e0e0; 
  margin-bottom: 25px;
  text-align: center;
}

.book-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* Changed to display exactly 4 cards per row */
  gap: 20px; /* Reduced gap slightly to accommodate more cards */
}

.book-card {
  background: #2d2d2d; 
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
}

.book-cover {
  height: 250px;
  overflow: hidden;
  background: #222; 
  display: flex;
  justify-content: center;
}

.cover-image {
  height: 100%;
  object-fit: cover;
}

.book-details {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.book-title {
  font-size: 1.3rem;
  margin-bottom: 8px;
  line-height: 1.3;
  color: #e0e0e0;
}

.book-author {
  font-size: 1rem;
  color: #bbb; 
  font-style: italic;
  margin-bottom: 15px;
}

.book-genre {
  font-size: 1rem;
  color: #bbb; 
  margin-bottom: 10px;
}

.book-reason {
  font-size: 0.9rem;
  color: #999; 
  margin-top: 10px;
}

.no-results {
  text-align: center;
  padding: 40px 0;
  color: #bbb;
}


</style>