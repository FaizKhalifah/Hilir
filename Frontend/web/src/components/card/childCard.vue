<template>
 <div>
    <h2>Children List</h2>
    <ul v-if="children.length">
      <li v-for="child in children" :key="child.child_id">
        <h3>Child ID: {{ child.child_id }}</h3>
        <p>Name: {{ child.name }}</p>
        <p>Age: {{ child.age }}</p>
        <p>Gender: {{ child.gender }}</p>
      </li>
    </ul>
    <p v-else>Loading...</p>
  </div>
</template>
<style scoped>
    *{
        color: black;
    }
</style>
<script>
    export default{
        name:"childCardComponent",
        data() {
    return {
      children: [], 
    };
  },
  mounted() {
    this.fetchChildren();
  },
  methods: {
    async fetchChildren() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/psychologists/all_children', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`, 
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        console.log(data)
        this.children = data; 
        console.log(this.children[1])
      } catch (error) {
        console.error('Fetch error:', error);
      }
    }
    }
}
</script>