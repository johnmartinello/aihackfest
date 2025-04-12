<template>
  <div class="history-container">
    <div class="history-header">
      <h3>Search History</h3>
      <button v-if="searchHistory.length > 0" @click="clearHistory" class="clear-history-button">
        Clear History
      </button>
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
  methods: {
    selectSearch(item) {
      this.$emit('select-search', item);
    },
    clearHistory() {
      this.$emit('clear-history');
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString(undefined, {
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  },
  computed: {
    // Add computed property to create preview data for each search
    // This prevents passing too much data to the component
    formattedHistory() {
      return this.searchHistory.map(item => {
        return {
          ...item,
          previewBooks: item.books.slice(0, 3)
        };
      });
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

.history-header h3 {
  font-size: 1.4rem;
  font-weight: 300;
  color: #e0e0e0;
  margin: 0;
}

.clear-history-button {
  background-color: #555;
  color: #ddd;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
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
</style>