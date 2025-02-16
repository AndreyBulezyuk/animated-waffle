# Part 1

### **Objective:**

Build a small web application in our tech stack.

### Background

We use **Python Django** as our backend framework and **htmx** for creating dynamic, reactive front-end functionality. Since our needs do not justify adopting a single-page application (SPA) architecture, we prioritize server-side rendering with lightweight interactivity using htmx. For styling, we rely on the **Bootstrap** library.

The web application for this challenge is intended to manage the inventory of a strongly simplified gas storage facility.

### Entities

The inventory consists of the following:

- **Components**: Each component is defined by a customer-given identifier and a brief description.
- **Inventory Levels**: Components are organized in a tree structure built of “inventory levels” that represents the facility's hierarchy. They also have meta information but for simplicity, you can reduce that to just a name besides the tree funcionality.

### Features to Implement

1. **Component List with Endless Scrolling**
    - Display a list of all components.
    - Implement endless scrolling to load additional components as the user scrolls down the page.
2. **Filtering and Sorting**
    - Add filters to search components by their name.
    - Enable filtering by inventory level.
    - Ensure table columns are sortable.
3. **Component Creation via Modal Dialog**
    - Provide a modal dialog to allow users to create new components.

### Constraints

- All interactions (e.g., filtering, sorting, endless scrolling, and creating components) should not trigger a full page reload.
- Leverage **htmx** to handle these interactions dynamically, ensuring a smooth and responsive user experience.