<template>
  <div>
    <button @click="showAddModal = true">Add Product</button>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Category</th>
          <th>Price</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>{{ product.id }}</td>
          <td>{{ product.name }}</td>
          <td>{{ product.category }}</td>
          <td>{{ product.price }}</td>
          <td>
            <button @click="editProduct(product)">Edit</button>
            <button @click="confirmDelete(product.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <modal v-if="showAddModal" @close="showAddModal = false">
      <!-- Add Product Modal Content -->
    </modal>
    <modal v-if="showEditModal" @close="showEditModal = false">
      <!-- Edit Product Modal Content -->
    </modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      products: [],
      showAddModal: false,
      showEditModal: false,
    };
  },
  methods: {
    fetchProducts() {
      fetch('/api/products') // Adjust the API endpoint as necessary
        .then(response => response.json())
        .then(data => {
          this.products = data;
        })
        .catch(error => console.error('Error fetching products:', error));
    },
    editProduct(product) {
      // Set up for editing the product
      this.showEditModal = true;
      // Further setup for editing, e.g. populate a form
    },
    confirmDelete(id) {
      // Confirm deletion
      if (confirm('Are you sure you want to delete this product?')) {
        this.deleteProduct(id);
      }
    },
    deleteProduct(id) {
      // API call to delete the product
      fetch(`/api/products/${id}`, {
        method: 'DELETE',
      })
        .then(() => {
          this.fetchProducts(); // Refresh the list
        })
        .catch(error => console.error('Error deleting product:', error));
    }
  },
  mounted() {
    this.fetchProducts();
  }
};
</script>
