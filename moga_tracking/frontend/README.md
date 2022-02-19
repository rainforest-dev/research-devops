# Frontend part of moga_tracking

## Packages

- [vite-plugin-pages](https://github.com/hannoeru/vite-plugin-pages)

```bash
npm install -D vite-plugin-pages
npm install vue-router@next
```

```ts
// vite.config.ts
import Pages from "vite-plugin-pages";

export default {
  plugins: [
    // ...
    Pages(),
  ],
};
```

```ts
// main.ts or routes.ts or anywhere
import { createRouter } from "vue-router";
import routes from "~pages";

const router = createRouter({
  // ...
  routes,
});
```

- [class-transformer](https://github.com/typestack/class-transformer)

```bash
npm install class-transformer --save
npm install reflect-metadata --save
```

```html
<!-- index.html -->
<html>
  <head>
    <!-- ... -->
    <script src="node_modules/reflect-metadata/Reflect.js"></script>
  </head>
  <!-- ... -->
</html>
```

# Vue 3 + Typescript + Vite

This template should help get you started developing with Vue 3 and Typescript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

## Recommended IDE Setup

- [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar)

## Type Support For `.vue` Imports in TS

Since TypeScript cannot handle type information for `.vue` imports, they are shimmed to be a generic Vue component type by default. In most cases this is fine if you don't really care about component prop types outside of templates. However, if you wish to get actual prop types in `.vue` imports (for example to get props validation when using manual `h(...)` calls), you can enable Volar's `.vue` type support plugin by running `Volar: Switch TS Plugin on/off` from VSCode command palette.
